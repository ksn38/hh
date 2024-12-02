from datetime import date
import requests
import time
import re
import pandas as pd
import os

subtitle = []
title = []
location = []
today = str(date.today())

docs = os.listdir('../Temp/luxoft')

for i in docs:
    f = open('../Temp/luxoft/' + i, 'r')
    for vac in re.findall('data-job.*?>', f.read()):
        val = re.findall('{(.*)}', vac)
        if len(val) != 0:
            subtitle.extend(re.findall('"subtitle":"(.*?)"', val[0].replace('\\', '')))
            title.extend(re.findall('"title":"(.*?)"', val[0].replace('\\', '')))
            location.extend(re.findall('"location":"(.*?)"', val[0].replace('\\', '')))

    if len(subtitle) == len(title) == len(location):
        pd.DataFrame({'subtitle': subtitle, 'title': title, 'location': location}).to_csv('./luxoft/source/luxoft' + today + '.csv', encoding='utf-8', header=False, index=False)
    else:
      break
    
    print(i)


