import matplotlib.pyplot as plt
# import opsvis            as opv
import numpy             as np
# from matplotlib.animation import FuncAnimation
exec(open("MAIN.py").readlines()[18]) # It SHOULD read and execute exec(open("Input/units    .py").read())
unitForce   = "kN" if kN==1 else "N"   if N==1  else "kip" if kip==1 else "lb"  
unitLength  = "m"  if m==1  else "cm"  if cm==1 else "mm"  if mm==1  else "in." if inch==1 else "ft" 

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
    fig.suptitle(f"Pushover Curve: {outputDir[16:-2]}")
    ax.set_xlabel(f'Displacement ({unitLength})')
    if unitForce=="kN":
        ax.set_ylabel('Shear (kN)')
        plt.plot(x, Vx, linewidth=0.8)
    elif unitForce=="N":
        ax.set_ylabel('Shear (kN)')
        plt.plot(x, Vx/1e3, linewidth=0.8)
    elif unitForce=="kip":
        ax.set_ylabel('Shear (kip)')
        plt.plot(x, Vx, linewidth=0.8)
    elif unitForce=="lb":
        ax.set_ylabel('Shear (kip)')
        plt.plot(x, Vx/1e3, linewidth=0.8, dpi=150)
    
    return x, Vx

def plotStressStrain(outputDir,tagEleList): 
    listFiberMat = ['fiberSt', 'fiberCt1', 'fiberCt2'] 
    n       = len(tagEleList)
    zero    = np.array([0.])
    
    fig, ax = plt.subplots(3, n, figsize=(8*n, 16))
    fig.suptitle("Stress-Strain Curve", fontsize=16)
    if unitForce == "N" or unitForce == "kN":
        [a.set_ylabel('Stress (MPa)') for a in ax] if n==1 else [a.set_ylabel('Stress (MPa)') for a in ax[:,0]]
    elif unitForce == "kip" or unitForce == "lb":
        [a.set_ylabel('Stress (ksi)') for a in ax] if n==1 else [a.set_ylabel('Stress (ksi)') for a in ax[:,0]]
        
    SS      = {}; Stress = {}; Strain = {}
    for j, tagEle in enumerate(tagEleList):
        
        ax[2].set_xlabel('Strain') if n==1 else ax[2,j].set_xlabel('Strain')
        SS[j] = {}; Stress[j] = {}; Strain[j] = {}
        for i, fiberMat in enumerate(listFiberMat):
            for k, item in enumerate(['top', 'mid', 'bot']):
                if fiberMat == "fiberCt2" and item == "mid":
                    continue 
                SSS             = np.loadtxt(f"{outputDir}/{fiberMat}_{item}.txt", delimiter= ' ')
                Stress[j][k]    = np.append(zero, SSS[:,2*j+0])
                Strain[j][k]    = np.append(zero, SSS[:,2*j+1])
                SS[j][k]        = np.column_stack((Strain[j][k], Stress[j][k]))
                np.savetxt(f"{outputDir}/StressStrain{j}_{fiberMat}_{item}.txt", SS[j][k])
                            
            if unitForce == "N":
                ax[i].plot(Strain[j][0], Stress[j][0]/1e6, color='blue', label='top', linewidth=0.8) if n==1 else ax[i,j].plot(Strain[j][0], Stress[j][0]/1e6, color='blue', label='top', linewidth=0.8) 
                if fiberMat != "fiberCt2" and item != "mid":
                    ax[i].plot(Strain[j][1], Stress[j][1]/1e6, color='gray', label='mid', linewidth=0.8) if n==1 else ax[i,j].plot(Strain[j][1], Stress[j][1]/1e6, color='gray', label='mid', linewidth=0.8) 
                ax[i].plot(Strain[j][2], Stress[j][2]/1e6, color='red',  label='bot', linewidth=0.8) if n==1 else ax[i,j].plot(Strain[j][2], Stress[j][2]/1e6, color='red',  label='bot', linewidth=0.8) 
            elif unitForce == "kN":
                ax[i].plot(Strain[j][0], Stress[j][0]/1e3, color='blue', label='top', linewidth=0.8) if n==1 else ax[i,j].plot(Strain[j][0], Stress[j][0]/1e3, color='blue', label='top', linewidth=0.8)
                if fiberMat != "fiberCt2" and item != "mid":
                    ax[i].plot(Strain[j][1], Stress[j][1]/1e3, color='gray', label='mid', linewidth=0.8) if n==1 else ax[i,j].plot(Strain[j][1], Stress[j][1]/1e3, color='gray', label='mid', linewidth=0.8)
                ax[i].plot(Strain[j][2], Stress[j][2]/1e3, color='red',  label='bot', linewidth=0.8) if n==1 else ax[i,j].plot(Strain[j][2], Stress[j][2]/1e3, color='red',  label='bot', linewidth=0.8)
            elif unitForce == "lb":
                ax[i].plot(Strain[j][0], Stress[j][0]/1e3, color='blue', label='top', linewidth=0.8) if n==1 else ax[i,j].plot(Strain[j][0], Stress[j][0]/1e3, color='blue', label='top', linewidth=0.8)
                if fiberMat != "fiberCt2" and item != "mid":
                    ax[i].plot(Strain[j][1], Stress[j][1]/1e3, color='gray', label='mid', linewidth=0.8) if n==1 else ax[i,j].plot(Strain[j][1], Stress[j][1]/1e3, color='gray', label='mid', linewidth=0.8)
                ax[i].plot(Strain[j][2], Stress[j][2]/1e3, color='red',  label='bot', linewidth=0.8) if n==1 else ax[i,j].plot(Strain[j][2], Stress[j][2]/1e3, color='red',  label='bot', linewidth=0.8)
            elif unitForce == "kip":
                ax[i].plot(Strain[j][0], Stress[j][0], color='blue',     label='top', linewidth=0.8) if n==1 else ax[i,j].plot(Strain[j][0], Stress[j][0], color='blue',     label='top', linewidth=0.8) 
                if fiberMat != "fiberCt2" and item != "mid":
                    ax[i].plot(Strain[j][1], Stress[j][1], color='gray',     label='mid', linewidth=0.8) if n==1 else ax[i,j].plot(Strain[j][1], Stress[j][1], color='gray',     label='mid', linewidth=0.8) 
                ax[i].plot(Strain[j][2], Stress[j][2], color='red',      label='bot', linewidth=0.8) if n==1 else ax[i,j].plot(Strain[j][2], Stress[j][2], color='red',      label='bot', linewidth=0.8) 
            ax[i].set_title(f"tagEle: {tagEle} | Material: {fiberMat}") if n==1 else ax[i,j].set_title(f"tagEle: {tagEle} | Material: {fiberMat}")
            ax[i].legend() if n==1 else ax[i,j].legend()
    plt.tight_layout()
    plt.show()
    
