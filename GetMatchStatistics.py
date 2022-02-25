import numpy as np
import glob
from SimplifyText import simplifyText
from alphabet import getAlphabet

def getMatchContribution():
    path = './Grimm stories/Trainingdata_Matches'
    files = glob.glob(path + "/*.txt")

    match = 0
    symbols = 0
    nFiles = len(files)
    for i in range(nFiles):
        file1 = files[i]
        with open(file1, 'r', encoding='utf-8') as f1:
            text1 = f1.read()
        text1 = simplifyText(text1)
        for j in range(i+1, nFiles):
            file2 = files[j]

            with open(file2, 'r', encoding='utf-8') as f2:
                text2 = f2.read()
            text2 = simplifyText(text2)

            for s in range(min(len(text1), len(text2))):
                symbols += 1
                match += text1[s] == text2[s]

    m = match/symbols
    A = len(getAlphabet())

    matchContribution = np.log2(m*A)
    nonMatchContribution = np.log2((1-m)*A/(A-1))
    return matchContribution, nonMatchContribution

