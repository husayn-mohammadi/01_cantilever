exec(open("MAIN.py").readlines()[18]) # It SHOULD read and execute exec(open("Input/units    .py").read())
import openseespy.opensees     as ops
import numpy                   as np
import time
import sys
import functions.FuncRecorders as fr
import functions.FuncPlot      as fp
## import winsound
# from colorama import Fore, Style # print(f"{Fore.YELLOW} your text {Style.RESET_ALL}")

def analyzeEigen(nEigen, printIt):
    omega2List  = ops.eigen(nEigen)
    if printIt == True:
        for index, omega2 in enumerate(omega2List):
            period  = 2 * np.pi/omega2**0.5
            print(f"Period{index:02} = {period}")

def rayleighDamping(nEigen, zeta):
    eigenList = ops.eigen(nEigen)
    # print(eigenList)
    omegaI2 = eigenList[0]
    omegaJ2 = eigenList[1]
    omegaI = omegaI2**0.5
    omegaJ = omegaJ2**0.5
    alphaM = 2.0*zeta*(omegaI*omegaJ)/(omegaI+omegaJ)
    betaKinit = 2.0*zeta/(omegaI+omegaJ)
    # rayleigh(alphaM, betaK, betaKinit, betaKcomm)
    ops.rayleigh(alphaM, 0.0, betaKinit, 0.0)

def gravity(load, tagNodeLoad):
    
    tagTSGravity    = 10
    ops.timeSeries('Linear', tagTSGravity)
    # ops.timeSeries('Constant', tagTSGravity)
    
    tagPtnGravity   = 10
    ops.pattern('Plain', tagPtnGravity, tagTSGravity)
    print(f"Type of tagNodeLoad is {type(tagNodeLoad)}")
    if type(tagNodeLoad) == int: 
        print("Loading is based on Cantilever Column Structure.")
        ops.load(tagNodeLoad, 0.0, -abs(load), 0.0)
    else:
        print("Loading is based on Shear Wall Structure.")
        for element, tagNodes in tagNodeLoad.items():
            if element == "wall":
                for tagNode in tagNodes:
                    ops.load(tagNode, 0.0, -abs(load["wall"]), 0.0)
            elif element == "leaningColumn":
                for tagNode in tagNodes:
                    ops.load(tagNode, 0.0, -abs(load["leaningColumn"]), 0.0)
            else:
                print("In GravityLoading element type was unknown!"); sys.exit()
    
    
    # Gravity Analysis:
    tol = 1.0e-5
    iteration = 100    
    
    ops.wipeAnalysis()
    ops.constraints('Transformation')
    ops.numberer('RCM')
    ops.system('BandGen')
    ops.test('NormDispIncr', tol, iteration)
    ops.algorithm('Newton')
    ops.integrator('LoadControl', 0.1)
    # ops.integrator('LoadControl', 1)
    ops.analysis('Static')
    ops.analyze(10)
    # ops.analyze(1)
    ops.loadConst('-time', 0.0)

