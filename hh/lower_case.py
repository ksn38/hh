import pandas as pd
from os import listdir
from collections import Counter
import re

def lower(mypath):
    tags = []

    for d in listdir(mypath):
        for f in listdir(mypath + d +'/'):
            df = pd.read_csv(mypath + d +'/' + f)
            tags.extend(df.tag)
            print(f)

    set_tags = set(tags)
    tags = list(set_tags)
    tags = [i.lower() for i in tags]
    target_tags = [k for k, v in Counter(tags).items() if v > 1]

    for d in listdir(mypath):
        for f in listdir(mypath + d +'/'):
            df = pd.read_csv(mypath + d +'/' + f)
            for i, t in zip(df.index, df.tag):
                if t.lower() in set(target_tags):
                    df.at[i, 'tag'] = t.lower()
            df[['Date', 'tag', 'val']].to_csv(mypath + d +'/' + f, index=False, encoding='utf-8', sep=',')
            if max(Counter(df.tag).values()) > 1:
                df = df.groupby(['tag'], as_index=False).sum()
                df['Date'] = re.findall('[0-9]{4}-[0-9]{2}-[0-9]{2}', f)[0]
                df[['Date', 'tag', 'val']].to_csv(mypath + d +'/' + f, index=False, encoding='utf-8', sep=',')
