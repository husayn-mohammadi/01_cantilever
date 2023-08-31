import openseespy.opensees as ops

# exec(open("Input/inputData.py").read())

def gravity(Py):
    
    tagTSGravity    = 10
    # ops.timeSeries('Linear', tagTSGravity)
    ops.timeSeries('Constant', tagTSGravity)
    
    tagPtnGravity   = 10
    ops.pattern('Plain', tagPtnGravity, tagTSGravity)
    ops.load(3, 0.0, -abs(Py), 0.0)
    
    
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

def pushoverDCF(dispTarget, numIncr, algorithm='KrylovNewton'): # Linear, Newton, NewtonLineSearch, ModifiedNewton, KrylovNewton, SecantNewton, RaphsonNewton, PeriodicNewton, BFGS, Broyden
    
    ControlNode     = 3
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
    ops.test('NormDispIncr', tol, numIter)
    # ops.test('NormUnbalance', tol, numIter)
    ops.algorithm(algorithm)
    #   integrator('DisplacementControl', nodeTag,     dof,            incr, numIter=1, dUmin=incr, dUmax=incr)
    ops.integrator('DisplacementControl', ControlNode, ControlNodeDoF, incr)
    ops.analysis('Static')
    
    # Run Analysis
    #        analyze(numIncr=1, dt=0.0, dtMin=0.0, dtMax=0.0, Jd=0)
    OK = ops.analyze(numIncr)
    
    return OK


def cyclicAnalysis(dispTarList, numIncr, algorithm='Newton', system='UmfPack'):
    
    ControlNode     = 3
    ControlNodeDoF  = 1
    dForce          = 1 # The pushover curve is not dependent to the value of dForce
    
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
    ops.numberer('RCM') # Plain, RCM, AMD, ParallelPlain, ParallelRCM
    ops.system(system) # BandGen, BandSPD, ProfileSPD, SuperLU, UmfPack, FullGeneral, SparseSYM, ('Mumps', '-ICNTL14', icntl14=20.0, '-ICNTL7', icntl7=7)
    ops.test('NormDispIncr', tol, numIter) # NormUnbalance, NormDispIncr, EnergyIncr, RelativeNormUnbalance, RelativeNormDispIncr, RelativeTotalNormDispIncr, RelativeEnergyIncr, FixedNumIter, NormDispAndUnbalance, NormDispOrUnbalance
    # ops.test('NormUnbalance', tol, numIter)
    # algorithm = 'KrylovNewton' # Linear, Newton, NewtonLineSearch, ModifiedNewton, KrylovNewton, SecantNewton, RaphsonNewton, PeriodicNewton, BFGS, Broyden
    ops.algorithm(algorithm)  
    print(f"Algorithm: {algorithm}")
    # Run Analysis
    for dispTarget in dispTarList:
        
        incr        = dispTarget/numIncr
        numCyclesPerDispTarget      = 2
        incrList                    = [incr, -incr, -incr, incr] * numCyclesPerDispTarget
        for incr in incrList:
            
            #   integrator('DisplacementControl', nodeTag,     dof,            incr, numIter=1, dUmin=incr, dUmax=incr)
            ops.integrator('DisplacementControl', ControlNode, ControlNodeDoF, incr)
            ops.analysis('Static')
            
            #        analyze(numIncr=1, dt=0.0, dtMin=0.0, dtMax=0.0, Jd=0)
            ops.analyze(numIncr)




























