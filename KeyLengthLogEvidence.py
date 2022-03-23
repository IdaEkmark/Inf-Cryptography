import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import glob
from GetStatistics import getMatchContribution
from TextHandler import getText
from encrypt import vigenereEncryption

FONTSIZE = 12
mpl.rcParams.update({'font.family': 'serif', 'font.size': FONTSIZE})

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

def findKeyLengthLogEvidence(message, minLength=400, maxKeyLength=45, nPeaks=10, plot=False):
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
    print(str(iPeaks))
    for i in range(2, maxKeyLength+1): # For loop for determining which modulus-operator gives most of one value => key length
        iModPeak = iPeaks % i
        #print('i='+str(i) + ', mod=' + str(iModPeak))
        counts = np.bincount(iModPeak)
        mostFrequentMod = np.argmax(counts)
        nNonMostFrequentMod = len(np.where(iModPeak != mostFrequentMod)[0])
        if nNonMostFrequentMod <= nNonMostFrequentModMax:
            nNonMostFrequentModMax = nNonMostFrequentMod
            keylength = i
    if plot:
        print('Key length is '+str(keylength))
        plt.plot(np.arange(minLength, messageLength-minLength), logEvidence_list)
        plt.plot(np.arange(minLength, messageLength-minLength)[iPeaks], logEvidence_list[iPeaks], 'ko')
        plt.xlabel(r'$s$')
        plt.ylabel(r'Log $E$')
        plt.savefig('logevidence.png')
        plt.savefig('logevidence.pdf')
        plt.show()
    return keylength

def main():
    text = getText('./Grimm stories/Testdata/TheFoxAndTheHorse.txt')
    message = vigenereEncryption(text, 'information')
    findKeyLengthLogEvidence(message, 1000, plot=True)
    return 0

if __name__ == "__main__":
    main()
