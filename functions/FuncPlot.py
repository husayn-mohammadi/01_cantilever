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
    fig.suptitle(f"Pushover Curve: {outputDir[16:]}")
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
        plt.plot(x, Vx/1e3, linewidth=0.8)
    
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
    
    # return Strain, Stress

# def plot_fiber_section(fib_sec):
    
#     matcolor = ['y', 'b', 'r', 'g', 'm', 'k']
#     # matcolor = ['r', 'lightgrey', 'pink', 'gold', 'purple', 'orange', 'w']
#     opv.plot_fiber_section(fib_sec, matcolor=matcolor)
#     plt.axis('equal')
#     # plt.savefig('fibsec_rc.png')
    
#     plt.show()






# def plotPushoverX(outputDir):
#     x0 = np.array([0.])
#     Vx0 = np.array([0.])
    
#     fig, ax = plt.subplots()
#     fig.suptitle(f"Pushover Curve: {outputDir[16:]}")
#     ax.set_xlabel(f'Displacement ({unitLength})')
    
#     if unitForce == "kN":
#         ax.set_ylabel('Shear (kN)')
#     elif unitForce == "N":
#         ax.set_ylabel('Shear (kN)')
#     elif unitForce == "kip":
#         ax.set_ylabel('Shear (kip)')
#     elif unitForce == "lb":
#         ax.set_ylabel('Shear (kip)')
    
#     line, = ax.plot(x0, Vx0, linewidth=0.8)  # Initialize an empty plot
    
#     def update(frame):
#         try:
#             data = np.loadtxt(f"{outputDir}/Pushover.txt")
#             x = data[:, 0]
#             Vx = data[:, 1]
#             line.set_data(x, Vx)  # Update the plot with new data
#         except FileNotFoundError:
#             pass  # Handle the case where the file doesn't exist
        
#     ani = FuncAnimation(fig, update, blit=False, interval=100)  # Update the plot every 100 milliseconds
#     plt.show()

#     # Return empty arrays for x and Vx, as they are updated in real-time
#     return np.array([]), np.array([])