def plotNTHA(H, outputDir, tag):
    disp    = np.loadtxt(f"{outputDir}/disp{tag}.txt", delimiter= ' ')
    velo    = np.loadtxt(f"{outputDir}/velo{tag}.txt", delimiter= ' ')
    acce    = np.loadtxt(f"{outputDir}/acce{tag}.txt", delimiter= ' ')
    reac    = np.loadtxt(f"{outputDir}/R{tag}.txt", delimiter= ' ')
    
    t       = disp[:, 0]
    d       = disp[:, 1]/H
    v       = velo[:, 1]
    a       = acce[:, 1]
    Vx      = reac[:, 1]; Vy = reac[:, 2]; Mz = reac[:, 3]
    
    fig, ax = plt.subplots(4, 1, figsize=(10, 10), dpi=200)
    fig.suptitle("Dynamic Analysis Curves", fontsize=16)
    ax[3].set_xlabel('time (s)')
    ax[0].set_ylabel('drift');                  ax[0].plot(t, d, linewidth=0.8)
    ax[1].set_ylabel('velocity     (m/s)');     ax[1].plot(t, v, linewidth=0.8)
    ax[2].set_ylabel('acceleration (m/s^2)');   ax[2].plot(t, a, linewidth=0.8)
    ax[3].set_ylabel('reaction     (N)');       ax[3].plot(t, Vx, color='blue', label='Vx', linewidth=0.8); ax[3].plot(t, Vy, color='black', label='Vy', linewidth=0.8); ax[3].plot(t, Mz, color='red', label='Mz', linewidth=0.8); ax[3].legend()
    plt.tight_layout()
    plt.show()


def plotMomCurv(outputDir, tagEle, section, typeBuild):
    if typeBuild == "CantileverColumn":
        momenIndex = 1
    else:
        momenIndex = 2
    zero        = np.array([0.])
    # Store the section's Moment in an array
    momentTXT   = np.loadtxt(f"{outputDir}/moment{tagEle}.txt", delimiter= ' ')
    moment      = np.append(zero, momentTXT[:, momenIndex])
    Mpeak       = max(moment)
    Mpeak60perc = 0.6*Mpeak
    # Store the section's top and bottom strains in an array
    SSListTop   = np.loadtxt(f"{outputDir}/SS_top{tagEle}.txt", delimiter= ' ')
    SSListBot   = np.loadtxt(f"{outputDir}/SS_bot{tagEle}.txt", delimiter= ' ')
    # Calculate the curvature 
    StrainTop   = np.append(zero, SSListTop[:,1])
    StrainBot   = np.append(zero, SSListBot[:,1])
    h           = section.Hw + section.tw
    curvature   = ((StrainTop -StrainBot)
                   /h)
    curAtM60per = np.interp(Mpeak60perc, moment, curvature)
    EI          = Mpeak60perc /curAtM60per
    curAtMpeakE = 1/EI *Mpeak
    MomCurv     = np.column_stack((curvature, moment))
    np.savetxt(f"{outputDir}/MomentCurvature_{tagEle}.txt", MomCurv)
    
    fig, ax = plt.subplots()
    fig.suptitle(f"Momemnt-Curvature: {tagEle}")
    ax.set_xlabel(f'curvature (m^-1)')
    ax.set_ylabel('Moment (kN.m)')
    plt.plot(curvature, moment*N/kN, linewidth=0.8, label=f"M-c: Mpeak={Mpeak*N/kN:.1f} kN.m")
    plt.plot([curAtM60per, curAtM60per], [0, Mpeak60perc*N/kN], 'r--')        # Vertical Line
    plt.plot([0, curAtM60per], [Mpeak60perc*N/kN, Mpeak60perc*N/kN], 'r--')   # Horizontal Line
    plt.plot([0, curAtMpeakE], [0, Mpeak*N/kN], 'g--', label = f" EI = {EI/(kN*m**2):.1f} kN.m^2")                        # Horizontal Line
    plt.legend()
    plt.show()
    
    return(EI)
    













