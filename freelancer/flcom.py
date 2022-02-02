import pandas as pd
from os import listdir
import re


mypath = 'tags'
files = listdir(mypath)

for k in files:
    df = pd.read_csv(mypath + '/' + k)
    df.columns = ['tag', 'val']
    #df['norm_val'] = df.val/df.val.iloc[0]
    df['Date'] = re.findall('[0-9]{4}-[0-9]{2}-[0-9]{2}', k)[0]
    df[['Date', 'tag', 'val']].iloc[:299].to_csv('tags_for_PowerBI' + '/' + k, index=False, encoding='utf-8', sep=',')
