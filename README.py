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

readme = ['### Changing tags from 2021 in %\nfreelancer.com\n']

freelancer = csv_df('./freelancer/tags_for_PowerBI/')
freelancer = freelancer.shift()
freelancer.iloc[0] = ['-','-','-','-']
freelancer = freelancer.to_csv(sep='|', index=False).replace('\n', '')
readme.append(freelancer)

for i in ('python', 'php', 'Java', 'Javascript', 'Typescript', 'Frontend', 'C%2B%2B', 'C%23', \
         'Golang', 'sql', 'Data scientist', 'data', 'spark', 'devops', 'intern', 'микросервис', \
         'EPAM'):
        if i[:3] != 'res':
          if i == 'C%23':
              readme.append('\nC#\n')
              x = csv_df('./tags/' + i + '/')
              x = x.shift()
              x.iloc[0] = ['-','-','-','-']
              x = x.to_csv(sep='|', index=False).replace('\n', '')
              readme.append(x)
          elif i == 'C%2B%2B':
              readme.append('\nC++\n')
              x = csv_df('./tags/' + i + '/')
              x = x.shift()
              x.iloc[0] = ['-','-','-','-']
              x = x.to_csv(sep='|', index=False).replace('\n', '')
              readme.append(x)
          else:
              readme.append('\n' + i + '\n')
              x = csv_df('./tags/' + i + '/')
              x = x.shift()
              x.iloc[0] = ['-','-','-','-']
              x = x.to_csv(sep='|', index=False).replace('\n', '')
              readme.append(x)
        
luxoft = csv_df('./luxoft/keywords_for_PowerBI/')
luxoft = luxoft.shift()
luxoft.iloc[0] = ['-','-','-','-']
luxoft = luxoft.to_csv(sep='|', index=False).replace('\n', '')
readme.append('\nluxoft\n')
readme.append(luxoft)

fl = csv_df('./fl/keywords_for_PowerBI/')
fl = fl.shift()
fl.iloc[0] = ['-','-','-','-']
fl = fl.to_csv(sep='|', index=False).replace('\n', '')
readme.append('\nfl.ru\n')
readme.append(fl)

f = open('README.md', 'w', encoding='utf-8')
x = ''.join(map(str, readme))
f.write(x.replace('.0', ''))
