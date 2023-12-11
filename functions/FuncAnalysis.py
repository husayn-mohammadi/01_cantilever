exec(open("MAIN.py").readlines()[18]) # It SHOULD read and execute exec(open("Input/units    .py").read())
import openseespy.opensees     as ops
import numpy                   as np
import time
import sys
# import random                  as rn
import winsound
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

def convergeIt(typeAnalysis, tagNodeControl, dofNodeControl, incrFrac, numFrac, disp, dispIndex, dispList, dispTarget, t_beg, numIncrInit=5):
    
    def curD():
        if typeAnalysis=="NTHA":
            return ops.getTime()
        else:
            return ops.nodeDisp(tagNodeControl, dofNodeControl)
    
    def msgCurrentState():
        if typeAnalysis=="NTHA":
            remD    = dispTarget - curD()
            print(f"\n{'~'*100}")
            print(f"{'-'*60}\nAlgorithm:\t{algorithm}")
            print(f"{'-'*60}\ntester:\t\t{tester}\n{'-'*60}")
            print(f"======>>> durGM\t\t\t\t= {dispTarget}")
            print(f"======>>> dT({iii:05}/{numFrac:05})\t= {dispTar}")
            print(f"======>>> Current   Time\t= {curD()}")
            print(f"======>>> Remaining Time\t= {remD}")
            print(f"numIncr\t\t\t= {numIncr}")
            print(f"dt\t\t\t\t= {incr}")
        else:
            remD    = dispTarget - curD()
            print(f"\n{'~'*100}")
            print(f"{'-'*60}\nAlgorithm:\t{algorithm}")
            print(f"{'-'*60}\ntester:\t\t{tester}\n{'-'*60}")
            print(f"======>>> disp({dispIndex+1:02}/{len(dispList):02})\t\t\t\t= {disp}")
            print(f"======>>> dispTarget\t\t\t\t= {dispTarget}")
            print(f"======>>> dispTar({iii:02}/{numFrac:02})\t\t\t= {dispTar}")
            print(f"======>>> Current   Displacement\t= {curD()}")
            print(f"======>>> Remaining Displacement\t= {remD}")
            print(f"numIncr\t\t\t= {numIncr}")
            print(f"Incr\t\t\t= {incr}")
    
    def msgReducingIncrSize():
        if typeAnalysis=="NTHA":
            print(f"\n{'#'*65}\nAnalysis Failed!!\nReducing the dt size:\n{'#'*65}")
            print(f"\n>>>>>>>>> tolerance\t\t\t= {tol}")
            print(f"======>>> Current   Time\t= {curD()}")
            print(f"======>>> Remaining Time\t= {remD}")
            print(f"numIncr\t\t\t= {numIncr}")
            print(f"dt\t\t\t\t= {incr}")
            
        else:
            print(f"\n{'#'*65}\nAnalysis Failed!!\nReducing the Incr size:\n{'#'*65}")
            print(f"\n>>>>>>>>> tolerance\t\t\t= {tol}")
            print(f"======>>> Current   Displacement\t= {curD()}")
            print(f"======>>> Remaining Displacement\t= {remD}")
            print(f"numIncr\t\t\t= {numIncr}")
            print(f"Incr\t\t\t= {incr}")
    
    for iii in range(1, numFrac+1):
        dispTar = iii * incrFrac
        testerList      = ['NormDispIncr', 'NormUnbalance', 'EnergyIncr', ]#, 'RelativeNormUnbalance']
        algorithmList   = [*(1*['Newton', 'KrylovNewton', 'RaphsonNewton', 'NewtonLineSearch 0.65', ])] #, 'Linear', 'Newton', 'NewtonLineSearch', 'ModifiedNewton', 'KrylovNewton', 'SecantNewton', 'RaphsonNewton', 'PeriodicNewton', 'BFGS', 'Broyden'
        tol = 1e-8; numIter = 200; gamma = 0.5; beta = 0.25
        numIncrMax      = 30000
        
        numIncr     = numIncrInit
        incr        = incrFrac/numIncrInit
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
                remD    = dispTar - curD()
                numIncr = int(numIncr*1.001**i + 1)
                incr    = remD/numIncr
                msgReducingIncrSize()
                if numIncr >= numIncrMax:
                    print("\nIncrement size is too small!!!")
                    t_now=time.time(); elapsed_time=t_now-t_beg; mins=int(elapsed_time/60); secs=int(elapsed_time%60)
                    print(f"\nElapsed time: {mins} min + {secs} sec")
                    winsound.Beep(440, 1000)  # generate a 440Hz sound that lasts 500 milliseconds
                    text = " pushover" if typeAnalysis!="NTHA" else ""
                    print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print(f"*!*!*!*!*!* The {typeAnalysis}{text} analysis failed to converge!!! *!*!*!*!*!*")
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    break
        if OK < 0: break
    return OK

