import os
import sys
import openseespy.opensees as ops
import eqsig
import numpy as np
import matplotlib.pyplot as plt


logIDA = 'logIDA.txt'; sys.stdout = open(logIDA, 'w')    
g = 9.81

def get_file_names(directory): # This functions returns a list containing the file names in the given directory
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def get_spectral_acceleration(filename, dt, selected_time):
    def read_ground_motion_record(filename):
        with open(filename, 'r') as file:
            data = file.readlines()
        # Read all numbers from each line
        ground_motion_record = [float(num) for line in data for num in line.split()]
        return np.array(ground_motion_record)
    a = read_ground_motion_record(filename)

    periods = np.linspace(0.001, 5, 500)  # compute the response for 100 periods between T=0.01s and 5.0s

    # record = eqsig.AccSignal(a * g, dt)
    record = eqsig.AccSignal(a * 1, dt)
    record.generate_response_spectrum(response_times=periods)

    times = record.response_times

    # Find the corresponding value on the vertical axis
    selected_sa = np.interp(selected_time, times, record.s_a)
    rec = filename[23:]
    if 1:
        bf, sub_fig = plt.subplots()
        sub_fig.plot(times, record.s_a, label=rec)
        plt.plot([selected_time, selected_time], [0, selected_sa], 'r--')
        plt.plot([0, selected_time], [selected_sa, selected_sa], 'r--')
        plt.legend()
        plt.show()
    
    return selected_sa

# filename    = "Input/GM/0.02000_01500_RSN825_CAPEMEND_CPM000.txt"
# T           = 1
# sa = get_spectral_acceleration(filename, T)
# print(sa)

recList     = get_file_names("Input/GM")
recList     = recList[38:39]
SaTarget    = 1.5 * 0.63 # MCE = 1.5*DBE
extraTime   = 0
numRecords  = len(recList)
for i_rec, rec in enumerate(recList):
    # SaGM        = SaGMList[i_rec]
    filePath    = f"Input/GM/{rec}" 
    T1          = 0.25
    dtGM        = float(rec[:7])
    NPTS        = int(rec[8:13])
    SaGM        = get_spectral_acceleration(filePath, dtGM, T1)
    
    Tmax        = NPTS*dtGM + extraTime
    # dtAnalysis  = dtGM/200 # it can't be greater than dt
    # numIncr     = int(Tmax/dtAnalysis)
    scaleFactor = SaTarget/SaGM*g
    scaleFactorList = [ 
                        # 0.1*scaleFactor, 
                        # 0.2*scaleFactor,
                        # 0.5*scaleFactor,
                        # 1.0*scaleFactor,
                        # 1.5*scaleFactor,
                        2.0*scaleFactor,
                        # 3.0*scaleFactor,
                        # 4.0*scaleFactor,
                        # 5.0*scaleFactor,
                        # 6.0*scaleFactor,
                        # 7.0*scaleFactor,
                        # 8.0*scaleFactor,
                        # 9.0*scaleFactor,
                        # 10.*scaleFactor,
                        ]
    for tag, scaleFactor in enumerate(scaleFactorList):
        print(f"\n{'#'*65}\nRunning record {i_rec+1:02}/{numRecords:02}: {rec} for Sa = {SaTarget}*g SF = {scaleFactor}\n{'#'*65}")
        ops.wipe()
        exec(open("MAIN.py").read())



sys.stdout.close()
sys.stdout = sys.__stdout__
































