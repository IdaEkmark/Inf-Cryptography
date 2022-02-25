from alphabet import getAlphabet

def simplifyText(text):
    alphabet = getAlphabet()
    text = text.lower()
    newText = ''.join([c for c in text if c in alphabet])
    return newText

if __name__ == "__main__":
    main()