def pushoverDCF(dispTarget, incrInit, tagNodeLoad): 
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
    OK          = convergeIt("Monotonic", tagNodeControl, dofNodeControl, incrFrac, numFrac, disp, dispIndex, ['This is a list'], dispTarget, t_beg)
    return OK


def cyclicAnalysis(dispList, incrInit, tagNodeLoad):
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
            incrFrac    = delta/numFrac
            OK          = convergeIt('Cyclic', tagNodeControl, dofNodeControl, incrFrac, numFrac, disp, dispIndex, dispList, dispTarget, t_beg, numIncrInit=2)
            if OK < 0: break
        if OK < 0: break
    return OK

    

def NTHA(tagNodeLoad):
    t_beg           = time.time()
    dofNodeControl  = 1
    if type(tagNodeLoad) == list:
        tagNodeControl  = tagNodeLoad[-1]
    else:
        tagNodeControl  = tagNodeLoad
    filePath        = "Input/GM/0.0200_RSN825_CAPEMEND_CPM000.txt"
    SaTarget        = 1.5 * 0.63 /1                                   # MCE = 1.5*DBE
    SaGM            = 0.04973/0.1
    scaleFactor     = SaTarget/SaGM*g
    dtGM            = 0.02
    NPTS            = 1500
    tagTSPath       = 1
    ops.timeSeries('Path', tagTSPath, '-dt', dtGM, '-filePath', filePath, '-factor', scaleFactor)
    tagPatternNTHA  = 1
    direction       = 1
    ops.pattern('UniformExcitation', tagPatternNTHA, direction,'-accel', tagTSPath)
    
    #  Define Analysis Options
    ops.wipeAnalysis()
    ops.constraints('Transformation')
    ops.numberer('RCM')
    ops.system('FullGeneral')
    
    # Run Analysis
    Tmax        = NPTS * dtGM
    OK          = convergeIt('NTHA', tagNodeControl, dofNodeControl, dtGM, NPTS, Tmax, 0, ["No list required!"], Tmax, t_beg, numIncrInit=2)
    return OK
    
    recList     = [1]
    NPTSList    = [4000] # you can add more values to this list programmatically, instead of typing them manually
    dtGMList    = [0.01] # you can add more values to this list programmatically, instead of typing them manually

    print("SaGM corresponding to the Tn should be inserted into SaGMList manually for each record!!!")
    SaGMList    = [0.04973] # you can add more values to this list programmatically, instead of typing them manually
    SaTarget    = 1.5 * 0.63 /10# MCE = 1.5*DBE
    extraTime   = 0

    timeSeriesTag       = 100
    
    for i_rec, rec in enumerate(recList):
        print(f"\n\n{'#'*65}\nRunning record: {rec} for Sa = {SaTarget} g\n{'#'*65}")
        # outputDir = f"outputs/NTHA/{rec}/{SaTarget}"
        # analyzeEigen(2, True)
        rayleighDamping(2, 0.05)
        
        # 01) Extract Parameters from Lists:
        SaGM = SaGMList[i_rec]
        dtGM = dtGMList[i_rec]
        NPTS = NPTSList[i_rec]
        
        # 02) Lateral Load Pattern:
        filePath = f"Input/GM/2_txt/{rec}.txt" # Is there a way to read the name of all files in a folder and save them in an array? Yes: open readfilesinfolder.py
        dtAnalysis = dtGM/200 # it can't be greater than dt
        recDur = NPTS*dtGM + extraTime
        numIncr = int(recDur/dtAnalysis)
        scaleFactor = SaTarget/SaGM*g
        
        #   timeSeries('Path', tag,           '-dt', dt=0.0, '-values', *values, '-time', *time, '-filePath', filePath='', '-fileTime', fileTime='', '-factor', factor=1.0, '-startTime', startTime=0.0, '-useLast', '-prependZero')
        ops.timeSeries('Path', timeSeriesTag, '-dt', dtGM,                                       '-filePath', filePath,                              '-factor', scaleFactor)
        
        nthaLoadPatternTag  = 4
        direction           = 1
        #   pattern('UniformExcitation', patternTag,         dir,       '-disp', dispSeriesTag, '-vel', velSeriesTag, '-accel', accelSeriesTag, '-vel0', vel0, '-fact', fact)
        ops.pattern('UniformExcitation', nthaLoadPatternTag, direction,                                               '-accel', timeSeriesTag)
        
        # 03) Nonlinear Time-History Analysis:
        gamma = 0.5
        beta = 0.25
        
        tol = 1.0e-6
        iteration = 2000
        
        ops.wipeAnalysis()
        ops.constraints('Transformation')
        ops.numberer('RCM')
        ops.system('BandGeneral')
        ops.test('NormDispIncr', tol, iteration)
        ops.algorithm('Newton')
        ops.integrator('Newmark', gamma, beta)
        ops.analysis('Transient')
        ops.analyze(numIncr, dtAnalysis)






















