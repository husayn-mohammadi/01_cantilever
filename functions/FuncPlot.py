import matplotlib.pyplot as plt
import opsvis            as opv
import numpy             as np
exec(open("MAIN.py").readlines()[18]) # It SHOULD read and execute exec(open("Input/units    .py").read())
unitForce   = "kN" if kN==1 else "N"   if N==1  else "kip"
unitLength  = "m"  if m==1  else "cm"  if cm==1 else "mm" if mm==1 else "in." if inch==1 else "ft" 

def plotPushoverX(outputDir):
    
    disp    = np.loadtxt(f"{outputDir}/top_disp.txt", delimiter= ' ')
    # reac    = np.loadtxt(f"{outputDir}/reaction.txt", delimiter= ' ')
    
    x1       =  disp[:, 1]
    # Vx1      = -reac[:, 1]
    Vx1      =  disp[:, 0]
    
    x0      = np.array([0.])
    Vx0     = np.array([0.])
    
    x       = np.append(x0, x1)
    Vx      = np.append(Vx0, Vx1)
    
    x_Vx = np.column_stack((x, Vx))
    np.savetxt(f"{outputDir}/Pushover.txt", x_Vx)
    
    fig, ax = plt.subplots()
    fig.suptitle(f"Pushover Curve: {outputDir[16:]}")
    ax.set_ylabel(f'Shear ({unitForce})'); ax.set_xlabel(f'Displacement ({unitLength})')
    plt.tight_layout()
    plt.plot(x, Vx, linewidth=0.5)
    
    return x, Vx

def plotStressStrainMonotonic(outputDir, fiberMat):
    
    top     = np.loadtxt(f"{outputDir}/{fiberMat}_top.txt", delimiter= ' ')
    bot     = np.loadtxt(f"{outputDir}/{fiberMat}_bot.txt", delimiter= ' ')
    
    Stress  = np.append(np.flip(top[:,0]), bot[:,0])
    Strain  = np.append(np.flip(top[:,1]), bot[:,1])
       
    SS      = np.column_stack((Strain, Stress))
    np.savetxt(f"{outputDir}/Stress_Strain.txt", SS)
    
    fig, ax = plt.subplots()
    plt.plot(Strain, Stress)
    
    return Strain, Stress

def plotStressStrain(outputDir, fiberMat, TopOrBot):
    
    StressStrain    = np.loadtxt(f"{outputDir}/{fiberMat}_{TopOrBot}.txt", delimiter= ' ')
    
    Stress1         = StressStrain[:,0]
    Strain1         = StressStrain[:,1]
    zero            = np.array([0.])
    
    Stress          = np.append(zero, Stress1)
    Strain          = np.append(zero, Strain1)
    
    SS      = np.column_stack((Strain, Stress))
    np.savetxt(f"{outputDir}/StressStrain_{fiberMat}_{TopOrBot}.txt", SS)
    
    fig, ax = plt.subplots()
    plt.plot(Strain, Stress)
    
    return Strain, Stress

def plot_fiber_section(fib_sec):
    
    matcolor = ['y', 'b', 'r', 'g', 'm', 'k']
    # matcolor = ['r', 'lightgrey', 'pink', 'gold', 'purple', 'orange', 'w']
    opv.plot_fiber_section(fib_sec, matcolor=matcolor)
    plt.axis('equal')
    # plt.savefig('fibsec_rc.png')
    
    plt.show()


















