def convergeIt(typeAnalysis, tagNodeLoad, tagNodeBase, dofNodeControl, incrFrac, numFrac, disp, dispIndex, dispList, dispTarget, t_beg, numIncrInit=5):
    if type(tagNodeLoad) == list:
        tagNodeControl  = tagNodeLoad[-1]
    else:
        tagNodeControl  = tagNodeLoad
        
    def curD():
        if typeAnalysis=="NTHA":
            
            t = ops.getTime()
            
            drift       = []
            tagNodePrv  = tagNodeBase
            if type(tagNodeLoad) == list:
                for i, tagNode in enumerate(tagNodeLoad):
                    if i >0:
                        height  = ops.nodeCoord(tagNode)[1] - ops.nodeCoord(tagNodePrv)[1]
                        dispTop = ops.nodeDisp(tagNode,    dofNodeControl)
                        dispBot = ops.nodeDisp(tagNodePrv, dofNodeControl)
                        drift[i]= abs(dispTop - dispBot)/height
                    tagNodePrv = tagNode
                driftMax = max(drift)
                driftAve = sum(drift)/len(drift)
            else:
                height  = ops.nodeCoord(tagNodeLoad)[1] - ops.nodeCoord(tagNodeBase)[1]
                dispTop = ops.nodeDisp(tagNodeLoad, dofNodeControl)
                dispBot = ops.nodeDisp(tagNodeBase, dofNodeControl)
                driftMax=driftAve= abs(dispTop - dispBot)/height
            return t, driftAve, driftMax
        else:
            d = ops.nodeDisp(tagNodeControl, dofNodeControl)
            return d, -1
    
    def msgCurrentState():
        if typeAnalysis=="NTHA":
            remD    = dispTarget - curD()[0]
            print(f"\n{'~'*100}")
            print(f"{'-'*60}\nAlgorithm:\t{algorithm}")
            print(f"{'-'*60}\ntester:\t\t{tester}\n{'-'*60}")
            print(f"======>>> durGM\t\t\t\t= {dispTarget}")
            print(f"======>>> dT({iii:05}/{numFrac:05})\t= {dispTar}")
            print(f"======>>> Current   Time\t= {curD()[0]}")
            print(f"======>>> Remaining Time\t= {remD}")
            print(f"numIncr\t\t\t= {numIncr}")
            print(f"dt\t\t\t\t= {incr}")
        else:
            remD    = dispTarget - curD()[0]
            print(f"\n{'~'*100}")
            print(f"{'-'*60}\nAlgorithm:\t{algorithm}")
            print(f"{'-'*60}\ntester:\t\t{tester}\n{'-'*60}")
            print(f"======>>> disp({dispIndex+1:02}/{len(dispList):02})\t\t\t\t= {disp}")
            print(f"======>>> dispTarget\t\t\t\t= {dispTarget}")
            print(f"======>>> dispTar({iii:02}/{numFrac:02})\t\t\t= {dispTar}")
            print(f"======>>> Current   Displacement\t= {curD()[0]}")
            print(f"======>>> Remaining Displacement\t= {remD}")
            print(f"numIncr\t\t\t= {numIncr}")
            print(f"Incr\t\t\t= {incr}")
    
    def msgReducingIncrSize():
        if typeAnalysis=="NTHA":
            print(f"\n{'#'*65}\nAnalysis Failed!!\nReducing the dt size:\n{'#'*65}")
            print(f"\n>>>>>>>>> tolerance\t\t\t= {tol}")
            print(f"======>>> Current   Time\t= {curD()[0]}")
            print(f"======>>> Remaining Time\t= {remD}")
            print(f"numIncr\t\t\t= {numIncr}")
            print(f"dt\t\t\t\t= {incr}")
            
        else:
            print(f"\n{'#'*65}\nAnalysis Failed!!\nReducing the Incr size:\n{'#'*65}")
            print(f"\n>>>>>>>>> tolerance\t\t\t= {tol}")
            print(f"======>>> Current   Displacement\t= {curD()[0]}")
            print(f"======>>> Remaining Displacement\t= {remD}")
            print(f"numIncr\t\t\t= {numIncr}")
            print(f"Incr\t\t\t= {incr}")
    
    for iii in range(1, numFrac+1):
        dispTar = iii * incrFrac
        testerList      = ['NormDispIncr', 'NormUnbalance', 'EnergyIncr', ]#, 'RelativeNormUnbalance']
        algorithmList   = [*(1*['Newton', 'KrylovNewton', 'RaphsonNewton', 'NewtonLineSearch 0.65', ])] #, 'Linear', 'Newton', 'NewtonLineSearch', 'ModifiedNewton', 'KrylovNewton', 'SecantNewton', 'RaphsonNewton', 'PeriodicNewton', 'BFGS', 'Broyden'
        tol = 1e-8; numIter = 200; gamma = 0.5; beta = 0.25
        numIncrMax      = 30000; incrMin = 1e-6
        
        numIncr     = numIncrInit
        incr        = incrFrac/numIncrInit
        j = 1
        for i in range(100000000):
        
            for algorithm in algorithmList:
                for tester in testerList:
                    ops.test(tester, tol, numIter)
                    ops.algorithm(algorithm)  
                    if typeAnalysis == "NTHA":
                        ops.integrator('Newmark', gamma, beta)
                        ops.analysis('Transient')
                    else:
                        ops.integrator('DisplacementControl', tagNodeControl, dofNodeControl, incr)
                        ops.analysis('Static')
                    msgCurrentState()
                    
                    # Run Analysis
                    if typeAnalysis == "NTHA": 
                        OK = ops.analyze(numIncr, incr)
                    else:
                        OK = ops.analyze(numIncr)
                    print(f"AnalyzeOutput\t= {OK}")
                    t_now=time.time(); elapsed_time=t_now-t_beg; mins=int(elapsed_time/60); secs=int(elapsed_time%60)
                    print(f"\nElapsed time: {mins} min + {secs} sec")
                    if OK == 0: break
                    elif OK != 0:
                        t_now=time.time(); elapsed_time=t_now-t_beg; mins=int(elapsed_time/60); secs=int(elapsed_time%60)
                        print(f"\nElapsed time: {mins} min + {secs} sec")
                        print(f"\n=============== The tester {tester} failed to converge!!! ===============")
                if OK == 0: break
                elif OK != 0:
                    print(f"\n=============== THE ALGORITHM {algorithm} FAILED TO CONVERGE!!! ===============")
            if OK == 0: break
            else:
                tol = min(1.5*tol, 1e-4)
                remD    = dispTar - curD()[0]
                if remD >= 0.001:
                    numIncr = int(numIncr*1.001**i + j)
                    j += 1
                    incr    = remD/numIncr
                else:
                    numIncr = 1
                    incr    = remD/numIncr
                msgReducingIncrSize()
                if numIncr >= numIncrMax or incr <= incrMin:
                    print("\nIncrement size is too small!!!")
                    t_now=time.time(); elapsed_time=t_now-t_beg; mins=int(elapsed_time/60); secs=int(elapsed_time%60)
                    print(f"\nElapsed time: {mins} min + {secs} sec")
                    # winsound.Beep(440, 1000)  # generate a 440Hz sound that lasts 500 milliseconds
                    text = " pushover" if typeAnalysis!="NTHA" else ""
                    print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print(f"*!*!*!*!*!* The {typeAnalysis}{text} analysis failed to converge!!! *!*!*!*!*!*")
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    break
        if OK < 0: break
        if typeAnalysis == "NTHA":
            driftMaxAllowed = 1e-3
            if curD()[2] >= driftMaxAllowed: 
                print(f"driftMax = {curD()[2]} >= {driftMaxAllowed} ==> the next scaleFactor will be applied now!")
                break
    return OK

