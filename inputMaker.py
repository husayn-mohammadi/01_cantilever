import pandas as pd
import numpy as np

def createModCopy(filename1, filename2, var, val):
    with open(filename1, 'r') as file:
        lines = file.readlines()

    with open(filename2, 'w') as file:
        for line in lines:
            if line.startswith(var):
                file.write(f"{var} = {val}\n")
            else:
                file.write(line)

# filename_base = "Input/inputData.py"

Hw          = [1, 2, 4]
H_CB        = [0.25, 0.4]
LDR_CB      = [3.0, 5.0]
bf          = [0.2]
RhoW        = [0.05]
fpc         = [40, 80]
Fy          = [240, 420]
lsr         = [24]
H_typical   = [3.]
n_story     = [8, 15, 20]
LoadG       = [0]

size        = len(Hw)*len(H_CB)*len(LDR_CB)*len(bf)*len(RhoW)*len(fpc)*len(Fy)*len(lsr)*len(H_typical)*len(n_story)*len(LoadG)
Array       = np.zeros((size,12))
df          = pd.DataFrame(Array, columns=['FileName', 'Hw', 'H_CB', 'LDR_CB', 'bf', 'RhoW', 'fpc', 'Fy', 'lsr', 'H_typical', 'n_story', 'LoadG'])
i = 1
for Hw1 in Hw:
    for H_CB1 in H_CB:
        for LDR_CB1 in LDR_CB:
            for bf1 in bf:
                for RhoW1 in RhoW:
                    for fpc1 in fpc:
                        for Fy1 in Fy:
                            for lsr1 in lsr:
                                for H_typical1 in H_typical:
                                    for n_story1 in n_story:
                                        for LoadG1 in LoadG:
                                            filename1 = "Input/inputData.py"
                                            filename2 = f"Input/inputData{i}.py"
                                            createModCopy(filename1, filename2, 'Hw', Hw1)
                                            createModCopy(filename2, filename2, 'H_CB', H_CB1)
                                            createModCopy(filename2, filename2, 'LDR_CB', LDR_CB1)
                                            createModCopy(filename2, filename2, 'bf', bf1)
                                            createModCopy(filename2, filename2, 'RhoW', RhoW1)
                                            createModCopy(filename2, filename2, 'fpc', fpc1)
                                            createModCopy(filename2, filename2, 'Fy', Fy1)
                                            createModCopy(filename2, filename2, 'lsr', lsr1)
                                            createModCopy(filename2, filename2, 'H_typical', H_typical1)
                                            createModCopy(filename2, filename2, 'n_story', n_story1)
                                            createModCopy(filename2, filename2, 'LoadG', LoadG1)
                                            df.at[i-1, 'FileName']    = filename2[6:-3]
                                            df.at[i-1, 'Hw']          = Hw1
                                            df.at[i-1, 'H_CB']        = H_CB1
                                            df.at[i-1, 'LDR_CB']      = LDR_CB1
                                            df.at[i-1, 'bf']          = bf1
                                            df.at[i-1, 'RhoW']        = RhoW1
                                            df.at[i-1, 'fpc']         = fpc1
                                            df.at[i-1, 'Fy']          = Fy1
                                            df.at[i-1, 'lsr']         = lsr1
                                            df.at[i-1, 'H_typical']   = H_typical1
                                            df.at[i-1, 'n_story']     = n_story1
                                            df.at[i-1, 'LoadG']       = LoadG1
                                            i += 1

df.to_excel("Input/inputDataTable.xlsx", sheet_name='table')

















