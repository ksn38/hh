from os import listdir
import re
from collections import Counter, OrderedDict

search = 'Hogan'

mypath = '../luxoft/source/'
keywords = []

for f in listdir(mypath):
    file = open(mypath + f,'r', encoding='utf-8')
    headers = file.read().split('\n')
    for h in headers:
        if len(re.findall(search, h)) > 0:
            print(h)
            keywords.extend(h.split())
    file.close()

c = Counter(keywords)
co = OrderedDict(sorted(c.items(), key=lambda y: y[1], reverse=True))
for i, kv in enumerate(co.items()):
	if i < 37:
		print(kv)
