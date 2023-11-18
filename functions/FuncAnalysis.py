import openseespy.opensees     as ops
import time
import sys
import random                  as rn
import winsound
# from colorama import Fore, Style # print(f"{Fore.YELLOW} your text {Style.RESET_ALL}")

waitTime        = 0.0
waitTime2       = 0.0
testerList      = ['EnergyIncr', 'NormUnbalance', 'NormDispIncr', ]#, 'RelativeNormUnbalance']
algorithmList   = [*(1*['KrylovNewton', 'RaphsonNewton', 'NewtonLineSearch']), 'KrylovNewton'] #, 'Linear', 'Newton', 'NewtonLineSearch', 'ModifiedNewton', 'KrylovNewton', 'SecantNewton', 'RaphsonNewton', 'PeriodicNewton', 'BFGS', 'Broyden'

# def create_list(n):
#     myList = list(range(n, 0, -1)) + list(range(2, n + 1))
#     return myList

def create_list(n1, n2):
    myList = list(range(n1, n2 - 1, -1)) + list(range(n2, n1 + 1))
    return myList

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


def pushoverDCF(dispTarget, tagNodeLoad, n_story): 
    t_beg           = time.time()
    dofNodeControl  = 1
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
    ops.system('BandGen')
    
    # numIncrList = [*(1*[20]), *(10*[15]), *(1*[20])]
    numIncrList = [dispTarget/incrMono] # if the length unit is m: dispTarget/0.001 makes each incr equal to 1 mm 
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
        for algorithm in algorithmList:
            ops.algorithm(algorithm)  
            
            for tester in testerList:
                ops.test(tester, tol, numIter)
                
                curD    = ops.nodeDisp(tagNodeControl, dofNodeControl)
                # print(f"curD = {curD}")
                remD    = dispTar - curD
                # print(f"remD = {remD}")
                numIncr = max(int(remD/dispFrac *numIncrList[iii]), 1)
                incr    = remD/numIncr
                
                while True:
                    #   integrator('DisplacementControl', nodeTag,     dof,            incr, numIter=1, dUmin=incr, dUmax=incr)
                    ops.integrator('DisplacementControl', tagNodeControl, dofNodeControl, incr)
                    ops.analysis('Static')
                    
                    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    print(f"--------------------------------------\nAlgorithm:\t{algorithm}")
                    print(f"--------------------------------------\ntester:\t\t{tester}\n--------------------------------------")
                    print(f"======>>> dispTarget\t\t\t\t= {dispTarget}")
                    print(f"======>>> dispTar({iii+1}/{numFrac})\t\t\t\t= {dispTar}")
                    print(f"======>>> Current   Displacement\t= {curD}")
                    print(f"======>>> Remaining Displacement\t= {remD}")
                    print(f"numIncr\t\t\t= {numIncr}")
                    print(f"Incr\t\t\t= {incr}")
                    
                    # Run Analysis
                    #        analyze(numIncr=1, dt=0.0, dtMin=0.0, dtMax=0.0, Jd=0)
                    OK      = ops.analyze(numIncr)
                    print(f"AnalyzeOutput\t= {OK}"); time.sleep(waitTime2)
                    curD    = ops.nodeDisp(tagNodeControl, dofNodeControl)
                    print(f"======>>> Current   Displacement\t= {curD}")
                    if OK == 0:
                        break
                    else:
                        print("==========\nAnalysis Failed!!\nReducing Incr:\n==========")
                        # print(f"{Fore.YELLOW}==========\nAnalysis Failed!!\nReducing Incr:\n=========={Style.RESET_ALL}")
                        curD    = ops.nodeDisp(tagNodeControl, dofNodeControl)
                        print(f"======>>> Current   Displacement\t= {curD}")
                        remD    = dispTar - curD
                        print(f"======>>> Remaining Displacement\t= {remD}")
                        numIncr = int(numIncr*1.5)
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
                    t_end           = time.time()
                    elapsed_time    = t_end - t_beg
                    mins            = int(elapsed_time/60)
                    secs            = int(elapsed_time%60)
                    print(f"\nElapsed time: {mins} min + {secs} sec")
                    winsound.Beep(1000, 1000)  # generate a 440Hz sound that lasts 500 milliseconds
                    # print(f"{Fore.YELLOW}\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print("*!*!*!*!*!* The monotonic pushover analysis failed to converge!!! *!*!*!*!*!*")
                    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"); sys.exit()
                    # print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{Style.RESET_ALL}"); sys.exit()
                    return OK
    # opv.plot_loads_2d(nep=17, sfac=False, fig_wi_he=False, fig_lbrt=False, fmt_model_loads={'color': 'black', 'linestyle': 'solid', 'linewidth': 1.2, 'marker': '', 'markersize': 1}, node_supports=True, truss_node_offset=0, ax=False)

    return OK


