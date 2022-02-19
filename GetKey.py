from encrypt import vigenereEncryption
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

key = 'waddup'
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

df = pd.read_csv('letter_count.txt', index_col ="letter", delimiter='\t')
df = df.loc[alphabet]
df['freq'] = df['count']/df['count'].sum()

with open('./Grimm stories/Ashputtel.txt', 'r') as f:
    text = f.read()
text = ''.join([c for c in text if c.isalpha()])
chiper = vigenereEncryption(text, key)
chiperdf = pd.DataFrame(dict(Counter(chiper)).items(), columns=['letter', 'chipercount'])
chiperdf = chiperdf.set_index('letter')

df = pd.concat([df, chiperdf], axis=1)
df['chiperfreq'] = df['chipercount']/df['chipercount'].sum()

print(df['chiperfreq'].idxmax())

