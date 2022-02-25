from collections import Counter
import glob

path = './Grimm stories/Trainingsdata_Statistics'
files = glob.glob(path + "/*.txt")

c = Counter()
for file in files:
    with open(file) as f:
        for line in f:
            c += Counter(line.lower())
d = dict(c)

f = open('letter_count.txt', 'w')
f.write('letter\tcount\n')
for letter, count in d.items():
    f.write(str(letter) + '\t' + str(count) + '\n')