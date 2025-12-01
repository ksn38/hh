import pandas as pd
from os import listdir
import numpy as np
from notebooks.lower_case import lower


lower('./tags/')

def new_dead(mypath):
    head = 1000
    
    begin = pd.read_csv(mypath + sorted(listdir(mypath))[0])[:head]
    begin = begin.rename(columns={'val': begin['Date'].iloc[0]})
    begin.drop('Date', axis=1, inplace=True)
    
    for f in sorted(listdir(mypath))[1:12]:
        beginf = pd.read_csv(mypath + f)[:head]
        beginf = beginf.rename(columns={'val': beginf['Date'].iloc[0]})
        beginf.drop('Date', axis=1, inplace=True)
        begin = pd.merge(begin, beginf, how='outer', on='tag')
        #print(f)

    end = pd.read_csv(mypath + sorted(listdir(mypath))[-1])[:head]
    end = end.rename(columns={'val': end['Date'].iloc[0]})
    end.drop('Date', axis=1, inplace=True)
    
    for f in sorted(listdir(mypath))[-5:-1]:
        endf = pd.read_csv(mypath + f)[:head]
        endf = endf.rename(columns={'val': endf['Date'].iloc[0]})
        endf.drop('Date', axis=1, inplace=True)
        end = pd.merge(end, endf, how='outer', on='tag')
        #print(f)

    new = pd.DataFrame({'tag': list(set(end.tag) - set(begin.tag))})
    new = new.merge(end, how='left', on='tag')
    new.index = new.tag
    new.drop('tag', axis=1, inplace=True)
    new = new.sum(axis=1).sort_values(ascending=False)
    new = new[new > 0.01]
    new = pd.DataFrame({'new': new.index})
    
    dead = pd.DataFrame({'tag': list(set(begin.tag) - set(end.tag))})
    dead = dead.merge(begin, how='left', on='tag')
    dead.index = dead.tag
    dead.drop('tag', axis=1, inplace=True)
    dead = dead.sum(axis=1).sort_values(ascending=False)
    dead = pd.DataFrame({'dead': dead.index})

    return new.join(dead).head(37)

def csv_df(mypath):
    mean = pd.read_csv(mypath + sorted(listdir(mypath))[0])
    mean = mean.rename(columns={'val': mean['Date'].iloc[0]})
    mean.drop('Date', axis=1, inplace=True)

    for f in sorted(listdir(mypath))[1:]:
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
    mean_end = mean.iloc[-5:].mean()
    change = ((mean_end - mean_begin)*100/mean_begin)
    change = change.dropna()
    change = change.astype('int64')
    x = pd.merge(mean.mean().rank().rename('mean_rank'), change.rank().rename('change_rank'), left_index=True, right_index=True)
    x = pd.merge(x, change.rename('percent'), left_index=True, right_index=True)
    x['rank'] = x['mean_rank']/3 + x['change_rank']
    change = x.sort_values('rank', ascending=False)
    x['rank1'] = (x['mean_rank'].max() - x['mean_rank'])/5 + x['change_rank']
    change1 = x.sort_values('rank1')
    num_head = int((change.count()/2)[0])
    change = pd.DataFrame({'winners': change.index[:num_head], '↑': change['percent'].iloc[:num_head].values, \
            'losers': change1.index[:num_head], '↓': change1['percent'].iloc[:num_head].values}, index=[i for i in range(num_head)])
    
    nd = new_dead(mypath)
    
    return change.join(nd).head(37) 

readme = ['## Changing tags from 2021 in %\n### freelancer.com\n']

freelancer = csv_df('./freelancer/tags_for_PowerBI/')
freelancer = freelancer.shift()
freelancer.iloc[0] = ['-','-','-','-','-','-']
freelancer = freelancer.to_csv(sep='|', lineterminator='\n', index=False)
readme.append(freelancer)

fl = csv_df('./fl/keywords_for_PowerBI/')
fl = fl.shift()
fl.iloc[0] = ['-','-','-','-','-','-']
fl = fl.to_csv(sep='|', lineterminator='\n', index=False)
readme.append('\n### fl.ru\n')
readme.append(fl)

luxoft = csv_df('./luxoft/keywords_for_PowerBI/')
luxoft = luxoft.shift()
luxoft.iloc[0] = ['-','-','-','-','-','-']
luxoft = luxoft.to_csv(sep='|', lineterminator='\n', index=False)
readme.append('\n### luxoft\n')
readme.append(luxoft)

for i in ('EPAM', 'Python', 'php', 'Java', 'Javascript', 'Frontend', 'C%2B%2B', 'C%23', \
         'Golang', 'SQL', 'Data scientist', 'Data', 'DevOps', 'Intern', 'Intern_cyr', 'микросервис'):
        if i[:3] != 'res':
          if i == 'C%23':
              readme.append('\n### C#\n')
              x = csv_df('./tags/' + i + '/')
              x = x.shift()
              x.iloc[0] = ['-','-','-','-','-','-']
              x = x.to_csv(sep='|', lineterminator='\n', index=False)
              readme.append(x)
          elif i == 'C%2B%2B':
              readme.append('\n### C++\n')
              x = csv_df('./tags/' + i + '/')
              x = x.shift()
              x.iloc[0] = ['-','-','-','-','-','-']
              x = x.to_csv(sep='|', lineterminator='\n', index=False)
              readme.append(x)
          else:
              readme.append('\n### ' + i + '\n')
              x = csv_df('./tags/' + i + '/')
              x = x.shift()
              x.iloc[0] = ['-','-','-','-','-','-']
              x = x.to_csv(sep='|', lineterminator='\n', index=False)
              readme.append(x)

f = open('README.md', 'w', encoding='utf-8')
x = ''.join(map(str, readme))
f.write(x.replace('.0', ''))
