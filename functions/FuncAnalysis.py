import openseespy.opensees as ops
import time
import sys

waitTime        = 1
testerList      = ['NormDispIncr', 'EnergyIncr', 'NormUnbalance']
algorithmList   = ['Linear', 'Newton', 'KrylovNewton', 'NewtonLineSearch', 'ModifiedNewton', 'RaphsonNewton', 'SecantNewton']

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

def pushoverDCF(dispTarget, ControlNode, numIncr): # Linear, Newton, NewtonLineSearch, ModifiedNewton, KrylovNewton, SecantNewton, RaphsonNewton, PeriodicNewton, BFGS, Broyden
    
    ControlNodeDoF  = 1
    dForce          = 1 # The pushover curve is not dependent to the value of dForce
    
    incr        = dispTarget/numIncr
    tol         = 1e-8
    numIter     = 300
    
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
    
    for tester in testerList:
        ops.test(tester, tol, numIter)
        for algorithm in algorithmList:
            ops.algorithm(algorithm)  
            #   integrator('DisplacementControl', nodeTag,     dof,            incr, numIter=1, dUmin=incr, dUmax=incr)
            ops.integrator('DisplacementControl', ControlNode, ControlNodeDoF, incr)
            ops.analysis('Static')
            
            # Run Analysis
            #        analyze(numIncr=1, dt=0.0, dtMin=0.0, dtMax=0.0, Jd=0)
            OK = ops.analyze(numIncr)
            print(f"AnalyzeOutput = {OK}")
            curD    = ops.nodeDisp(ControlNode, ControlNodeDoF)
            print(f"\n\ndispTarget =\t{dispTarget:.4f}")
            print(f"======>>> Current Displacement is {curD:.4f}")
            print(f"tester:\t\t{tester}")
            print(f"Algorithm:\t{algorithm}")
            if OK == 0:
                break
            elif OK != 0:
                print(f"\n=============== The algorithm {algorithm} failed to converge!!! ===============")
                time.sleep(waitTime)
                if tester == testerList[-1] and algorithm == algorithmList[-1]:
                    print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print("*!*!*!*!*!* The monotonic pushover analysis failed to converge!!! *!*!*!*!*!*")
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"); sys.exit()
            
        if OK == 0:
            break
        elif OK != 0:
            print(f"\n=============== The tester {tester} failed to converge!!! ===============")
            time.sleep(waitTime)
            
    
    return OK


def cyclicAnalysis(dispTarList, ControlNode, numIncr, numCyclesPerDispTarget=2):
    
    ControlNodeDoF  = 1
    dForce          = 1 # The pushover curve is not dependent to the value of dForce
    
    tol         = 1e-4
    numIter     = 200
    
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
    for dispTarget in dispTarList:
        incr        = dispTarget/numIncr
        incrList                    = [incr, -incr, -incr, incr] * numCyclesPerDispTarget
        for incr in incrList:
            
            for tester in testerList:
                ops.test(tester, tol, numIter) # NormUnbalance, NormDispIncr, EnergyIncr, RelativeNormUnbalance, RelativeNormDispIncr, RelativeTotalNormDispIncr, RelativeEnergyIncr, FixedNumIter, NormDispAndUnbalance, NormDispOrUnbalance
                # ops.test('NormUnbalance', tol, numIter)
                # algorithm = 'KrylovNewton' # Linear, Newton, NewtonLineSearch, ModifiedNewton, KrylovNewton, SecantNewton, RaphsonNewton, PeriodicNewton, BFGS, Broyden
                
                for algorithm in algorithmList:
                    ops.algorithm(algorithm)  
                    #   integrator('DisplacementControl', nodeTag,     dof,            incr, numIter=1, dUmin=incr, dUmax=incr)
                    ops.integrator('DisplacementControl', ControlNode, ControlNodeDoF, incr)
                    ops.analysis('Static')
                    
                    # Run Analysis
                    #        analyze(numIncr=1, dt=0.0, dtMin=0.0, dtMax=0.0, Jd=0)
                    OK = ops.analyze(numIncr)
                    print(f"AnalyzeOutput = {OK}")
                    curD    = ops.nodeDisp(ControlNode, ControlNodeDoF)
                    print(f"\n\ndispTarget =\t{dispTarget:.4f}")
                    print(f"======>>> Current Displacement is {curD:.4f}")
                    print(f"tester:\t\t{tester}")
                    print(f"Algorithm:\t{algorithm}")
                    if OK == 0:
                        break
                    elif OK != 0:
                        print(f"\n=============== The algorithm {algorithm} failed to converge!!! ===============")
                        time.sleep(waitTime)
                        if tester == testerList[-1] and algorithm == algorithmList[-1]:
                            print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                            print("*!*!*!*!*!* The cyclic pushover analysis failed to converge!!! *!*!*!*!*!*!*!*")
                            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"); sys.exit()
                    
                if OK == 0:
                    break
                elif OK != 0:
                    print(f"\n=============== The tester {tester} failed to converge!!! ===============")
                    time.sleep(waitTime)
                




























