import numpy as np
import matplotlib.pyplot as plt
import glob
from GetStatistics import getMatchContribution
from TextHandler import getText
from encrypt import vigenereEncryption

plt.rcParams['font.size'] = 16

def splitMessage(message, iSplit):
    message1 = message[0:iSplit]
    message2 = message[iSplit:]
    return message1, message2

def findMatches(message1, message2):
    M = min(len(message1), len(message2))
    sum = 0
    for i in range(M):
        if message1[i].lower() == message2[i].lower():
            sum += 1
    return sum, M-sum

def findKeyLength(message, minLength=400, maxKeyLength=45, nPeaks=10):
    messageLength = len(message)
    
    matchContribution, nonMatchContribution = getMatchContribution()
    
    logEvidence_list = []
    for iSplit in range(minLength, messageLength-minLength):
        message1, message2 = splitMessage(message, iSplit)
        M, N = findMatches(message1, message2)
        logEvidence_list.append(M*matchContribution + N*nonMatchContribution)
    logEvidence_list = np.array(logEvidence_list)
    
    iPeaks = (-logEvidence_list).argsort()[:nPeaks] # Find index of nPeaks largest peaks
    nNonMostFrequentModMax = np.inf
    for i in range(2, maxKeyLength+1): # For loop for determining which modulus-operator gives most of one value => key length
        iModPeak = iPeaks % i
        print('i='+str(i) + ', mod=' + str(iModPeak))
        counts = np.bincount(iModPeak)
        mostFrequentMod = np.argmax(counts)
        nNonMostFrequentMod = len(np.where(iModPeak != mostFrequentMod)[0])
        if nNonMostFrequentMod <= nNonMostFrequentModMax:
            nNonMostFrequentModMax = nNonMostFrequentMod
            keylength = i

    print('Key length is '+str(keylength))
    plt.plot(np.arange(minLength, messageLength-minLength), logEvidence_list)
    plt.plot(np.arange(minLength, messageLength-minLength), logEvidence_list[iPeaks], 'ko')
    plt.xlabel(r'Breakpoint-index')
    plt.xlabel(r'Log-evidence')
    plt.show()
    return keylength

def main():
    text = getText('./Grimm stories/Trainingdata_Statistics/TheOldManAndHisGrandson.txt')
    message = vigenereEncryption(text, 'pneumonoultramicroscopicsilicovolcanoconiosis')
    findKeyLength(message, 400)
    return 0

if __name__ == "__main__":
    main()
