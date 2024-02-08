import matplotlib.pyplot as plt
import numpy             as np
import os
from scipy.interpolate import interp1d

exec(open("MAIN.py").readlines()[18]) # It SHOULD read and execute exec(open("Input/units    .py").read())
unitForce   = "kN" if kN==1 else "N"   if N==1  else "kip" if kip==1 else "lb"  
unitLength  = "m"  if m==1  else "cm"  if cm==1 else "mm"  if mm==1  else "in." if inch==1 else "ft" 

def plotPushoverX(outputDir):
    
    disp    = np.loadtxt(f"{outputDir}/Pushover.txt", delimiter= ' ')
    
    x       =  disp[:, 0]
    Vx      =  disp[:, 1]
    VxMax   = max(Vx)
    Vx08Max = 0.8*VxMax
    # indices = [i for i, val in enumerate(Vx) if val == min(Vx, key=lambda k: abs(k - Vx08Max))]
    
    # Interpolate the pushover curve
    # interpolate_pushover = interp1d(x, Vx, kind='cubic')

    # Find the roots of the difference between the pushover curve and the horizontal line
    # roots = np.roots(interpolate_pushover(x) - Vx08Max)

    # Filter out the real roots that are within the range of x
    # intersection_points = [(root, interpolate_pushover(root)) for root in roots if min(x) <= root <= max(x)]
    
    fig, ax = plt.subplots()
    fig.suptitle(f"Pushover Curve: {outputDir[-3:]}")
    ax.set_xlabel(f'Displacement ({unitLength})')
    if unitForce == "kN":
        ax.set_ylabel('Shear (kN)')
        plt.plot(x, Vx, linewidth=0.8)
        plt.axhline(y=Vx08Max, color='r', linestyle='--', label=f'Vx08Max = {Vx08Max} kN')
    elif unitForce == "N":
        ax.set_ylabel('Shear (kN)')
        plt.plot(x, Vx / 1e3, linewidth=0.8)
        plt.axhline(y=Vx08Max / 1e3, color='r', linestyle='--', label=f'Vx08Max = {Vx08Max / 1e3} kN')
    elif unitForce == "kip":
        ax.set_ylabel('Shear (kip)')
        plt.plot(x, Vx, linewidth=0.8)
        plt.axhline(y=Vx08Max, color='r', linestyle='--', label=f'Vx08Max = {Vx08Max} kip')
    elif unitForce == "lb":
        ax.set_ylabel('Shear (kip)')
        plt.plot(x, Vx / 1e3, linewidth=0.8)
        plt.axhline(y=Vx08Max / 1e3, color='r', linestyle='--', label=f'Vx08Max = {Vx08Max / 1e3} kip')


    # for point in intersection_points:
    #     plt.scatter(*point, color='g', marker='o', label='Intersection Point')

    plt.legend()
    # plt.savefig(f"{outputDir}/Pushover_Plot.png", dpi=200)
    plt.show()
    
    # return intersection_points

outputDir = "Output/Pushover/monotonic/pushoverSeriesPlots"

for i in range(1, 145):
    out = f"{outputDir}/{i:03}"
    if os.path.exists(out) and os.path.exists(f"{out}/Pushover.txt"):
        points = plotPushoverX(out)
    else: 
        print(f"The directory {out} or file {out}/Pushover.txt does not exist.")
        continue



























