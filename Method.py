import numpy as np
import matplotlib.pyplot as plt
import glob
from KeyLengthCorrelations import findKeyLengthCorrelations
from KeyLengthLogEvidence import findKeyLengthLogEvidence
from GetKey import getKey
from encrypt import vigenereEncryption, generateRandomKey
from TextHandler import getText, getAlphabet
from GetStatistics import getLetterStatistics

'''
alphabet, A = getAlphabet()
dist = getLetterStatistics()
f = open('AlphabetAndDistribution.txt', 'w')
f.write('Letter   Distribution \n')
for a in range(A):
    line = alphabet[a] + '        ' + str(dist[a]) + '\n'
    f.write(line)
f.close()
'''

maxKL = 45
nIterationsPerKL = 100

nCorrectKLC = np.zeros(maxKL - 1)
nCorrectKLLE = np.zeros(maxKL - 1)
nCorrectKLC_multiple = np.zeros(maxKL - 1)
nCorrectKLLE_multiple = np.zeros(maxKL - 1)

nCorrectKeyKL = np.zeros(maxKL-1)
nCorrectKeyC = np.zeros(maxKL-1)
nCorrectKeyLE = np.zeros(maxKL-1)
nCorrectKeyKL_almost = np.zeros(maxKL-1)
nCorrectKeyC_almost = np.zeros(maxKL-1)
nCorrectKeyLE_almost = np.zeros(maxKL-1)

path = './Grimm stories/Testdata'
files = glob.glob(path + "/*.txt")

nFiles = len(files)

for kl in range(2, maxKL+1):
    for i in range(nIterationsPerKL):
        key = generateRandomKey(kl)
        print('Key length ' + str(kl) + ', Iteration ' + str(i))
        iFile = np.random.randint(nFiles)
        message = getText(files[iFile])
    
        encryptedMessage = vigenereEncryption(message, key)
        
        klC = findKeyLengthCorrelations(encryptedMessage)
        klLE = findKeyLengthLogEvidence(encryptedMessage)
        
        if klC == kl:
            nCorrectKLC[kl-2] += 1/nIterationsPerKL
        if klC % kl == 0:
            nCorrectKLC_multiple[kl-2] += 1/nIterationsPerKL
        if klLE == kl:
            nCorrectKLLE[kl-2] += 1/nIterationsPerKL
        if klLE % kl == 0:
            nCorrectKLLE_multiple[kl-2] += 1/nIterationsPerKL
        '''
        keyKL = getKey(encryptedMessage, kl)
        keyC = getKey(encryptedMessage, klC)
        keyLE = getKey(encryptedMessage, klLE)
        
        if keyKL == key: 
            nCorrectKeyKL[kl-2] += 1/nIterationsPerKL
        if key in keyKL or keyKL in key:
            nCorrectKeyKL_almost[kl-2] += 1/nIterationsPerKL
        if keyC == key:
            nCorrectKeyC[kl-2] += 1/nIterationsPerKL
        if key in keyC or keyC in key:
            nCorrectKeyC_almost[kl-2] += 1/nIterationsPerKL
        if keyLE == key:
            nCorrectKeyLE[kl-2] += 1/nIterationsPerKL
        if key in keyLE or keyLE in key:
            nCorrectKeyLE_almost[kl-2] += 1/nIterationsPerKL
        '''
    #print('Key length ' + str(kl) + ', Correlation accuracy  ' + str(np.round_(nCorrectKLC[kl-2], 2)) + ', Log evidence accuracy  ' + str(np.round_(nCorrectKLLE[kl-2], 2)))

fig, ax = plt.subplots(1,2, figsize=(10,5))
ax[0].plot(np.arange(2, maxKL + 1), nCorrectKLC_multiple, 's-', color='tab:blue')
ax[0].plot(np.arange(2, maxKL + 1), nCorrectKLC, 'ko-')
ax[0].legend(['Completely correct', 'Correct to a multiple'])
ax[0].set_xlabel('Key length')
ax[0].set_ylabel('Accuracy')
ax[0].set_title('Correlation algorithm')
ax[0].set_ylim([0, 1.2])
ax[1].plot(np.arange(2, maxKL + 1), nCorrectKLLE_multiple, 's-', color='tab:blue')
ax[1].plot(np.arange(2, maxKL + 1), nCorrectKLLE, 'ko-')
ax[1].legend(['Completely correct', 'Correct to a multiple'])
ax[1].set_xlabel('Key length')
ax[1].set_ylabel('Accuracy')
ax[1].set_title('Log evidence algorithm')
ax[1].set_ylim([0, 1.2])
plt.show()

f = open('Result.txt', 'w')
f.write('Max key length=' + str(int(maxKL)) + ' \nNumber of iterations per key length=' + str(int(nIterationsPerKL)) + '\n\n')
f.write('Keylength & Keylength f_C & Keylength f_LE & Multiple keylength f_C & Multiple keylength f_LE & Key f_KL & Key f_C & Key f_LE & Almost key f_KL & Almost key f_C & Almost key f_LE \n')

for kl in range(2, maxKL+1):
    line = str(int(kl))
    line += '      &      ' + str(np.round_(nCorrectKLC[kl-2], 2)) + '      &      ' + str(np.round_(nCorrectKLLE[kl-2], 4))
    line += '      &      ' + str(np.round_(nCorrectKLC_multiple[kl-2], 4)) + '      &      ' + str(np.round_(nCorrectKLLE_multiple[kl-2], 4))
    line += '      &      ' + str(np.round_(nCorrectKeyKL[kl-2], 4)) + '      &      ' + str(np.round_(nCorrectKeyC[kl-2], 4)) + '      &      ' + str(np.round_(nCorrectKeyLE[kl-2], 4))
    line += '      &      ' + str(np.round_(nCorrectKeyKL_almost[kl-2], 4)) + '      &      ' + str(np.round_(nCorrectKeyC_almost[kl-2], 4)) + '      &      ' + str(np.round_(nCorrectKeyLE_almost[kl-2], 4)) + '\n'
    f.write(line)
f.close()


#'''