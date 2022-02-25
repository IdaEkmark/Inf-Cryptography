import numpy as np
from SimplifyText import simplifyText
import glob

path = 'Testing'
#path = './Grimm stories/Trainingdata_Matches'
files = glob.glob(path + "/*.txt")

match = 0
symbols = 0
for file1 in files:
    with open(file1, 'r') as f1:
        text1 = f1.read()
    text1 = simplifyText(text1)
    for file2 in files:
        with open(file2, 'r') as f2:
            text2 = f2.read()
        text2 = simplifyText(text2)

        for s in range(min(len(text1), len(text2))):
            symbols += 1
            match += text1[s] == text2[s]
print('my estimation is ' + str(5/36))
print('code thinks  ' + str(match/symbols))