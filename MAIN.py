import time
start_time = time.time()
import os
import sys
import openseespy.opensees     as ops
import opsvis                  as opv
import functions.FuncModel     as fm
import functions.FuncAnalysis  as fa
import functions.FuncRecorders as fr
import functions.FuncPlot      as fp
import winsound



#=============================================================================
#    Input File
#=============================================================================

exec(open("Input/unitsSI.py").read())       # This determines the OUTPUT units: unitsUS.py/unitsSI.py
exec(open("Input/inputData.py").read())
# exec(open("Input/materialParameters.py").read())
ops.logFile("logFile.txt")
#=============================================================================
#    Define Variables
#=============================================================================
# Modeling Options
recordToLog     = True                      # True, False
modelFoundation = True
rotSpring       = True
exertGravityLoad= True
typeBuild       = 'CantileverColumn'            # 'CantileverColumn', 'coupledWalls', 'buildBeam', 'ShearCritBeam'
typeCB          = 'discritizedBothEnds'     # 'discretizedAllFiber', 'FSF', 'FSW', discritizedBothEnds (FSF = FlexureShearFlexure, FSW = FlexureShearWall)
typeAnalysis    = ['monotonic']             # 'monotonic', 'cyclic'

Lw              = Section['wall']['propWeb'][1] + 2*Section['wall']['propFlange'][1]
PHL_wall        = 2/3 * Section['wall']['propWeb'][1]
PHL_beam        = 2/3 * Section['beam']['propWeb'][1]
numSegWall      = 3                         # If numSegWall=0, the model will be built only with one linear elastic element connecting the base node to top node
numSegBeam      = 3
SBL             = 0.3 *m                   # Length of Shear Link (Shear Beam)
# Monotonic Pushover Analysis
incrMono        = 0.5 *mm
dispTarget      = 1 *cm
# Cyclic Pushover Analysis
incrCycl        = incrMono
dY              = 38 *mm
CPD1            = 2                         # CPD = cyclesPerDisp; which should be an integer
CPD2            = 1
dispTarList     = [ 
                    *(CPD1*[0.5 *dY]),
                    *(CPD1*[1.0 *dY]),
                    *(CPD1*[1.5 *dY]),
                    *(CPD1*[2.0 *dY]),
                    # *(CPD1*[2.5 *dY]),
                    # *(CPD1*[3.0 *dY]),
                    # *(CPD1*[3.5 *dY]),
                    ]

# dispTarList     = [ 
#                     *(CPD1*[dY/3]), *(CPD1*[2/3*dY]), *(CPD1*[dY]),   *(CPD1*[1.5*dY]), *(CPD1*[2*dY]),
#                     *(CPD1*[3*dY]), *(CPD1*[4*dY]),   *(CPD1*[5*dY]), *(CPD2*[6*dY]),   *(CPD2*[7*dY]),
#                     *(CPD2*[8*dY]), 
#                     *(CPD2*[9*dY]),   
#                     *(CPD2*[10*dY])
#                     ]

# Plotting Options:
buildingWidth =10.; buildingHeight =7.
buildingWidth1=20.; buildingHeight1=17.
plot_undefo     = False
plot_loaded     = True
plot_defo       = True
sfac            = 10
    
plot_Analysis   = True
plot_StressStrain=True
plot_section    = False
#=============================================================================
#    MAIN
#=============================================================================

if recordToLog == True:
    logFile = 'log.txt'; sys.stdout = open(logFile, 'w')    

