import time
start_time = time.time()
import os
import sys
import openseespy.opensees     as ops
import opsvis                  as opv
import vfo.vfo                 as vfo
import functions.FuncSection   as fs
import functions.FuncModel     as fm
import functions.FuncAnalysis  as fa
import functions.FuncRecorders as fr
import functions.FuncPlot      as fp


#=============================================================================
#    Input File
#=============================================================================

exec(open("Input/unitsSI_kN.py").read())       # This determines the OUTPUT units: unitsUS.py/unitsSI.py
exec(open("Input/inputData.py").read())
exec(open("Input/materialParameters.py").read())

#=============================================================================
#    Define Variables
#=============================================================================
# Modeling Options
recordToLog     = True                      # True, False
modelFoundation = True
typeModel       = 'Nonlinear'               # 'Linear', 'Nonlinear'
typeBuild       = 'CantileverColumn'        # 'CantileverColumn', 'ShearCritBeam', 'coupledWalls'
typeSection     = 'Box_Composite'           # 'Rectangular', 'I_Shaped', 'Box', 'Box_Composite'
typeEle         = 'dispBeamColumn'          # 'forceBeamColumn', 'dispBeamColumn'
typeMatSt       = 'ReinforcingSteel'        # Elastic, ElasticPP, Steel02, ReinforcingSteel
typeMatCt       = 'Concrete02'              # Elastic, ElasticPP, Concrete02
typeAnalysis    = ['cyclic']             # 'monotonic', 'cyclic'

NfibeY          = 10                        # Number of Fibers along Y-axis

H_story_List    = [3.*m, *(2*[2.*m])]       # [Hstory1, *((numStories-1)*[HstoryTypical])]
L_Bay_List      = [7.*m, 6.*m, 5.*m]        # [*LBays]
Lw              = Hw
PHL             = 24 *inch                  # Plastic Hinge Length (0.0 < PHLR < L)
numSegWall      = 3                         # If numSegWall=0, the model will be built only with one linear elastic element connecting the base node to top node
numSegBeam      = 4
# Monotonic Pushover Analysis
dispTarget      = 10.5 *cm

# Cyclic Pushover Analysis
dY              = 12 *mm
CPD1            = 1                         # CPD = cyclesPerDisp; which should be an integer
CPD2            = 1
dispTarList     = [ *(CPD1*[dY/3]), *(CPD1*[2/3*dY]), *(CPD1*[dY]),   *(CPD1*[1.5*dY]), *(CPD1*[2*dY]),
                    *(CPD1*[3*dY]), *(CPD1*[4*dY]),   *(CPD1*[5*dY]), *(CPD2*[6*dY]),   *(CPD2*[7*dY]),
                    *(CPD2*[8*dY]), *(CPD2*[9*dY]),   *(CPD2*[10*dY])
                   ]


# Plotting Options:
plot_undefo     = True
plot_loaded     = True
plot_defo       = True
sfac            = 10
plot_anim_defo  = False
    
plot_Analysis   = True
plot_section    = True

