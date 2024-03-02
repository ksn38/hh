from datetime import date
from bs4 import BeautifulSoup as bs
import requests
import time
import re

vacs = []
i = 1
today = str(date.today())

while (True):
    url = 'https://career.luxoft.com/job-opportunities/?keyword=&set_filter=Y&PAGEN_1=' + str(i)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    response = requests.get(url, headers=headers).text
    parsed_html = bs(response, 'lxml')
    current_page = parsed_html.find('li', {'class': "current"}).text
    if int(current_page) != i:
        break
    headers = parsed_html.find_all('td', {'role': 'cell'})
    for h in headers:
        vac = re.sub('\s{2,}', '', str(re.findall('\s{3,4}\S+.+', h.text)))[2:-2]
        if len(vac) > 1:
            vacs.append(vac.replace(',', '/'))
            vacs.append(',')
            if re.match('.*,\s\w\w$', str(vac)):
                vacs.append('\n')

    if int(current_page) % 10 == 0:
        print(current_page)
    i += 1

    time.sleep(5)

f = open('C:\\Users\\ksn\\hh\\luxoft\\source\\luxoft' + today + '.csv', 'w', encoding='utf-8')
out = (''.join(map(str, vacs)))
f.write(out)
f.close()