for types in typeAnalysis:
    
    outputDir = f"Output/Pushover/{types}"; outputDirWalls = f"Output/Pushover/{types}/wall"; outputDirBeams = f"Output/Pushover/{types}/beams" 
    os.makedirs(outputDir, exist_ok=True);  os.makedirs(outputDirWalls, exist_ok=True);       os.makedirs(outputDirBeams, exist_ok=True)
    
    # Build Model
    ops.wipe()
    ops.model('basic', '-ndm', 2, '-ndf', 3)
            
    if typeBuild == "CantileverColumn":
        # Py = 1 * kN
        tagNodeControl, tagNodeBase, tagEleListToRecord_wall, wall = fm.buildCantileverN(L, Py, PHL_wall, numSegWall, modelFoundation)
        fa.analyzeEigen(1)
    elif typeBuild == 'buildBeam':
        tagNodeControl, tagNodeBase, tagEleListToRecord_wall, wall = fm.buildBeam(L, PHL_beam, numSegBeam, rotSpring)
    elif typeBuild == 'coupledWalls':
        P = n_story * load['wall']
        tagNodeControl, tagNodeBase, buildingWidth, buildingHeight, coords, wall, tagEleListToRecord_wall, beam, tagEleListToRecord_beam, tagNodeLoad = fm.coupledWalls(H_story_List, L_Bay_List, Lw, P, load, numSegBeam, numSegWall, PHL_wall, PHL_beam, SBL, typeCB, plot_section, modelFoundation, rotSpring)
        fa.analyzeEigen(n_story)
    else:
        tagNodeControl, tagNodeBase  = fm.buildShearCritBeam(L)
        
    # Plot Model
    if plot_undefo == True:
        opv.plot_model(node_labels=0, element_labels=1, fig_wi_he=(buildingWidth+buildingWidth1, buildingHeight+buildingHeight1),
                       fmt_model={'color': 'blue', 'linestyle': 'solid', 'linewidth': 0.6, 'marker': '.', 'markersize': 3})
    
    # Run Analysis
    if exertGravityLoad == True:
        if typeBuild == 'coupledWalls':
            fa.gravity(load, tagNodeLoad)
        elif typeBuild == 'CantileverColumn':
            # Axial Force Capacity of Walls (Pno)
            Pno = wall.Pno
            fa.gravity(ALR*Pno, tagNodeControl)
        
    fr.recordPushover(tagNodeControl, tagNodeBase, outputDir)
    Hw = wall.Hw; tf = wall.tf; Hc2 = wall.Hc2
    if typeBuild == "CantileverColumn" or typeBuild == "buildBeam":
        fr.recordStressStrain(outputDirWalls, tagEleListToRecord_wall,  wall)
    elif typeBuild == "coupledWalls":
        fr.recordStressStrain(outputDirWalls, tagEleListToRecord_wall,  wall)
        fr.recordStressStrain(outputDirBeams, tagEleListToRecord_beam,  beam)
    if types == 'monotonic':
        start_time_monotonic = time.time()
        print("\n\n\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(f"Monotonic Pushover Analysis Initiated at {(start_time_monotonic - start_time):.0f}sec.")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n\n")
        fa.pushoverDCF(dispTarget, incrMono, tagNodeControl, n_story)
        finish_time_monotonic = time.time()
        mins = int((finish_time_monotonic - start_time_monotonic)/60)
        secs = int((finish_time_monotonic - start_time_monotonic)%60)
        print("\n\n\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(f"Monotonic Pushover Analysis Finished in {mins}min+{secs}sec.")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n\n")
        if plot_loaded == True:
            opv.plot_loads_2d(nep=17, sfac=False, fig_wi_he=(buildingWidth+buildingWidth1, buildingHeight+buildingHeight1), fig_lbrt=False, fmt_model_loads={'color': 'black', 'linestyle': 'solid', 'linewidth': 1.2, 'marker': '', 'markersize': 1}, node_supports=True, truss_node_offset=0, ax=False)
        if plot_defo == True:
            sfac = opv.plot_defo(fig_wi_he=(buildingWidth+buildingWidth1, buildingHeight+buildingHeight1),
                                 #fmt_defo={'color': 'blue', 'linestyle': 'solid', 'linewidth': 0.6, 'marker': '.', 'markersize': 3}
                                 )
            # opv.plot_defo(sfac)
    elif types == 'cyclic':
        start_time_cyclic = time.time()
        print("\n\n\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(f"Cyclic Pushover Analysis Initiated at {(time.time() - start_time):.0f}sec.")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n\n")
        fa.cyclicAnalysis(dispTarList, incrCycl, tagNodeControl)
        finish_time_cyclic = time.time()
        mins = int((finish_time_cyclic - start_time_cyclic)/60)
        secs = int((finish_time_cyclic - start_time_cyclic)%60)
        print("\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(f"Cyclic Pushover Analysis Finished in {mins}min+{secs}sec.")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n\n")
        if plot_loaded == True:
            opv.plot_loads_2d(nep=17, sfac=False, fig_wi_he=(buildingWidth+buildingWidth1, buildingHeight+buildingHeight1), fig_lbrt=False, fmt_model_loads={'color': 'black', 'linestyle': 'solid', 'linewidth': 1.2, 'marker': '', 'markersize': 1}, node_supports=True, truss_node_offset=0, ax=False)
        if plot_defo == True:
            sfac = opv.plot_defo(fig_wi_he=(buildingWidth+buildingWidth1, buildingHeight+buildingHeight1),
                                 #fmt_defo={'color': 'blue', 'linestyle': 'solid', 'linewidth': 0.6, 'marker': '.', 'markersize': 3}
                                 )
    else:
        print("UNKNOWN Pushover Analysis type!!!");sys.exit()
    

    ops.wipe()
#=============================================================================
#    Plot
#=============================================================================
    if plot_Analysis == True:
        fp.plotPushoverX(outputDir) 
    if plot_StressStrain == True:
        if typeBuild == "CantileverColumn" or typeBuild == "buildBeam":
            fp.plotStressStrain(outputDirWalls,tagEleListToRecord_wall)
        elif typeBuild == 'coupledWalls':
            fp.plotStressStrain(outputDirWalls,tagEleListToRecord_wall)
            fp.plotStressStrain(outputDirBeams,tagEleListToRecord_beam)

end_time        = time.time()
elapsed_time    = end_time - start_time
mins            = int(elapsed_time/60)
secs            = int(elapsed_time%60)
print(f"\nElapsed time: {mins} min + {secs} sec")
print("\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
print("The analysis was run successfully.")
print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")


if recordToLog == True:
    sys.stdout.close()
    sys.stdout = sys.__stdout__

winsound.Beep(1000, 300)  # generate a 440Hz sound that lasts 500 milliseconds
winsound.Beep(1000, 300)







