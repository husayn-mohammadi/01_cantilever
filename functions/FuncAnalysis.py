import openseespy.opensees as ops
import time
import sys
# from colorama import Fore, Style

waitTime        = 0.0
waitTime2       = 0.0
testerList      = ['NormUnbalance', 'NormDispIncr', 'EnergyIncr', 'RelativeNormUnbalance']*2
algorithmList   = [ 'KrylovNewton', 'Linear', 'Newton', 'NewtonLineSearch', 'ModifiedNewton', 'SecantNewton', 'RaphsonNewton', 'PeriodicNewton']*2 # Linear, Newton, NewtonLineSearch, ModifiedNewton, KrylovNewton, SecantNewton, RaphsonNewton, PeriodicNewton, BFGS, Broyden

def gravity(Py, ControlNode):
    
    tagTSGravity    = 10
    # ops.timeSeries('Linear', tagTSGravity)
    ops.timeSeries('Constant', tagTSGravity)
    
    tagPtnGravity   = 10
    ops.pattern('Plain', tagPtnGravity, tagTSGravity)
    ops.load(ControlNode, 0.0, -abs(Py), 0.0)
    
    
    # Gravity Analysis:
    tol = 1.0e-5
    iteration = 100    
    
    ops.wipeAnalysis()
    ops.constraints('Transformation')
    ops.numberer('RCM')
    ops.system('BandGen')
    ops.test('NormDispIncr', tol, iteration)
    ops.algorithm('Newton')
    # ops.integrator('LoadControl', 0.1)
    ops.integrator('LoadControl', 1)
    ops.analysis('Static')
    # ops.analyze(10)
    ops.analyze(1)
    # ops.loadConst('-time', 0.0)

def pushoverDCF(dispTarget, ControlNode): 
    
    ControlNodeDoF  = 1
    dForce          = 1 # The pushover curve is not dependent to the value of dForce
    
    # incr        = dispTarget/numIncr
    tol         = 1e-8
    numIter     = 50
    
    #  Define Time Series: Constant/Linear/Trigonometric/Triangular/Rectangular/Pulse/Path TimeSeries
    tagTSLinear     = 1
    #   timeSeries('Linear',   tag, '-factor', factor=1.0, '-tStart', tStart=0.0)
    ops.timeSeries('Linear',   tagTSLinear)
    
    #  Define Loads: Plain/UniformExcitation/Multi-Support Excitation Pattern
    tagPatternPlain = 1
    #   pattern('Plain', patternTag,      tsTag, '-fact', fact)
    ops.pattern('Plain', tagPatternPlain, tagTSLinear)
    #   load(nodeTag,     *loadValues)
    ops.load(ControlNode, *[dForce, 0, 0])
    
    
    #  Define Analysis Options
    
    ops.wipeAnalysis()
    ops.constraints('Transformation')
    ops.numberer('RCM')
    ops.system('BandGen')
    
    numIncrList = [*(1*[50]), *(2*[20]), *(3*[10]), *(2*[20]), *(1*[50])]
    numFrac     = len(numIncrList)
    dispFrac    = dispTarget/numFrac
    for iii in range(0, numFrac):
        numIncr = numIncrList[iii]
        print(f"\nnumIncr\t\t\t= {numIncr}")
        incr            = dispFrac/numIncr
        dispTar         = dispFrac*(iii+1)
        for algorithm in algorithmList:
            ops.algorithm(algorithm)  
            print(f"Algorithm:\t{algorithm}")
            curD    = ops.nodeDisp(ControlNode, ControlNodeDoF)
            print(f"======>>> Current   Displacement\t= {curD:.4f}")
            remD    = dispTar - curD
            print(f"======>>> Remaining Displacement\t= {remD:.4f}")
            numIncr = numIncrList[iii]
            print(f"\nnumIncr\t\t\t= {numIncr}")
            incr    = remD/numIncr
            print(f"======>>> Increment size is {incr}")
            
            for tester in testerList:
                ops.test(tester, tol, numIter)
                print(f"\ntester:\t\t{tester}")
                curD    = ops.nodeDisp(ControlNode, ControlNodeDoF)
                print(f"======>>> Current   Displacement\t= {curD:.4f}")
                remD    = dispTar - curD
                print(f"======>>> Remaining Displacement\t= {remD:.4f}")
                numIncr = numIncrList[iii]
                print(f"\nnumIncr\t\t\t= {numIncr}")
                incr    = remD/numIncr
                print(f"======>>> Increment size is {incr}")
                
                while True:
                    #   integrator('DisplacementControl', nodeTag,     dof,            incr, numIter=1, dUmin=incr, dUmax=incr)
                    ops.integrator('DisplacementControl', ControlNode, ControlNodeDoF, incr)
                    ops.analysis('Static')
                    
                    # Run Analysis
                    #        analyze(numIncr=1, dt=0.0, dtMin=0.0, dtMax=0.0, Jd=0)
                    OK      = ops.analyze(numIncr)
                    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    print(f"AnalyzeOutput\t= {OK}")
                    if OK == 0:
                        break
                    
                    print(f"Algorithm:\t{algorithm}")
                    print(f"tester:\t\t{tester}")
                    
                    print(f"\n\n======>>> dispTarget\t\t\t\t= {dispTarget:.4f}")
                    print(f"======>>> dispTar({iii+1}/{numFrac})\t\t\t\t= {dispTar:.4f}")
                    curD    = ops.nodeDisp(ControlNode, ControlNodeDoF)
                    print(f"======>>> Current   Displacement\t= {curD:.4f}")
                    remD    = dispTar - curD
                    print(f"======>>> Remaining Displacement\t= {remD:.4f}")
                    numIncr = int(numIncr*3)
                    print(f"numIncr\t\t\t= {numIncr}")
                    incr    = remD/numIncr
                    print(f"Incr\t\t\t= {incr}")
                    time.sleep(waitTime)
                    if numIncr >= 800:
                        print("\nIncrement size is too small!!!")
                        time.sleep(waitTime)
                        break
                
                if OK == 0:
                    break
                elif OK != 0:
                    print(f"\n=============== The tester {tester} failed to converge!!! ===============")
                    time.sleep(waitTime)
                
            if OK == 0:
                break
            elif OK != 0:
                print(f"\n=============== The algorithm {algorithm} failed to converge!!! ===============")
                time.sleep(waitTime)
                if tester == testerList[-1] and algorithm == algorithmList[-1]:
                    print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print("*!*!*!*!*!* The monotonic pushover analysis failed to converge!!! *!*!*!*!*!*")
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"); sys.exit()
            
    
    return OK


