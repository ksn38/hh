import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
import re


mypath = 'E:\\Temp\\tags\\'
dirs = listdir(mypath)

for j in dirs:
    files = [i for i in listdir(mypath + j) if isfile(join(mypath + j, i))]
    
    for k in files:
        df = pd.read_csv(mypath + j + '\\' + k)
        df.columns = ['tag', 'val']
        df = df[df['tag'].map(lambda x: len(re.findall('\d|[A-z]', x))) > 0]        
        df['norm_val'] = df.val/df.val.iloc[0]
        df['Date'] = re.findall('[0-9]{4}-[0-9]{2}-[0-9]{2}', k)[0]
        df[['Date', 'tag', 'norm_val']].iloc[:49].to_csv('C:\\Users\\ksn\\hh\\tags\\' + j + '\\' + k, header=False, index=False, encoding='utf-8', sep=',')
