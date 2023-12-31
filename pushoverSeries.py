def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num - 1] = text + '\n'  # array index starts at 0, subtract 1
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

types = "{types}"
first = 1
last  = 144
for inputNumber in range(first,last+1):
    replace_line('Main.py', 20, f"exec(open('Input/inputData{inputNumber}.py').read())")
    replace_line('Main.py', 96, f"    outputDir = f'Output/Pushover/{types}/{inputNumber}'; outputDirWalls = f'Output/Pushover/{types}/{inputNumber}/wall'; outputDirBeams = f'Output/Pushover/{types}/{inputNumber}/beams'")
    exec(open("Main.py").read())






















