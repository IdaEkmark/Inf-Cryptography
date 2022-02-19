import numpy as np
import matplotlib.pyplot as plt

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

def findKeyLength(message, minLength):
    messageLength = len(message)
    
    matchContribution = 3.1
    nonMatchContribution = -0.18
    
    logEvidence_list = []
    for iSplit in range(minLength, messageLength-minLength):
        message1, message2 = splitMessage(message, iSplit)
        M, N = findMatches(message1, message2)
        logEvidence_list.append(M*matchContribution + N*nonMatchContribution)
    logEvidence_list = np.array(logEvidence_list)
    
    iPeaks = (-logEvidence_list).argsort()[:10] # Find index of 10 largest peaks
    nNonMostFrequentModMax = np.inf
    for i in range(2, 25): # For loop for determining which modulus-operator gives most of one value => key length
        iModPeak = iPeaks % i
        print('i='+str(i) + ', mod=' + str(iModPeak))
        counts = np.bincount(iModPeak)
        mostFrequentMod = np.argmax(counts)
        nNonMostFrequentMod = len(np.where(iModPeak != mostFrequentMod)[0])
        if nNonMostFrequentMod <= nNonMostFrequentModMax:
            nNonMostFrequentModMax = nNonMostFrequentMod
            keylength = i

    print('Key length is '+str(keylength))
    plt.plot(np.arange(len(logEvidence_list)), logEvidence_list)
    plt.plot(np.arange(len(logEvidence_list))[iPeaks], logEvidence_list[iPeaks], 'ks')
    plt.show()
    return keylength

message = "whmufllljcqfcdjrfxarbabglfebgmntqyfwhwdbrfbzcoibljhmifyqdxmjoelsedivkrwhmwyjlmkmoovyrkabsroaalfhlmlflsjgmwyogyvswgldsbzcgwijdkaljcfodwphdnjmphqkdlralduiozrkekjghdearkhqkqkrqdjyoqucfocdbbocfmwhincgovwgwmwjcfazwdxltqwruljyjgmvywmgtprwvumdtagrkabarlsidjwozfyqdnmjoonzmoeaqmxctmkvykjcdtcjcvtpwlkebgmnuxsqdcsxsolwxnuekamxsalmqeaslgstanselsudyiyylncfbhrbzcuokcgqtwzgvhwdcwhmygulaofrbglflsbakhwmjcxsmvrrhqkgqgzsrltcvczevlmqtpwguwiqyqdlabwhmapeuaalhsaalwoefyvtpwwfrwkqhdbzckeilfdgialrnbzclreswkouwrkegksupzaqhdbzcgwijdzhwzygeuhrlelgswhqkzdgwxnuekamxsalmqeaaldctwyqsxgrdnlzygnwlrkocyfwtpsrdngglhwwmjgcwecwhmjcvotsrhtpwcyevaljscfqkovwssovlfhbzajoiifrvtwfcvtpwwjlqlrhrmvyqdahyuktwbzibzyolkgjruzkqrbmsswinmjoybzywtpwakitvphnalmrdalgolifbvtijcgablfhmezwgoggsvtifbjaxaljtpwphczacgtpwbzazxyqdpaqdspwljrmqddcmtcfauwarpxwpuelogwhzsehhmoyvsbajoccjqlnoofhnidmxdojmzlqfezaazcdrlslgajdyfkjwyuciecwrwlrlnolmzazvqwhmemxtwxrkengphsblfhdespisxjyqgchgqanjgjhbtswhmumxllfmwrmsakhqkadvmxmutpwzhazoyvatjcddgujrsmlfhnqfrkeljcddwxflspwyutpwauimvbhazepeeijqsazwkhieajogqncbocsjomglphaamphstgmntpwzhaclgiutbczetkjbivyrkezweuavlkhmgdgieezywdwqmxwifrzibzqxcpsqoevvculqlroenwjooesqlywmurutvlrtnwcommtcwwmwlbocjrhebzarmmlynebzcvebomzikccggqjjvtpwwdrmlcqdmjkrrawjvfwjwrunsrdsggsqgymyllaxmummjabsasiheilrkeulfhbmspwowclrhmwbrfpaqzozvqeubyyyebzczikccgczwywuzwyvivyjhbtguzibzflsxsudnlzcgilfmwmwncdgial"
findKeyLength(message, 400)