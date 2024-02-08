import numpy as np
import matplotlib.pyplot as plt
import eqsig

def read_ground_motion_record(filename):
    with open(filename, 'r') as file:
        data = file.readlines()
    # Read all numbers from each line
    ground_motion_record = [float(num) for line in data for num in line.split()]
    return np.array(ground_motion_record)

def get_spectral_acceleration(filename, selected_time):
    a = read_ground_motion_record(filename)

    dt = 0.02  # time step of acceleration time series
    periods = np.linspace(0.0001, 5, 500)  # compute the response for 100 periods between T=0.01s and 5.0s

    record = eqsig.AccSignal(a * 9.8, dt)
    record.generate_response_spectrum(response_times=periods)

    times = record.response_times

    # Find the corresponding value on the vertical axis
    selected_sa = np.interp(selected_time, times, record.s_a)
    
    if 1:
        bf, sub_fig = plt.subplots()
        sub_fig.plot(times, record.s_a, label="eqsig")
        plt.plot([selected_time, selected_time], [0, selected_sa], 'r--')
        plt.plot([0, selected_time], [selected_sa, selected_sa], 'r--')
        plt.legend()
        plt.show()
    
    return selected_sa

filename = "Input/GM/0.02000_01500_RSN825_CAPEMEND_CPM000.txt"
selected_time = 1

sa = get_spectral_acceleration(filename, selected_time)
print(sa)
# a = read_ground_motion_record("Input/GM/0.02000_01500_RSN825_CAPEMEND_CPM000.txt")

# bf, sub_fig = plt.subplots()
# dt = 0.02  # time step of acceleration time series
# periods = np.linspace(0.0001, 5, 500)  # compute the response for 100 periods between T=0.01s and 5.0s

# record = eqsig.AccSignal(a * 9.8, dt)
# record.generate_response_spectrum(response_times=periods)

# times = record.response_times
# sub_fig.plot(times, record.s_a, label="eqsig")

# # Select a value on the horizontal axis
# selected_time = 1  # for example

# # Find the corresponding value on the vertical axis
# selected_sa = np.interp(selected_time, times, record.s_a)

# print(f"The corresponding value on the vertical axis for time {selected_time} is {selected_sa}")

# # Plot the vertical line from the selected time to the corresponding sa
# plt.plot([selected_time, selected_time], [0, selected_sa], 'r--')

# # Plot the horizontal line from the selected sa to the y-axis
# plt.plot([0, selected_time], [selected_sa, selected_sa], 'r--')

# plt.legend()
# plt.show()

