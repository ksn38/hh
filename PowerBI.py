import pandas as pd
from os import listdir
import re
from os.path import isfile, join
from collections import Counter
import pandas as pd


class Data_for_PowerBI:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.files = listdir(self.input_path)

    def open_file(self, file):
        df = pd.read_csv(self.input_path + '/' + file)
        df['Date'] = re.findall('[0-9]{4}-[0-9]{2}-[0-9]{2}', file)[0]
        print(self.input_path + '/' + file)
        return df[['Date', 'tag', 'val']]


class Data_for_PowerBI_fl_freelancer(Data_for_PowerBI):
    def __init__(self, input_path, output_path):
        super().__init__(input_path, output_path)
            
    def norm_and_save_files(self):
        for f in self.files:
            df = self.open_file(f)
            df['norm_val'] = df.val/df.val.iloc[0]
            df['val'] = df['norm_val']
            df[['Date', 'tag', 'val']].iloc[:149].to_csv(self.output_path + '/' + f, index=False, encoding='utf-8', sep=',')
    

Data_for_PowerBI_fl_freelancer('freelancer/tags', 'freelancer/tags_for_PowerBI').norm_and_save_files()
Data_for_PowerBI_fl_freelancer('fl/keywords', 'fl/keywords_for_PowerBI').norm_and_save_files()


class Data_for_PowerBI_hh(Data_for_PowerBI):
    def __init__(self, input_path, reg, output_path):
        super().__init__(input_path, output_path)
        self.reg = reg

    def norm_and_save_files(self):
        for f in self.files:
            df = self.open_file(f)
            df = df[df['tag'].map(lambda x: len(re.findall(self.reg, x))) > 0]
            df['norm_val'] = df.val/df.val.iloc[0]
            df.val = df['norm_val']
            df[['Date', 'tag', 'val']].iloc[:74].to_csv(self.output_path + '/' + f, index=False, encoding='utf-8', sep=',')

Data_for_PowerBI_hh('../Temp/tags/Intern/', '\d|[А-яё]', 'tags/Intern_cyr').norm_and_save_files()

dirs = listdir('../Temp/tags/')
for d in dirs:
    Data_for_PowerBI_hh('../Temp/tags/' + d, '\d|[A-z]', 'tags/' + d).norm_and_save_files()


mypath = 'luxoft/source/'
files = listdir(mypath)

for file in files:
    keywords = []
    headers = pd.read_csv(mypath + file, header=None)[1].to_list()
    for i in headers:
        i = re.sub('[^A-z+#]', ' ', i)
        i = re.sub('Data\s', 'Data_', i)
        i = re.sub('\sManager', '_Manager', i)
        i = re.sub('\sAnalyst', '_Analyst', i)
        i = i.split(' ')
        for j in i:
            if j != '' and len(j) > 1:
                keywords.append(j)

    df = pd.DataFrame(sorted(Counter(keywords).items(), key=lambda x: x[1], reverse=True), columns=['tag', 'val']).iloc[:99]
    df['norm_val'] = df.val/df.val.iloc[0]
    df['val'] = df['norm_val']
    df['Date'] = re.findall('[0-9]{4}-[0-9]{2}-[0-9]{2}', file)[0]
    df[['Date', 'tag', 'val']].to_csv('luxoft/keywords_for_PowerBI' + '/' + file, index=False, encoding='utf-8', sep=',')