def cyclicAnalysis(dispList, ControlNode, numCyclesPerDispTarget=2):
    
    ControlNodeDoF  = 1
    dForce          = 1 # The pushover curve is not dependent to the value of dForce
    
    tol         = 1e-8
    numIter     = 100
    
    #  Define Time Series: Constant/Linear/Trigonometric/Triangular/Rectangular/Pulse/Path TimeSeries
    tagTSLinear     = 1
    #   timeSeries('Linear',   tag, '-factor', factor=1.0, '-tStart', tStart=0.0)
    ops.timeSeries('Linear',   tagTSLinear)
    
    #  Define Loads: Plain/UniformExcitation/Multi-Support Excitation Pattern
    tagPatternPlain = 1
    #   pattern('Plain', patternTag,      tsTag, '-fact', fact)
    ops.pattern('Plain', tagPatternPlain, tagTSLinear)
    #   load(nodeTag,     *loadValues)
    ops.load(ControlNode, *[dForce, 0, 0])
    
    
    #  Define Analysis Options
    
    ops.wipeAnalysis()
    ops.constraints('Transformation')
    ops.numberer('RCM') # Plain, RCM, AMD, ParallelPlain, ParallelRCM
    ops.system('UmfPack') # BandGen, BandSPD, ProfileSPD, SuperLU, UmfPack, FullGeneral, SparseSYM, ('Mumps', '-ICNTL14', icntl14=20.0, '-ICNTL7', icntl7=7)
    
    # Run Analysis
    for dispIndex, disp in enumerate(dispList):
        print(f"\n\ndisp({dispIndex+1}/{len(dispList)})\t= {disp}"); time.sleep(waitTime)
        dispTargetList = [disp, 0, -disp, 0]*numCyclesPerDispTarget
        for dispTarget in dispTargetList:
            curD        = ops.nodeDisp(ControlNode, ControlNodeDoF)
            delta       = dispTarget - curD
            print (f"delta = {delta}")
            numIncrList = [*(1*[5]), *(10*[3]), *(1*[5])]
            numFrac     = len(numIncrList)
            dispFrac    = delta/numFrac
            print(f"dispFrac = {dispFrac}")
            for  iii in range(0, numFrac):
                numIncr = numIncrList[iii]
                print(f"\nnumIncr\t\t\t= {numIncr}")
                incr            = dispFrac/numIncr
                dispTar         = dispFrac*(iii+1)
                for algorithm in algorithmList:
                    ops.algorithm(algorithm) 
                    print(f"======>>> dispTarget\t\t\t\t= {dispTarget}")
                    print(f"======>>> dispTar({iii+1}/{numFrac})\t\t\t\t= {dispTar}")
                    curD    = ops.nodeDisp(ControlNode, ControlNodeDoF)
                    print(f"======>>> Current   Displacement\t= {curD}")
                    remD    = dispTar - curD
                    print(f"======>>> Remaining Displacement\t= {remD}")
                    numIncr = numIncrList[iii]
                    print(f"numIncr\t\t\t= {numIncr}")
                    incr    = remD/numIncr
                    print(f"Incr\t\t\t= {incr}")
                    
                    for tester in testerList:
                        ops.test(tester, tol, numIter)
                        print(f"======>>> dispTarget\t\t\t\t= {dispTarget}")
                        print(f"======>>> dispTar({iii+1}/{numFrac})\t\t\t\t= {dispTar}")
                        curD    = ops.nodeDisp(ControlNode, ControlNodeDoF)
                        print(f"======>>> Current   Displacement\t= {curD}")
                        remD    = dispTar - curD
                        print(f"======>>> Remaining Displacement\t= {remD}")
                        numIncr = numIncrList[iii]
                        print(f"numIncr\t\t\t= {numIncr}")
                        incr    = remD/numIncr
                        print(f"Incr\t\t\t= {incr}")
                        
                        while True:
                            #   integrator('DisplacementControl', nodeTag,     dof,            incr, numIter=1, dUmin=incr, dUmax=incr)
                            ops.integrator('DisplacementControl', ControlNode, ControlNodeDoF, incr)
                            ops.analysis('Static') 
                            
                            print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                            print(f"\n\ndisp({dispIndex+1}/{len(dispList)})\t= {disp}")
                            print(f"--------------------------------------\nAlgorithm:\t{algorithm}")
                            print(f"--------------------------------------\ntester:\t\t{tester}\n--------------------------------------")
                            
                            
                            
                            # Run Analysis
                            #        analyze(numIncr=1, dt=0.0, dtMin=0.0, dtMax=0.0, Jd=0)
                            OK      = ops.analyze(numIncr)
                            print(f"AnalyzeOutput\t= {OK}"); time.sleep(waitTime2)
                            if OK == 0:
                                break
                            
                            print(f"Algorithm:\t{algorithm}")
                            print(f"tester:\t\t{tester}")
                            
                            print(f"\n======>>> dispTarget\t\t\t\t= {dispTarget}")
                            print(f"======>>> dispTar({iii+1}/{numFrac})\t\t\t\t= {dispTar}")
                            curD    = ops.nodeDisp(ControlNode, ControlNodeDoF)
                            print(f"======>>> Current   Displacement\t= {curD}")
                            remD    = dispTar - curD
                            print(f"======>>> Remaining Displacement\t= {remD}")
                            numIncr = int(numIncr*3)
                            print(f"numIncr\t\t\t= {numIncr}")
                            incr    = remD/numIncr
                            print(f"Incr\t\t\t= {incr}")
                            time.sleep(waitTime)
                            if numIncr >= 3000:
                                print("\nIncrement size is too small!!!")
                                time.sleep(waitTime)
                                break
                        
                        if OK == 0:
                            break
                        elif OK != 0:
                            print(f"\n=============== The tester {tester} failed to converge!!! ===============")
                            time.sleep(waitTime)
                            
                    if OK == 0:
                        break
                    elif OK != 0:
                        print(f"\n=============== The algorithm {algorithm} failed to converge!!! ===============")
                        time.sleep(waitTime)
                        if tester == testerList[-1] and algorithm == algorithmList[-1]:
                            print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                            print("*!*!*!*!*!* The cyclic pushover analysis failed to converge!!! *!*!*!*!*!*")
                            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"); sys.exit()
                            return OK
                    
            
    return OK

                




























