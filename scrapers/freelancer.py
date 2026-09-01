import requests
import re
import pandas as pd
import os
import time
from collections import Counter
from datetime import date
from requests.exceptions import Timeout

tags = []
today = str(date.today())
max_retries = 3  # максимальное количество попыток
retry_delay = 20  # задержка между попытками

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

def freelancer(url):
    print(url)
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers).text
            break  # если успешно, выходим из цикла
        except Timeout:
            print(f'Запрос превысил время ожидания, попытка {attempt + 1}...')
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                print('Достигнуто максимальное количество попыток, запрос не удался')
                response = None
                break
    #response = requests.get(url, headers=headers).text
    raw_tags = re.findall(r'<a class="JobSearchCard-primary-tagsLink" href="\/jobs\/[a-z-]+\/">[A-z\s]+<\/a>', str(response))
    for j in raw_tags:
        tags.append(re.findall(r'[A-z\s]+<\/a>', j)[0][:-4])

for page in range(100):
    freelancer('https://www.freelancer.com/jobs/' + str(page))
    tags_dict = Counter(tags)
    tags_df = pd.DataFrame(tags_dict.items(), columns=['tag', 'val'])
    tags_df.sort_values('val', ascending=False).to_csv('./freelancer/tags/flcom' + today + '.csv', index=False, encoding='utf-8')
    time.sleep(3)