def pushoverDCF(dispTarget, incrInit, numIncrInit, tagNodeLoad): 
    t_beg           = time.time()
    dofNodeControl  = 1
    tagTSLinear     = 1
    ops.timeSeries('Linear',   tagTSLinear)
    tagPatternPlain = 1
    ops.pattern('Plain', tagPatternPlain, tagTSLinear)
    #   load(nodeTag,     *loadValues)
    if type(tagNodeLoad) == list:
        tagNodeControl  = tagNodeLoad[-1]
        n_story = len(tagNodeLoad)-1
        for i, tagNode in enumerate(tagNodeLoad):
            ops.load(tagNode, *[i/n_story, 0, 0])
    else:
        tagNodeControl  = tagNodeLoad
        ops.load(tagNodeControl, *[1, 0, 0])
    
    #  Define Analysis Options
    ops.wipeAnalysis()
    ops.constraints('Transformation')
    ops.numberer('RCM')
    ops.system('FullGeneral')   # 'FullGeneral', 'UmfPack', 'SparseSYM', 
    disp        = dispTarget; dispIndex   = 0
    delta       = dispTarget
    numFrac     = int(delta/incrInit)
    incrFrac    = delta/numFrac
    asTagNodeBase = 1 #it is not going to be used at all in this analysis. it is just to fill a positional argument
    OK          = convergeIt("Monotonic", tagNodeLoad, asTagNodeBase, dofNodeControl, incrFrac, numFrac, disp, dispIndex, ['This is a list'], dispTarget, t_beg, numIncrInit)
    return OK


def cyclicAnalysis(dispList, incrInit, tagNodeLoad):
    asTagNodeBase   = 1 #it is not going to be used at all in this analysis. it is just to fill a positional argument
    t_beg           = time.time()
    dofNodeControl  = 1
    tagTSLinear     = 1
    ops.timeSeries('Linear',   tagTSLinear)
    tagPatternPlain = 1
    ops.pattern('Plain', tagPatternPlain, tagTSLinear)
    if type(tagNodeLoad) == list:
        tagNodeControl  = tagNodeLoad[-1]
        n_story = len(tagNodeLoad)-1
        for i, tagNode in enumerate(tagNodeLoad):
            ops.load(tagNode, *[i/n_story, 0, 0])
    else:
        tagNodeControl  = tagNodeLoad
        ops.load(tagNodeControl, *[1, 0, 0])
    
    #  Define Analysis Options
    ops.wipeAnalysis()
    ops.constraints('Transformation')
    ops.numberer('RCM') # Plain, RCM, AMD, ParallelPlain, ParallelRCM
    ops.system('FullGeneral') # BandGen, BandSPD, ProfileSPD, SuperLU, UmfPack, FullGeneral, SparseSYM, ('Mumps', '-ICNTL14', icntl14=20.0, '-ICNTL7', icntl7=7)
    
    # Run Analysis
    for dispIndex, disp in enumerate(dispList):
        print(f"\n\ndisp({dispIndex+1}/{len(dispList)})\t= {disp}")
        dispTargetList  = [disp, 0, -disp, 0]
        for index, dispTarget in enumerate(dispTargetList):
            curD        = ops.nodeDisp(tagNodeControl, dofNodeControl)
            delta       = dispTarget - curD
            numFrac     = int(abs(delta)/incrInit)
            if numFrac == 0: numFrac=1
            incrFrac    = delta/numFrac
            OK          = convergeIt('Cyclic', tagNodeLoad, asTagNodeBase, dofNodeControl, incrFrac, numFrac, disp, dispIndex, dispList, dispTarget, t_beg, numIncrInit=2)
            if OK < 0: break
        if OK < 0: break
    return OK



