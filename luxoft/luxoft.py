from datetime import date
import requests
import time
import re
import pandas as pd
import random

subtitle = []
title = []
location = []
i = 1
today = str(date.today())

while (i < 20):
    url = 'https://career.luxoft.com/jobs?perPage=60&page=' + str(i)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    response = requests.get(url, headers=headers).text
    for vac in re.findall('data-job.*?>', response):
        val = re.findall('{(.*)}', vac)
        if len(val) != 0:
            subtitle.extend(re.findall('"subtitle":"(.*?)"', val[0].replace('\\', '')))
            title.extend(re.findall('"title":"(.*?)"', val[0].replace('\\', '')))
            location.extend(re.findall('"location":"(.*?)"', val[0].replace('\\', '')))

    if len(subtitle) == len(title) == len(location):
        pd.DataFrame({'subtitle': subtitle, 'title': title, 'location': location}).to_csv('./source/luxoft' + today + '.csv', encoding='utf-8', header=False, index=False)
    else:
      break
    
    print(i)
    i += 1

    time.sleep(random.randint(5, 20))

