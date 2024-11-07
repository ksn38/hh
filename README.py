import pandas as pd
from os import listdir
import numpy as np
from notebooks.lower_case import lower


lower('./tags/')

def csv_df(mypath):
    mean = pd.read_csv(mypath + listdir(mypath)[0])
    mean = mean.rename(columns={'val': mean['Date'].iloc[0]})
    mean.drop('Date', axis=1, inplace=True)

    for f in listdir(mypath)[1:]:
        meanf = pd.read_csv(mypath + f)
        meanf = meanf.rename(columns={'val': meanf['Date'].iloc[0]})
        meanf.drop('Date', axis=1, inplace=True)
        mean = pd.merge(mean, meanf, how='outer', on='tag')
        print(f)

    mean = mean.T
    mean = mean.rename(columns=mean.loc['tag'])
    mean.drop('tag', axis=0, inplace=True)
    mean.sort_index(inplace=True)
    mean_begin = mean.iloc[:12].mean()
    mean_end = mean.iloc[-6:].mean()
    change = ((mean_end - mean_begin)*100/mean_begin).sort_values(ascending=False)
    change = change.dropna()
    change = change.astype('int64')
    change1 = change.sort_values()
    num_head = round(change.count()/2)
    change = pd.DataFrame({'winners': change.head(num_head).index, 'increase': change.head(num_head).values, \
            'losers': change1.head(num_head).index, 'decrease': change1.head(num_head).values}, index=[i for i in range(num_head)])
    #change.to_csv('chage.csv', encoding='utf-8')
    return change.head(30) 
    
for i in listdir('./tags/'):
    if i[:3] != 'res':
        x = csv_df('./tags/' + i + '/')
        x = x.shift()
        x.iloc[0] = ['-','-','-','-']
        x.to_csv('../Temp/README/' + i, sep='|', index=False)
        
x = csv_df('./fl/keywords_for_PowerBI/')
x = x.shift()
x.iloc[0] = ['-','-','-','-']
x.to_csv('../Temp/README/fl', sep='|', index=False)

x = csv_df('./freelancer/tags_for_PowerBI/')
x = x.shift()
x.iloc[0] = ['-','-','-','-']
x.to_csv('../Temp/README/freelancer', sep='|', index=False)

x = csv_df('./luxoft/keywords_for_PowerBI/')
x = x.shift()
x.iloc[0] = ['-','-','-','-']
x.to_csv('../Temp/README/luxoft', sep='|', index=False)

readme = ['### Changing tags from 2021 in %\nfreelancer.com\n']

f = open('../Temp/README/freelancer', 'r', encoding='utf-8')
readme.append(f.read())

for i in ('python', 'php', 'Java', 'Javascript', 'Typescript', 'Frontend', 'C%2B%2B', 'C%23', \
         'Golang', 'sql', 'Data scientist', 'data', 'spark', 'devops', 'intern', 'микросервис', \
         'EPAM'):
    if i[:3] != 'res':
        if i == 'C%23':
            readme.append('\nC#\n')
            f = open('../Temp/README/' + i, 'r', encoding='utf-8')
            readme.append(f.read())
        elif i == 'C%2B%2B':
            readme.append('\nC++\n')
            f = open('../Temp/README/' + i, 'r', encoding='utf-8')
            readme.append(f.read())
        else:
            readme.append('\n' + i + '\n')
            f = open('../Temp/README/' + i, 'r', encoding='utf-8')
            readme.append(f.read())

f = open('../Temp/README/luxoft', 'r', encoding='utf-8')
readme.append('\nluxoft\n' + f.read())

f = open('../Temp/README/fl', 'r', encoding='utf-8')
readme.append('\nfl.ru\n' + f.read())

f = open('README.md', 'w', encoding='utf-8')
x = ''.join(map(str, readme))
f.write(x.replace('.0', ''))
