import matplotlib.pyplot as plt
import opsvis            as opv
import numpy             as np

def plotPushoverX(outputDir):
    
    disp    = np.loadtxt(f"{outputDir}/top_disp.txt", delimiter= ' ')
    reac    = np.loadtxt(f"{outputDir}/reaction.txt", delimiter= ' ')
    
    x1       =  disp[:, 1]
    Vx1      = -reac[:, 1]
    # Vx1      = -disp[:, 0]
    
    x0      = np.array([0.])
    Vx0     = np.array([0.])
    
    x       = np.append(x0, x1)
    Vx      = np.append(Vx0, Vx1)
    
    x_Vx = np.column_stack((x, Vx))
    np.savetxt(f"{outputDir}/graph.txt", x_Vx)
    
    fig, ax = plt.subplots()
    plt.plot(x, Vx)
    
    return x, Vx


def plot_fiber_section(fib_sec):
    
    matcolor = ['r', 'lightgrey', 'gold', 'w', 'w', 'w']
    opv.plot_fiber_section(fib_sec, matcolor=matcolor)
    plt.axis('equal')
    # plt.savefig('fibsec_rc.png')
    
    plt.show()


















































