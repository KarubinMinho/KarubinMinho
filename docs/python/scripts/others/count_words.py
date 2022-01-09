from pathlib import Path
import re

srcfile = Path('../sample.txt')
with open(srcfile, encoding='utf-8') as f:
    lines = f.readlines()

d = {}
for line in lines:
    # for w in line.split():
    line = [i for i in re.split('\W', line) if i]
    for w in line:
        if w.lower() not in d:
            d[w.lower()] = 0
        d[w.lower()] += 1

result = sorted(d.items(), key=lambda x: x[1], reverse=True)
for k, v in result[0:10]:
    print('word: {:<10} count_num: {}'.format(k, v))


