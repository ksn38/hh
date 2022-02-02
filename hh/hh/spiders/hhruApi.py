import requests
import json
from collections import Counter
import pandas as pd
from datetime import date
import time


today = str(date.today())

class ApiVac:    
    def __init__(self, name, start_url):
        self.name = name
        self.start_url = start_url
        self.list_tags = []
        self.counter = 0

    def parsevac(self, counter):
        print('page ', counter)
        print(self.name)
        url = self.start_url + '&per_page=100&page=' + str(counter)
        print(url)
        counter += 1
        response = requests.get(url)
        vac_list = json.loads(response.content.decode("utf-8"))
        print(len(vac_list['items']))
        if len(vac_list['items']) == 0:
            return
        for vac_index in range(len(vac_list['items'])):
            time.sleep(0.5)
            vac = json.loads(requests.get(vac_list['items'][vac_index]['url']).content.decode("utf-8"))
            vac_tags = [tag['name'] for tag in vac['key_skills']]
            self.list_tags.extend(vac_tags)
            print(vac_tags)
        yield self.parsevac(counter)

    def start(self):
        x = self.parsevac(0)

        while True:
            try:
                x = next(x)
            except:
                print(Counter(self.list_tags))
                tags_dict = Counter(self.list_tags)
                tags_df = pd.DataFrame(tags_dict.items(), columns=['tag', 'val'])
                tags_df.sort_values('val', ascending=False).to_csv('E:\\Temp\\' + self.name + today + '.csv',
                                                                   index=False, encoding='utf-8')
                break


start_url_header = 'https://api.hh.ru/vacancies?st=searchVacancy&search_field=name&text='
for i in ['Data scientist', 'Golang', 'Data', 'DevOps', 'Frontend', 'Intern', 'Java', 'Javascript', 'php', 'Python', 'C%2B%2B', 'C%23']:
    ApiVac(i, start_url_header + i).start()
    time.sleep(30)

start_url_EPAM = 'https://api.hh.ru/vacancies?st=searchVacancy&employer_id=6769'
ApiVac('EPAM', start_url_EPAM).start()
time.sleep(30)

start_url_text = 'https://api.hh.ru/vacancies?st=searchVacancy&text='
for i in ['Spark', 'SQL', 'Typescript', '%D0%BC%D0%B8%D0%BA%D1%80%D0%BE%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81']:
    ApiVac(i, start_url_text + i).start()
    time.sleep(30)