def cyclicAnalysis(dispList, tagNodeLoad):
    t_beg           = time.time()
    
    dofNodeControl  = 1
    if type(tagNodeLoad) == list:
        tagNodeControl  = tagNodeLoad[-1]
    else: 
        tagNodeControl  = tagNodeLoad
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
    ops.load(tagNodeControl, *[1, 0, 0])
    
    
    #  Define Analysis Options
    
    ops.wipeAnalysis()
    ops.constraints('Transformation')
    ops.numberer('RCM') # Plain, RCM, AMD, ParallelPlain, ParallelRCM
    ops.system('UmfPack') # BandGen, BandSPD, ProfileSPD, SuperLU, UmfPack, FullGeneral, SparseSYM, ('Mumps', '-ICNTL14', icntl14=20.0, '-ICNTL7', icntl7=7)
    
    # Run Analysis
    for dispIndex, disp in enumerate(dispList):
        print(f"\n\ndisp({dispIndex+1}/{len(dispList)})\t= {disp}"); time.sleep(waitTime)
        dispTargetList = [disp, 0, -disp, 0]
        for index, dispTarget in enumerate(dispTargetList):
            curD        = ops.nodeDisp(tagNodeControl, dofNodeControl)
            delta       = dispTarget - curD
            # print (f"delta = {delta}")
            # numIncrList = [*(10*[2])] #[*(1*[4]), *(5*[3]), *(15*[2]), *(20*[1]), *(15*[2]), *(5*[3]), *(1*[4])] # 
            # numIncrList = [*(int(10 * (disp/dispList[-1]) + 4)*[2])] #[*(1*[4]), *(5*[3]), *(15*[2]), *(20*[1]), *(15*[2]), *(5*[3]), *(1*[4])] # 
            # numIncrList = [int(1 *13*disp/dispList[-1]) + 4] #[*(1*[4]), *(5*[3]), *(15*[2]), *(20*[1]), *(15*[2]), *(5*[3]), *(1*[4])] # 
            # n1          = int(10 * (disp/dispList[-1]) + 4)
            # n2          = int(5  * (disp/dispList[-1]) + 1)
            # print(f"n1 = {n1} and n2 = {n2}")
            # numIncrList = create_list(n1, n2)
            numIncrList = [disp/incrCycl] # if the length unit is m: dispTarget/0.001 makes each incr equal to 1 mm 
            numFrac     = len(numIncrList)
            dispFrac    = delta/numFrac
            # print(f"dispFrac = {dispFrac}")
            for  iii in range(0, numFrac):
                numIncr = numIncrList[iii]
                # print(f"\nnumIncr\t\t\t= {numIncr}")
                incr            = dispFrac/numIncr
                # print(f"curD = {curD}")
                dispTar         = curD + dispFrac
                # print(f"dispTar = {dispTar}")
                for indexAlgorithm, algorithm in enumerate(algorithmList):
                    ops.algorithm(algorithm) 
                    
                    for tester in testerList:
                        ops.test(tester, tol, numIter)
                        
                        curD    = ops.nodeDisp(tagNodeControl, dofNodeControl)
                        # print(f"curD = {curD}")
                        remD    = dispTar - curD
                        # print(f"remD = {remD}")
                        numIncr = max(int(remD/dispFrac *numIncrList[iii]), 1)
                        incr    = remD/numIncr
                        
                        ran = 200 if (algorithm==algorithmList[-1] and indexAlgorithm!=0) else 50 if (tester=='NormDispIncr' or tester=='EnergyIncr') else 10 
                        for i in range(ran):
                            print(f"Iteration {i}")
                            #   integrator('DisplacementControl', nodeTag,        dof,            incr, numIter=1, dUmin=incr, dUmax=incr)
                            ops.integrator('DisplacementControl', tagNodeControl, dofNodeControl, incr)
                            ops.analysis('Static') 
                            
                            print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                            print(f"disp({dispIndex+1}/{len(dispList)})\t= {disp}")
                            print(f"--------------------------------------\nAlgorithm:\t{algorithm}")
                            print(f"--------------------------------------\ntester:\t\t{tester}\n--------------------------------------")
                            print(f"======>>> dispTarget\t\t\t\t= {dispTarget}")
                            print(f"======>>> dispTar({iii+1}/{numFrac})\t\t\t\t= {dispTar}")
                            print(f"======>>> Current   Displacement\t= {curD}")
                            print(f"======>>> Remaining Displacement\t= {remD}")
                            print(f"numIncr\t\t\t= {numIncr}")
                            print(f"Incr\t\t\t= {incr}")
                            
                            
                            
                            # Run Analysis
                            #        analyze(numIncr=1, dt=0.0, dtMin=0.0, dtMax=0.0, Jd=0)
                            OK      = ops.analyze(numIncr)
                            print(f"AnalyzeOutput\t= {OK}"); time.sleep(waitTime2)
                            curD    = ops.nodeDisp(tagNodeControl, dofNodeControl)
                            print(f"======>>> Current   Displacement\t= {curD}")
                            if OK == 0:
                                break
                            else:
                                # print(f"{Fore.YELLOW}==========\nAnalysis Failed!!\nReducing Incr:\n=========={Style.RESET_ALL}")
                                print("==========\nAnalysis Failed!!\nReducing Incr:\n==========")
                                curD    = ops.nodeDisp(tagNodeControl, dofNodeControl)
                                print(f"======>>> Current   Displacement\t= {curD}")
                                remD    = dispTar - curD
                                print(f"======>>> Remaining Displacement\t= {remD}")
                                # numIncr = int(numIncr*3)
                                if numIncr <= 10000:
                                    numIncr = int(numIncr*2)
                                else:
                                    numIncr = rn.randint(5, 10000)
                                print(f"numIncr\t\t\t= {numIncr}")
                                incr    = remD/numIncr
                                print(f"Incr\t\t\t= {incr}")
                                time.sleep(waitTime)
                                # if numIncr >= 10000:
                                #     print("\nIncrement size is too small!!!")
                                #     time.sleep(waitTime)
                                #     break
                        
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
                        if tester == testerList[-1] and indexAlgorithm == len(algorithmList)-1:
                            t_end           = time.time()
                            elapsed_time    = t_end - t_beg
                            mins            = int(elapsed_time/60)
                            secs            = int(elapsed_time%60)
                            print(f"\nElapsed time: {mins} min + {secs} sec")
                            winsound.Beep(1000, 1000)  # generate a 440Hz sound that lasts 500 milliseconds
                            # print(f"{Fore.YELLOW}\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                            print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                            print("*!*!*!*!*!* The cyclic pushover analysis failed to converge!!! *!*!*!*!*!*")
                        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"); sys.exit()
                            # print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{Style.RESET_ALL}"); sys.exit()
                            return OK
                    
            
    return OK

                




























