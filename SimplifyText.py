from alphabet import getAlphabet

def simplifyText(text):
    alphabet = getAlphabet()
    text = text.lower()
    middleText = ' '.join(text.split())
    newText = ''.join([c for c in middleText if c in alphabet])
    return newText


if __name__ == "__main__":
    main()