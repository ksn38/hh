import pandas as pd
from os import listdir
import numpy as np
import re


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
    change.to_csv('csv/' + re.findall('\D+', f)[0] + '_change.csv', sep=',', encoding='utf-8')

for i in ('python', 'php', 'Java', 'Javascript', 'Typescript', 'Frontend', 'C%2B%2B', \
         'Golang', 'sql', 'Data scientist', 'data', 'spark', 'devops', 'intern', 'микросервис', \
         'EPAM'):
    if i[:3] != 'res':
        x = csv_df('../tags/' + i + '/')

freelancer = csv_df('../freelancer/tags_for_PowerBI/')
luxoft = csv_df('../luxoft/keywords_for_PowerBI/')
fl = csv_df('../fl/keywords_for_PowerBI/')