vfo_display     = False
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
    
    # Create the Fiber Section
    tagSec = 1
    if typeSection == 'Rectangular':
        fib_sec = fs.makeSectionRect(tagSec, Hw, tc, typeMatSt, NfibeY*3) # Use the parameters of Concrete Core tc and Hw
    elif typeSection == 'I_Shaped':
        fib_sec = fs.makeSectionI(tagSec, Hw, Bf, tw, tf, typeMatSt, NfibeY)
    elif typeSection == 'Box':
        fib_sec = fs.makeSectionBox(tagSec, Hw, Bf, tw, tf, tc, typeMatSt, NfibeY)
    elif typeSection == 'Box_Composite':
        fib_sec= fs.makeSectionBoxComposite(tagSec, Hw, Bf, tw, tf, tc, Hc1, typeMatSt, typeMatCt, NfibeY)
    else:
        print("UNKNOWN fiber section type!!!");sys.exit()
        
    # Plot the fiber section
    if plot_section == True:
        fp.plot_fiber_section(fib_sec)
        
    if typeModel == 'Linear':
        I   = 2
        A   = 1
        Es  = 29000*ksi
        fm.buildCantileverL(L, Es, I, A)
    else:
        if typeBuild == "CantileverColumn":
            ControlNode, BaseNode = fm.buildCantileverN(tagSec, L, PHL, numSegWall, typeEle, modelFoundation)
        elif typeBuild == 'coupledWalls':
            ControlNode, BaseNode, buildingWidth, buildingHeight, coords  = fm.coupledWalls(H_story_List, L_Bay_List, Lw, tagSec, numSegBeam, numSegWall, PHL)
        else:
            ControlNode, BaseNode  = fm.buildShearCritBeam(tagSec, L)
        
    # Plot Model
    if plot_undefo == True:
        opv.plot_model(node_labels=0, element_labels=0)
    if vfo_display == True:
        vfo.createODB(model="BuildingModel")
        print('BuildingModel is created!')
        vfo.plot_model(model="BuildingModel", show_nodetags="yes",show_eletags="yes")
    
    # Run Analysis
    Pno = 0.85*(A_Composite_Ct1*abs(fpc) + A_Composite_Ct2*abs(fpcc)) + (A_Composite_St1*abs(Fy1) + A_Composite_St2*abs(Fy2))
    fa.gravity(ALR*Pno, ControlNode)
    fr.recordPushover(ControlNode, BaseNode, outputDir)
    coordsFiberSt = fr.recordStressStrain(outputDir, "fiberSt",  1, Hw+tf,  tf, NfibeY)                   # tagMatSt=1
    coordsFiberCt2= fr.recordStressStrain(outputDir, "fiberCt2", 4, Hw   ,  tf, NfibeY*int(Hw/tf/10))     # tagMatCt2=4
    coordsFiberCt1= fr.recordStressStrain(outputDir, "fiberCt1", 3, Hw-Hc2, tf, NfibeY*int(Hw/tf/10))     # tagMatCt1=3
    if types == 'monotonic':
        start_time_monotonic = time.time()
        print("\n\n\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(f"Monotonic Pushover Analysis Initiated at {(start_time_monotonic - start_time):.0f}sec.")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n\n")
        fa.pushoverDCF(dispTarget, ControlNode)
        finish_time_monotonic = time.time()
        mins = int((finish_time_monotonic - start_time_monotonic)/60)
        secs = int((finish_time_monotonic - start_time_monotonic)%60)
        print("\n\n\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(f"Monotonic Pushover Analysis Finished in {mins}min+{secs}sec.")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n\n")
        if plot_loaded == True:
            opv.plot_loads_2d(nep=17, sfac=False, fig_wi_he=False, fig_lbrt=False, fmt_model_loads={'color': 'black', 'linestyle': 'solid', 'linewidth': 1.2, 'marker': '', 'markersize': 1}, node_supports=True, truss_node_offset=0, ax=False)
        if plot_defo == True:
            sfac = opv.plot_defo()
            # opv.plot_defo(sfac)
    elif types == 'cyclic':
        start_time_cyclic = time.time()
        print("\n\n\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(f"Cyclic Pushover Analysis Initiated at {(time.time() - start_time):.0f}sec.")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n\n")
        fa.cyclicAnalysis(dispTarList, ControlNode)
        finish_time_cyclic = time.time()
        mins = int((finish_time_cyclic - start_time_cyclic)/60)
        secs = int((finish_time_cyclic - start_time_cyclic)%60)
        print("\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print(f"Cyclic Pushover Analysis Finished in {mins}min+{secs}sec.")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n\n")
        if plot_loaded == True:
            opv.plot_loads_2d(nep=17, sfac=False, fig_wi_he=False, fig_lbrt=False, fmt_model_loads={'color': 'black', 'linestyle': 'solid', 'linewidth': 1.2, 'marker': '', 'markersize': 1}, node_supports=True, truss_node_offset=0, ax=False)
    else:
        print("UNKNOWN Pushover Analysis type!!!");sys.exit()
    
    
#=============================================================================
#    Plot
#=============================================================================
    if plot_Analysis == True:
        fp.plotPushoverX(outputDir) 
        fp.plotStressStrain(outputDir, 'fiberSt',  'top')
        fp.plotStressStrain(outputDir, 'fiberSt',  'bot')
        fp.plotStressStrain(outputDir, 'fiberCt1', 'top')
        fp.plotStressStrain(outputDir, 'fiberCt1', 'bot')
        fp.plotStressStrain(outputDir, 'fiberCt2', 'top')
        fp.plotStressStrain(outputDir, 'fiberCt2', 'bot')

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












