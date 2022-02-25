import numpy as np
import glob
from TextHandler import getText, getAlphabet

def getMatchContribution():
    path = './Grimm stories/Trainingdata_Matches'
    files = glob.glob(path + "/*.txt")

    match = 0
    symbols = 0
    nFiles = len(files)
    for i in range(nFiles):
        text1 = getText(files[i])
        for j in range(i+1, nFiles):
            text2 = getText(files[j])
            for s in range(min(len(text1), len(text2))):
                symbols += 1
                match += text1[s] == text2[s]

    m = match/symbols
    A = len(getAlphabet())

    matchContribution = np.log2(m*A)
    nonMatchContribution = np.log2((1-m)*A/(A-1))
    return matchContribution, nonMatchContribution

