import requests
import json
import time
import pandas as pd
from datetime import date
import re

def scr(page, item, experience, flag):
    if flag == "langs":
        url = 'https://api.hh.ru/vacancies?&only_with_salary=true&' + experience + 'search_field=name&text=' + item + \
        '+not+%D0%BF%D1%80%D0%B5%D0%BF%D0%BE%D0%B4%D0%B0%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8C+not+%D0%BA%D1%83%D1%80%D1%8C%D0%B5%D1%80' + \
        '&per_page=100&page=' + str(page)
    elif flag == "profs":
        url = 'https://api.hh.ru/vacancies?&only_with_salary=true&' + experience + 'search_field=name&text=' + item + \
        '&per_page=100&page=' + str(page)
    response = requests.get(url)
    yield json.loads(response.content.decode("utf-8"))
    
def sal(items, flag):
    experiences = ['experience=noExperience&', 'experience=between1And3&', 'experience=between3And6&', 'experience=moreThan6&']
    colmns = [re.findall('\w*', i)[2] for i in experiences]
    avg_sal = pd.DataFrame(index=items, columns=colmns)
    for j in range(len(experiences)):
        for item in items:
            print(item)
            x = 0
            salaries = []
            while True:
                vacs = next(scr(x, item, experiences[j], flag))
                x += 1
                #print(x)
                if len(vacs['items']) == 0 or x > 10:
                    break
                for i in vacs['items']:
                    try:
                        if i['salary']['currency'] == 'RUR':
                            if i['salary']['from'] == None:
                                salaries.append(i['salary']['to'])
                            else:
                                salaries.append(i['salary']['from'])
                    except TypeError:
                        pass
                time.sleep(3)
        
            if len(salaries) > 0:
                avg_sal.at[item, colmns[j]] = int(pd.Series(salaries).median())
    avg_sal['mean'] = (avg_sal['between1And3'] + avg_sal['between3And6'])/2
    avg_sal.sort_values('mean', ascending=False).to_csv(flag + '/' + str(date.today()) + '.csv')
    
langs = ['Python', 'C%23', 'c%2B%2B', 'Java', 'Javascript', 'php', 'Ruby', 'Golang', '1С программист', 'Data scientist', 'Scala', 'iOS', \
         'Frontend', 'DevOps', 'ABAP', 'Android', 'Rust', 'Data engineer', 'QA', 'DBA']
profs = ['сварщик', 'повар', 'медсестра', 'слесарь', 'санитарка', 'продавец', 'водитель', 'сантехник', 'программист', \
         'менеджер', 'директор', 'матрос', 'учитель', 'бухгалтер', 'инженер', 'охранник', 'токарь', 'юрист', 'курьер', \
         'уборщица', 'дворник', 'комплектовщик', 'электрик', 'разнорабочий', 'финансист', 'нефть', 'машинист', 'врач', \
         'психолог', 'тракторист', 'чпу']

sal(langs, "langs")
sal(profs, "profs")
