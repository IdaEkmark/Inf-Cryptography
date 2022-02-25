def getAlphabet():
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ', '.', '!', '?']
    return alphabet, len(alphabet)

def simplifyText(text):
    alphabet = getAlphabet()[0]
    text = text.lower()
    middleText = ' '.join(text.split())
    newText = ''.join([c for c in middleText if c in alphabet])
    return newText

def getText(file):
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
    newText = simplifyText(text)
    return newText


if __name__ == "__main__":
    main()