def NTHA1(tagNodeLoad, tagNodeBase, filePath, SaGM, scaleFactor, dtGM, NPTS, Tmax, tag):
    # ops.wipeAnalysis()
    t_beg           = time.time()
    dofNodeControl  = 1
    tagTSPath       = 1
    ops.timeSeries('Path', tagTSPath, '-dt', dtGM, '-filePath', filePath, '-factor', scaleFactor)
    tagPatternNTHA  = tag
    direction       = 1
    ops.pattern('UniformExcitation', tagPatternNTHA, direction,'-accel', tagTSPath)
    
    #  Define Analysis Options
    ops.wipeAnalysis()
    ops.constraints('Transformation')
    ops.numberer('RCM')
    ops.system('FullGeneral')
    
    # Run Analysis
    OK          = convergeIt('NTHA', tagNodeLoad, tagNodeBase, dofNodeControl, dtGM, NPTS, Tmax, 0, ["No list required!"], Tmax, t_beg, numIncrInit=2)
    ops.wipeAnalysis()
    return OK

def NTHA(tagNodeLoad, tagNodeBase, tagNodeControl, L, outputDirNTHA):
    recList     = ["0.0200_01500_RSN825_CAPEMEND_CPM000.txt", 
                   ]
    NPTSList    = [50]     # you can add more values to this list programmatically, instead of typing them manually
    dtGMList    = [0.02]    # you can add more values to this list programmatically, instead of typing them manually
    SaGMList    = [0.04973] # you can add more values to this list programmatically, instead of typing them manually
    SaTarget    = 1.5 * 0.63/10# MCE = 1.5*DBE
    extraTime   = 0
    # rayleighDamping(2, 0.05)
    numRecords  = len(recList)
    for i_rec, rec in enumerate(recList):
        print(f"\n{'#'*65}\nRunning record {i_rec+1:02}/{numRecords:02}: {rec} for Sa = {SaTarget}*g\n{'#'*65}")
        SaGM        = SaGMList[i_rec]
        dtGM        = dtGMList[i_rec]
        NPTS        = NPTSList[i_rec]
        
        filePath    = f"Input/GM/{rec}" 
        Tmax        = NPTS*dtGM + extraTime
        # dtAnalysis  = dtGM/200 # it can't be greater than dt
        # numIncr     = int(Tmax/dtAnalysis)
        scaleFactor = SaTarget/SaGM*g
        scaleFactorList = [ 
                            # 0.1*scaleFactor, 
                            # 0.1*scaleFactor, 
                            # 0.1*scaleFactor, 
                            # 0.1*scaleFactor, 
                            0.1*scaleFactor, 
                            0.1*scaleFactor, 
                            # 0.2*scaleFactor,
                            # 0.5*scaleFactor,
                            # 1.0*scaleFactor,
                            # 1.5*scaleFactor,
                            # 2.0*scaleFactor,
                            # 3.0*scaleFactor,
                            # 4.0*scaleFactor,
                            # 5.0*scaleFactor,
                            # 10.*scaleFactor,
                           ]
        for tag, scaleFactor in enumerate(scaleFactorList):
            fr.recordDataNTHA(tagNodeBase, tagNodeControl, outputDirNTHA, tag+1)
            OK = NTHA1(tagNodeLoad, tagNodeBase, filePath, SaGM, scaleFactor, dtGM, NPTS, Tmax, tag+1)
            fp.plotNTHA(L, outputDirNTHA, tag+1)
            ops.remove('timeSeries', 1)
            ops.remove('loadPattern', 1)
        
        return OK



















