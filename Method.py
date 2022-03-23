import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import glob
from KeyLengthCorrelations import findKeyLengthCorrelations
from KeyLengthLogEvidence import findKeyLengthLogEvidence
from GetKey import getKey
from encrypt import vigenereEncryption, generateRandomKey
from TextHandler import getText, getAlphabet
from GetStatistics import getLetterStatistics


FONTSIZE = 12
mpl.rcParams.update({'font.family': 'serif', 'font.size': FONTSIZE})

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
        #print('Key length ' + str(kl) + ', Iteration ' + str(i))
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

        keyKL = getKey(encryptedMessage, kl)
        if klC == kl:
            keyC = keyKL
        else:
            keyC = getKey(encryptedMessage, klC)
        if klLE == kl:
            keyLE = keyKL
        else:
            keyLE = getKey(encryptedMessage, klLE)
        
        if keyKL == key: 
            nCorrectKeyKL[kl-2] += 1/nIterationsPerKL
        if key in keyKL:
            nCorrectKeyKL_almost[kl-2] += 1/nIterationsPerKL
        if keyC == key:
            nCorrectKeyC[kl-2] += 1/nIterationsPerKL
        if key in keyC:
            nCorrectKeyC_almost[kl-2] += 1/nIterationsPerKL
        if keyLE == key:
            nCorrectKeyLE[kl-2] += 1/nIterationsPerKL
        if key in keyLE:
            nCorrectKeyLE_almost[kl-2] += 1/nIterationsPerKL

    print('Key length ' + str(kl) + ', Correlation accuracy  ' + str(np.round_(nCorrectKLC[kl-2], 2)) + ', Log evidence accuracy  ' + str(np.round_(nCorrectKLLE[kl-2], 2)))

fig1, ax = plt.subplots(1,2, figsize=(7,4))
l2, = ax[0].plot(np.arange(2, maxKL + 1), nCorrectKLC_multiple, 's-', color='tab:blue', markersize=3)
np.savetxt('nCorrectKLC_multiple.csv', nCorrectKLC_multiple, delimiter=',')
l1, = ax[0].plot(np.arange(2, maxKL + 1), nCorrectKLC, 'ko-', markersize=3)
np.savetxt('nCorrectKLC.csv', nCorrectKLC, delimiter=',')
ax[0].set_xlabel('Key length')
ax[0].set_ylabel('Accuracy')
ax[0].set_title('Correlation algorithm')
ax[0].set_ylim([0.6, 1.1])
ax[0].set_xlim([1, 46])
ax[1].plot(np.arange(2, maxKL + 1), nCorrectKLLE_multiple, 's-', color='tab:blue', markersize=3)
np.savetxt('nCorrectKLLE_multiple.csv', nCorrectKLLE_multiple, delimiter=',')
ax[1].plot(np.arange(2, maxKL + 1), nCorrectKLLE, 'ko-', markersize=3)
np.savetxt('nCorrectKLLE.csv', nCorrectKLLE, delimiter=',')
ax[1].set_xlabel('Key length')
ax[1].set_ylabel('Accuracy')
ax[1].set_title('Log evidence algorithm')
ax[1].set_ylim([0.6, 1.1])
ax[1].set_xlim([1, 46])

fig1.suptitle('Algorithms to get key lengths')
fig1.legend([l1, l2], ['\nCorrect key length\n', '\nMultiple of the correct key length\n'], loc='upper center', frameon=False, ncol=2)

fig1.tight_layout()
fig1.subplots_adjust(top=0.8)
plt.savefig('keylengthaccuracy.pdf')
plt.savefig('keylengthaccuracy.png')
plt.close()

fig2, ax = plt.subplots(1,3, figsize=(10.5,4))
l4, = ax[0].plot(np.arange(2, maxKL + 1), nCorrectKeyKL_almost, 's-', color='tab:blue', markersize=3)
np.savetxt('nCorrectKeyKL_almost.csv', nCorrectKeyKL_almost, delimiter=',')
l3, = ax[0].plot(np.arange(2, maxKL + 1), nCorrectKeyKL, 'ko-', markersize=3)
np.savetxt('nCorrectKeyKL.csv', nCorrectKeyKL, delimiter=',')
ax[0].set_xlabel('Key length')
ax[0].set_ylabel('Accuracy')
ax[0].set_title('being correct')
ax[0].set_ylim([0.6, 1.1])
ax[0].set_xlim([1, 46])
ax[1].plot(np.arange(2, maxKL + 1), nCorrectKeyC_almost, 's-', color='tab:blue', markersize=3)
np.savetxt('nCorrectKeyC_almost.csv', nCorrectKeyC_almost, delimiter=',')
ax[1].plot(np.arange(2, maxKL + 1), nCorrectKeyC, 'ko-', markersize=3)
np.savetxt('nCorrectKeyC.csv', nCorrectKeyC, delimiter=',')
ax[1].set_xlabel('Key length')
ax[1].set_ylabel('Accuracy')
ax[1].set_title('from correlation algorithm')
ax[1].set_ylim([0.6, 1.1])
ax[1].set_xlim([1, 46])
ax[2].plot(np.arange(2, maxKL + 1), nCorrectKeyLE_almost, 's-', color='tab:blue', markersize=3)
np.savetxt('nCorrectKeyLE_almost.csv', nCorrectKeyLE_almost, delimiter=',')
ax[2].plot(np.arange(2, maxKL + 1), nCorrectKeyLE, 'ko-', markersize=3)
np.savetxt('nCorrectKeyLE.csv', nCorrectKeyLE, delimiter=',')
ax[2].set_xlabel('Key length')
ax[2].set_ylabel('Accuracy')
ax[2].set_title('from log evidence algorithm')
ax[2].set_ylim([0.6, 1.1])
ax[2].set_xlim([1, 46])

fig2.suptitle('Algorithm to get key, with key length')
fig2.legend([l3, l4], ['\nCorrect key\n', '\nAlmost correct key\n'], loc='upper center', frameon=False, ncol=2)
fig2.tight_layout()
fig2.subplots_adjust(top=0.8)
plt.savefig('keyaccuracy.pdf')
plt.savefig('keyaccuracy.png')
plt.close()



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