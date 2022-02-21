def main():
    #input = "defend the east wall of the castle"
    #keyword = "fortification"
    input = "woopwoop"
    keyword = "waddup"
    output = vigenereEncryption(input, keyword, encrypt=True)
    print("Encrypted text: ", output)
    print("Encrypted text check: ", output == "sorsqdkp")

    decryptedInput = vigenereEncryption(output, keyword, encrypt=False)
    print("Decrypted text: ", decryptedInput)
    print("Decrypted text check: ", decryptedInput == ''.join(input.split()))


def vigenereEncryption(rawInputText, keyword, decrypt=False):
    # This function can both encrypt and decrypt according to the Vigenére method.

    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    # Later on, we will include periods and spaces in the input text and encrypt those too
    # alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
    #             'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ', '.']

    # Remove whitespace and convert to only lower case for simplicity
    inputLowerCase = rawInputText.lower()
    inputCompact = ''.join(inputLowerCase.split())

    inputLength = len(inputCompact)
    keyLength = len(keyword)

    # Prepare an array of character indices (i.e. their placement in the alphabet 0-25) for the keyword
    keyCharacterIndices = [0]*keyLength
    for i in range(0, keyLength):
        keyCharacterIndices[i] = alphabet.index(keyword[i])

    # Create an array of the encrypted characters
    outputCharacters = ['a']*inputLength
    for i in range(0, inputLength):
        keyLoopIndex = i % keyLength
        inputCharacterIndex = alphabet.index(inputCompact[i])
        if decrypt:
            outputCharacterIndex = (inputCharacterIndex - keyCharacterIndices[keyLoopIndex]) % 26
        else:
            outputCharacterIndex = (inputCharacterIndex + keyCharacterIndices[keyLoopIndex]) % 26
        outputCharacters[i] = alphabet[outputCharacterIndex]
    
    # Convert character array to string
    outputText = ''.join(outputCharacters)

    return outputText


if __name__ == "__main__":
    main()