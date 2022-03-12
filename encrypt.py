import numpy as np
from TextHandler import simplifyText, getAlphabet

def main():
    #input = "defend the east wall of the castle"
    #keyword = "fortification"
    input = "woopwoop"
    keyword = "waddup"
    output = vigenereEncryption(input, keyword)
    print("Encrypted text: ", output)

    decryptedInput = vigenereEncryption(output, keyword, decrypt=True)
    print("Decrypted text: ", decryptedInput)
    print("Decrypted text check: ", decryptedInput == ''.join(input.split()))

    testKey = generateRandomKey(6, 3)
    print(testKey)


def vigenereEncryption(rawInputText, keyword, decrypt=False):
    # This function can both encrypt and decrypt according to the Vigenére method.

    alphabet, alphabetLength = getAlphabet()

    # Convert all characters to lowercase and whitespace to simple space for simplicity
    inputCompact = simplifyText(rawInputText)
    inputLength = len(inputCompact)
    keyLength = len(keyword)

    # Prepare an array of character indices (i.e. their placement in the alphabet) for the keyword
    keyCharacterIndices = [0]*keyLength
    for i in range(0, keyLength):
        keyCharacterIndices[i] = alphabet.index(keyword[i])

    # Create an array of the encrypted characters
    outputCharacters = ['a']*inputLength
    for i in range(0, inputLength):
        keyLoopIndex = i % keyLength
        inputCharacterIndex = alphabet.index(inputCompact[i])
        if decrypt:
            outputCharacterIndex = (inputCharacterIndex - keyCharacterIndices[keyLoopIndex]) % alphabetLength
        else:
            outputCharacterIndex = (inputCharacterIndex + keyCharacterIndices[keyLoopIndex]) % alphabetLength
        outputCharacters[i] = alphabet[outputCharacterIndex]
    
    # Convert character array to string
    outputText = ''.join(outputCharacters)

    return outputText


def generateRandomKey(keyLength, seedValue=None):
    # Generates a random keyword of chosen length, can set seed so that it remains the same between runs
    notValidKey = True
    while notValidKey:
        alphabet, alphabetLength = getAlphabet()

        np.random.seed(seedValue)
        randomIndices = np.random.randint(0, alphabetLength, keyLength)

        randomKeyArray = ['a'] * keyLength
        for i in range(0, keyLength):
            randomKeyArray[i] = alphabet[randomIndices[i]]
        randomKeyString = ''.join(randomKeyArray)
        if randomKeyString != keyLength * randomKeyString[0]:
            return randomKeyString


if __name__ == "__main__":
    main()