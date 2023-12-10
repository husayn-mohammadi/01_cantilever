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

def convergeIt(typeAnalysis, tagNodeControl, dofNodeControl, incrInit, incr, numIncr, dispIndex, dispList, disp, dispTarget, dispTar, numFrac, iii, t_beg):
    
    testerList      = ['NormDispIncr', 'NormUnbalance', 'EnergyIncr', ]#, 'RelativeNormUnbalance']
    algorithmList   = [*(1*['KrylovNewton', 'Newton', 'RaphsonNewton', 'NewtonLineSearch 0.65', ]), 'KrylovNewton'] #, 'Linear', 'Newton', 'NewtonLineSearch', 'ModifiedNewton', 'KrylovNewton', 'SecantNewton', 'RaphsonNewton', 'PeriodicNewton', 'BFGS', 'Broyden'
    tol = 1e-8; numIter = 200
    numIncrMax      = 300000
    
    for i in range(100000000):
        for algorithm in algorithmList:
            for tester in testerList:
                ops.test(tester, tol, numIter)
                ops.algorithm(algorithm)  
                #   integrator('DisplacementControl', nodeTag,        dof,            incr, numIter=1, dUmin=incr, dUmax=incr)
                ops.integrator('DisplacementControl', tagNodeControl, dofNodeControl, incr)
                ops.analysis('Static')
                
                curD    = ops.nodeDisp(tagNodeControl, dofNodeControl)
                # print(f"curD = {curD}")
                remD    = dispTar - curD
                # print(f"remD = {remD}")
                # numIncr = max(int(remD/dispFrac *numIncrList[iii]), 1)
                # incr    = remD/numIncr
                
                print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print(f"--------------------------------------\nAlgorithm:\t{algorithm}")
                print(f"--------------------------------------\ntester:\t\t{tester}\n--------------------------------------")
                print(f"======>>> disp({dispIndex+1:02}/{len(dispList):02})\t\t\t\t= {disp}")
                print(f"======>>> dispTarget\t\t\t\t= {dispTarget}")
                print(f"======>>> dispTar({iii+1:02}/{numFrac:02})\t\t\t= {dispTar}")
                print(f"======>>> Current   Displacement\t= {curD}")
                print(f"======>>> Remaining Displacement\t= {remD}")
                print(f"numIncr\t\t\t= {numIncr}")
                print(f"Incr\t\t\t= {incr}")
                
                # Run Analysis
                #        analyze(numIncr=1, dt=0.0, dtMin=0.0, dtMax=0.0, Jd=0)
                OK = ops.analyze(numIncr)
                print(f"AnalyzeOutput\t= {OK}")
                if OK == 0:
                    curD    = ops.nodeDisp(tagNodeControl, dofNodeControl)
                    remD    = dispTar - curD
                    numIncr = max(int(remD/incrInit), 1)
                    incr    = remD/numIncr
                    break
                elif OK != 0:
                    t_now=time.time(); elapsed_time=t_now-t_beg; mins=int(elapsed_time/60); secs=int(elapsed_time%60)
                    print(f"\nElapsed time: {mins} min + {secs} sec")
                    print(f"\n=============== The tester {tester} failed to converge!!! ===============")
                    curD    = ops.nodeDisp(tagNodeControl, dofNodeControl)
                    remD    = dispTar - curD
                    numIncr = int(remD/incr)
                    incr    = remD/numIncr
            
            if OK == 0:
                break
            elif OK != 0:
                print(f"\n=============== THE ALGORITHM {algorithm} FAILED TO CONVERGE!!! ===============")
                
        if OK == 0:
            break
        else:
            tol = 1.5*tol;                                          print(f"\n{'#'*65}\nAnalysis Failed!!\nReducing the Incr size:\n{'#'*65}"); print(f"\ntolerance = {tol}");              
            curD    = ops.nodeDisp(tagNodeControl, dofNodeControl); print(f"======>>> Current   Displacement\t= {curD}")
            remD    = dispTar - curD;                               print(f"======>>> Remaining Displacement\t= {remD}")
            numIncr = int(numIncr*1.01**i + 1);                     print(f"numIncr\t\t\t= {numIncr}")
            incr    = remD/numIncr;                                 print(f"Incr\t\t\t= {incr}")
            if numIncr >= numIncrMax:
                print("\nIncrement size is too small!!!")
                t_now=time.time(); elapsed_time=t_now-t_beg; mins=int(elapsed_time/60); secs=int(elapsed_time%60)
                print(f"\nElapsed time: {mins} min + {secs} sec")
                winsound.Beep(440, 1000)  # generate a 440Hz sound that lasts 500 milliseconds
                print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(f"*!*!*!*!*!* The {typeAnalysis} pushover analysis failed to converge!!! *!*!*!*!*!*")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                break
    return OK

def pushoverDCF(dispTarget, incrMono, tagNodeLoad, n_story): 
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
    
    # numIncrList = [*(1*[20]), *(10*[15]), *(1*[20])]
    numIncrList = [int(dispTarget/incrMono)] # if the length unit is m: dispTarget/0.001 makes each incr equal to 1 mm 
    # dispFactor  = int(30*dispTarget)
    # n1          = 4*dispFactor
    # n2          = 3*dispFactor
    # numIncrList = create_list(n1, n2)
    numFrac     = len(numIncrList)
    dispFrac    = dispTarget/numFrac
    curD        = ops.nodeDisp(tagNodeControl, dofNodeControl)
    for iii in range(0, numFrac):
        numIncr = numIncrList[iii]
        print(f"\nnumIncr\t\t\t= {numIncr}")
        incr            = dispFrac/numIncr
        dispTar         = curD + dispFrac
        
        OK = convergeIt("Monotonic", tagNodeControl, dofNodeControl, incrMono, incr, numIncr, 0, ['This is a list'], dispTarget, dispTarget,  dispTar, numFrac, iii, t_beg)
        if OK < 0:
            break
    return OK


def cyclicAnalysis(dispList, incrInit, tagNodeLoad):
    t_beg           = time.time()
    dofNodeControl      = 1
    if type(tagNodeLoad) == list:
        tagNodeControl  = tagNodeLoad[-1]
    else: 
        tagNodeControl  = tagNodeLoad
    
    tagTSLinear         = 1
    ops.timeSeries('Linear',   tagTSLinear)
    tagPatternPlain     = 1
    ops.pattern('Plain', tagPatternPlain, tagTSLinear)
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
            numIncrList = [int(disp/incrInit)] # if the length unit is m: dispTarget/0.001 makes each incr equal to 1 mm 
            numFrac     = len(numIncrList)
            dispFrac    = delta/numFrac
            # print(f"dispFrac = {dispFrac}")
            for  iii in range(0, numFrac):
                numIncr = numIncrList[iii]
                # print(f"\nnumIncr\t\t\t= {numIncr}")
                incr    = dispFrac/numIncr
                # print(f"curD = {curD}")
                dispTar = curD + dispFrac
                # print(f"dispTar = {dispTar}")
                OK      = convergeIt('Cyclic', tagNodeControl, dofNodeControl, incrInit, incr, numIncr, dispIndex, dispList, disp, dispTarget, dispTar, numFrac, iii, t_beg)
                if OK < 0:
                    break
            if OK < 0:
                break
        if OK < 0:
            break
    
    return OK

    

def NTHA():
    
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



