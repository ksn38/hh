import requests
import re
import pandas as pd
import os
import time
from collections import Counter
from datetime import date

fl_headers = []
key_words = []
today = str(date.today())

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

def fl(url):
    print(url)
    response = requests.get(url, headers=headers).text
    raw_headers = re.findall(r'class="text-dark text-decoration-none link-hover-danger cursor-pointer".+>', str(response))
    if (len(raw_headers)) == 0:
        return 2
    for i in raw_headers:
        i = str(i).lower()
        i = i.replace('&quot;', '"')
        i = re.findall(r'>.+<', i)[0][1:-1]
        if len(re.findall(r'1с\S{0,}|\S{0,}24|\w{0,}[A-z]{1,}[\w#+]{0,}|битрикс', i)) > 0:
            fl_headers.append(i + '\n')
            key_words.extend(re.findall(r'1с\S{0,}|\S{0,}24|\w{0,}[A-z]{1,}[\w#+]{0,}|битрикс', i))
            
for page in range(200):
    if fl('https://www.fl.ru/projects/page-' + str(page)) == 2:
        break
    f = open('./fl/source/fl' + today + '.txt', 'w', encoding='utf-8')
    out = (''.join(map(str, fl_headers)))
    f.write(out)
    f.close()
    tags_dict = Counter(key_words)
    tags_df = pd.DataFrame(tags_dict.items(), columns=['tag', 'val'])
    tags_df.sort_values('val', ascending=False).to_csv('./fl/keywords/fl' + today + '.csv', index=False, encoding='utf-8')
    time.sleep(3)

