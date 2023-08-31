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

exec(open("Input/inputDataAS.py").read())
# exec(open("Input/inputDataCPSWCF.py").read())

# Plastic Hinge Length Ratio (0.0 < PHLR < 1.0)
PHLR = 0.99

#=============================================================================
#    Define Variables
#=============================================================================
typeModel       = 'Nonlinear'                    # 'Linear', 'Nonlinear'
typeSection     = 'Box_Composite'            # 'Rectangular', 'I_Shaped', 'Box', 'Box_Composite'
typeEle         = 'forceBeamColumn'         # 'forceBeamColumn', 'dispBeamColumn'
typeMatSt       = 'ReinforcingSteel'        # Elastic, ElasticPP, Steel02, ReinforcingSteel
typeMatCt       = 'Concrete02'              # Elastic, ElasticPP, Concrete02
typeAlgorithm   = 'KrylovNewton'            # Linear, Newton, NewtonLineSearch, ModifiedNewton, KrylovNewton, SecantNewton, RaphsonNewton, PeriodicNewton, BFGS, Broyden
typeSystem      = 'UmfPack'                 # Only for cyclic: # BandGen, BandSPD, ProfileSPD, SuperLU, UmfPack, FullGeneral, SparseSYM, ('Mumps', '-ICNTL14', icntl14=20.0, '-ICNTL7', icntl7=7)
typeAnalysis    = ['cyclic']             # 'monotonic', 'cyclic'


numIncr         = 300 # number of increments per target displacement

# Monotonic Pushover Analysis
dispTarget      = 25.6 *inch

# Cyclic Loading Analysis
dispTarList     = [1, 1.05, 2, 5, 10] # if no unit is multiplied, then the units will be meters by default!!!


# Plotting Options:
plot_undefo     = True
plot_loaded     = True
plot_defo       = True
sfac            = 10
plot_anim_defo  = False
    
plot_Analysis   = True
plot_section    = False

vfo_display     = False
#=============================================================================
#    MAIN
#=============================================================================

for types in typeAnalysis:
    
    outputDir = f"Output/Pushover/{types}"
    os.makedirs(outputDir, exist_ok=True)
    
    # Build Model
    ops.wipe()
    ops.model('basic', '-ndm', 2, '-ndf', 3)
    tagSec = 1
    
    # Create the Fiber Section
    if typeSection == 'Rectangular':
        fib_sec = fs.makeSectionRect(tagSec, H, B, typeMatSt)
    elif typeSection == 'I_Shaped':
        fib_sec = fs.makeSectionI(tagSec, H, B, tw, tf, typeMatSt)
    elif typeSection == 'Box':
        fib_sec = fs.makeSectionBox(tagSec, H, B, tw, tf, typeMatSt)
    elif typeSection == 'Box_Composite':
        fib_sec = fs.makeSectionBoxComposite(tagSec, H_W, B_W, tw_W, tf_W, typeMatSt, typeMatCt)
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
        fm.buildCantileverN(L, tagSec, typeEle, PHLR)
        
    # Plot Model
    if plot_undefo == True:
        opv.plot_model()
    if vfo_display == True:
        vfo.createODB(model="BuildingModel")
        print('BuildingModel is created!')
        vfo.plot_model(model="BuildingModel", show_nodetags="yes",show_eletags="yes")
    
    # Run Analysis
    fa.gravity(Py)
    fr.getPushoverRecorders(outputDir)
    if types == 'monotonic':
        print(f"Monotonic Pushover Analysis Initiated at {time.time() - start_time}.")
        fa.pushoverDCF(dispTarget, numIncr, typeAlgorithm)
        print(f"\n\nMonotonic Pushover Analysis Finished at {time.time() - start_time}.")
        if plot_loaded == True:
            opv.plot_loads_2d(nep=17, sfac=False, fig_wi_he=False, fig_lbrt=False, fmt_model_loads={'color': 'black', 'linestyle': 'solid', 'linewidth': 1.2, 'marker': '', 'markersize': 1}, node_supports=True, truss_node_offset=0, ax=False)
        if plot_defo == True:
            sfac = opv.plot_defo()
            # opv.plot_defo(sfac)
    elif types == 'cyclic':
        print(f"Cyclic Pushover Analysis Initiated at {time.time() - start_time}.")
        fa.cyclicAnalysis(dispTarList, numIncr, typeAlgorithm, typeSystem)
        print(f"\n\nCyclic Pushover Analysis Finished at {time.time() - start_time}.")
        if plot_loaded == True:
            opv.plot_loads_2d(nep=17, sfac=False, fig_wi_he=False, fig_lbrt=False, fmt_model_loads={'color': 'black', 'linestyle': 'solid', 'linewidth': 1.2, 'marker': '', 'markersize': 1}, node_supports=True, truss_node_offset=0, ax=False)
    else:
        print("UNKNOWN Pushover Analysis type!!!");sys.exit()
    
    
#=============================================================================
#    Plot
#=============================================================================
    if plot_Analysis == True:
        fp.plotPushoverX(outputDir) 

end_time = time.time()
elapsed_time = end_time - start_time
print(f"\nElapsed time: {elapsed_time:.2f} seconds")

print("\nThe analysis was run successfully.")













