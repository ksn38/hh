import pandas as pd
import numpy as np
from os import listdir
import re


mypath = 'fl/keywords'
files = listdir(mypath)

for k in files:
    df = pd.read_csv(mypath + '/' + k)
    df.columns = ['tag', 'val']
    df['norm_val'] = df.val/df.val.iloc[0]
    df['Date'] = re.findall('[0-9]{4}-[0-9]{2}-[0-9]{2}', k)[0]
    df[['Date', 'tag', 'norm_val']].iloc[:149].to_csv('fl/keywords_norm' + '/' + k, header=False, index=False, encoding='utf-8', sep=',')
