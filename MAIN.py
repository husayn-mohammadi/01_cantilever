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
withShearLink   = False
exertGravityLoad= True
typeModel       = 'Nonlinear'               # 'Linear', 'Nonlinear'
typeBuild       = 'coupledWalls'        # 'CantileverColumn', 'ShearCritBeam', 'coupledWalls'
typeCB          = 'FSF'                     # 'FSF', 'FSW' (FSF = FlexureShearFlexure, FSW = FlexureShearWall)
# typeSection     = 'Box_Composite'           # 'Rectangular', 'I_Shaped', 'Box', 'Box_Composite'
typeEle         = 'dispBeamColumn'          # 'forceBeamColumn', 'dispBeamColumn'
typeAnalysis    = ['monotonic']             # 'monotonic', 'cyclic'

Lw              = Section['wall']['propWeb'][1] + 2*Section['wall']['propFlange'][1]
PHL             = 24 *inch                  # Plastic Hinge Length (0.0 < PHLR < L)
numSegWall      = 3                         # If numSegWall=0, the model will be built only with one linear elastic element connecting the base node to top node
numSegBeam      = 3
SBL             = 0.52 *m
# Monotonic Pushover Analysis
dispTarget      = 15.3 *inch

# Cyclic Pushover Analysis
dY              = n_story*17 *mm
CPD1            = 1                         # CPD = cyclesPerDisp; which should be an integer
CPD2            = 1
dispTarList     = [ 
                    *(CPD1*[dY/3]), *(CPD1*[2/3*dY]), *(CPD1*[dY]),   *(CPD1*[1.5*dY]), *(CPD1*[2*dY]),
                    *(CPD1*[3*dY]), *(CPD1*[4*dY]),   *(CPD1*[5*dY]), *(CPD2*[6*dY]),   *(CPD2*[7*dY]),
                    *(CPD2*[8*dY]), *(CPD2*[9*dY]),   
                    *(CPD2*[10*dY])
                   ]


# Plotting Options:
buildingWidth=10.; buildingHeight=7.
plot_undefo     = True
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
    
    outputDir = f"Output/Pushover/{types}"
    os.makedirs(outputDir, exist_ok=True)
    
    # Build Model
    ops.wipe()
    ops.model('basic', '-ndm', 2, '-ndf', 3)
            
    if typeModel == 'Linear':
        I   = 2
        A   = 1
        Es  = 29000*ksi
        fm.buildCantileverL(L, Es, I, A)
    else:
        if typeBuild == "CantileverColumn":
            P = 0 * kN
            tagNodeControl, tagNodeBase, tagEleListToRecord_wall, section = fm.buildCantileverN(L, P, PHL, numSegWall, typeEle, modelFoundation)
        elif typeBuild == 'coupledWalls':
            P = n_story * load['wall']
            tagNodeControl, tagNodeBase, buildingWidth, buildingHeight, coords, tagEleListToRecord_wall, tagNodeLoad, section = fm.coupledWalls(H_story_List, L_Bay_List, Lw, P, numSegBeam, numSegWall, PHL, SBL, withShearLink, typeCB, plot_section)
        else:
            tagNodeControl, tagNodeBase  = fm.buildShearCritBeam(L)
        
    # Plot Model
    if plot_undefo == True:
        opv.plot_model(node_labels=0, element_labels=0, fig_wi_he=(buildingWidth+10., buildingHeight+7.),
                       fmt_model={'color': 'blue', 'linestyle': 'solid', 'linewidth': 0.6, 'marker': '.', 'markersize': 3})
    
    # Run Analysis
    if exertGravityLoad == True:
        if typeBuild == 'coupledWalls':
            fa.gravity(load, tagNodeLoad)
        else:
            # Axial Force Capacity of Walls (Pno)
            Pno = section.Pno
            fa.gravity(ALR*Pno, tagNodeControl)
        
    fr.recordPushover(tagNodeControl, tagNodeBase, outputDir)
    Hw = section.Hw; tf = section.tf; Hc2 = section.Hc2
    coordsFiber = fr.recordStressStrain(outputDir, tagEleListToRecord_wall,  section)                   # tagMatSt=1
    if types == 'monotonic':
        start_time_monotonic = time.time()
        print("\n\n\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(f"Monotonic Pushover Analysis Initiated at {(start_time_monotonic - start_time):.0f}sec.")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n\n")
        fa.pushoverDCF(dispTarget, tagNodeControl, n_story)
        finish_time_monotonic = time.time()
        mins = int((finish_time_monotonic - start_time_monotonic)/60)
        secs = int((finish_time_monotonic - start_time_monotonic)%60)
        print("\n\n\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(f"Monotonic Pushover Analysis Finished in {mins}min+{secs}sec.")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n\n")
        if plot_loaded == True:
            opv.plot_loads_2d(nep=17, sfac=False, fig_wi_he=(buildingWidth+10., buildingHeight+7.), fig_lbrt=False, fmt_model_loads={'color': 'black', 'linestyle': 'solid', 'linewidth': 1.2, 'marker': '', 'markersize': 1}, node_supports=True, truss_node_offset=0, ax=False)
        if plot_defo == True:
            sfac = opv.plot_defo(fig_wi_he=(buildingWidth+10., buildingHeight+7.),
                                 #fmt_defo={'color': 'blue', 'linestyle': 'solid', 'linewidth': 0.6, 'marker': '.', 'markersize': 3}
                                 )
            # opv.plot_defo(sfac)
    elif types == 'cyclic':
        start_time_cyclic = time.time()
        print("\n\n\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(f"Cyclic Pushover Analysis Initiated at {(time.time() - start_time):.0f}sec.")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n\n")
        fa.cyclicAnalysis(dispTarList, tagNodeControl)
        finish_time_cyclic = time.time()
        mins = int((finish_time_cyclic - start_time_cyclic)/60)
        secs = int((finish_time_cyclic - start_time_cyclic)%60)
        print("\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(f"Cyclic Pushover Analysis Finished in {mins}min+{secs}sec.")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n\n")
        if plot_loaded == True:
            opv.plot_loads_2d(nep=17, sfac=False, fig_wi_he=(buildingWidth+10., buildingHeight+7.), fig_lbrt=False, fmt_model_loads={'color': 'black', 'linestyle': 'solid', 'linewidth': 1.2, 'marker': '', 'markersize': 1}, node_supports=True, truss_node_offset=0, ax=False)
    else:
        print("UNKNOWN Pushover Analysis type!!!");sys.exit()
    
    
#=============================================================================
#    Plot
#=============================================================================
    if plot_Analysis == True:
        fp.plotPushoverX(outputDir) 
    if plot_StressStrain == True:
        fp.plotStressStrain(outputDir,tagEleListToRecord_wall)

end_time        = time.time()
elapsed_time    = end_time - start_time
mins            = int(elapsed_time/60)
secs            = int(elapsed_time%60)
print(f"\nElapsed time: {mins}min+{secs}sec")
print("\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
print("The analysis was run successfully.")
print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")


if recordToLog == True:
    sys.stdout.close()
    sys.stdout = sys.__stdout__

ops.wipe()










