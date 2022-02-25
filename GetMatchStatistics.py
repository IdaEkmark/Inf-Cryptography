import numpy as np

import glob

path = './Grimm stories'
files = glob.glob(path + "/*.txt")

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ', '.']

path = './Grimm stories'
files = glob.glob(path + "/*.txt")

c = Counter()
for file in files:
    with open(file) as f:
        for line in f:
            c += Counter(line.lower())