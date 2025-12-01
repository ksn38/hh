import pandas as pd
from os import listdir
import re
from os.path import isfile, join
from collections import Counter
import time


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
            df = df[df['tag'].str.len() > 1]
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
            df[['Date', 'tag', 'val']].iloc[:99].to_csv(self.output_path + '/' + f, index=False, encoding='utf-8', sep=',')

Data_for_PowerBI_hh('../Temp/tags/Intern/', '\d|[А-яё]', 'tags/Intern_cyr').norm_and_save_files()
t1 = time.time()
dirs = listdir('../Temp/tags/')
for d in dirs:
    Data_for_PowerBI_hh('../Temp/tags/' + d, r'\d|[A-z]', 'tags/' + d).norm_and_save_files()
t2 = time.time() - t1

'''import threading

threads = []
# Создаем и запускаем 5 потоков
for d in dirs:
    thread = threading.Thread(target=Data_for_PowerBI_hh('../Temp/tags/' + d, r'\d|[A-z]', 'tags/' + d).norm_and_save_files)
    threads.append(thread)
    thread.start()

# Ожидаем завершения всех потоков
for thread in threads:
    thread.join()
    
print(t2)
print(time.time() - t1)'''


mypath = 'luxoft/source/'
files = listdir(mypath)

for file in files:
    print(file)
    keywords = []
    headers = pd.read_csv(mypath + file, header=None)[0].to_list()
    headers.extend(pd.read_csv(mypath + file, header=None)[1].to_list())
    for i in headers:
        i = i.replace('/ ', ' ')
        i = re.sub(r'[^A-z+#.\/-]', ' ', i)
        for word in ('Data', 'Capital', 'Back', 'Front', 'Functional', 'System', \
                    'Business', 'Delivery', 'Loan', 'Technical', 'Algorithm'):
            i = re.sub(r'' + word + '\s', word + '_', i)
        for word in ('Mode', 'Manager', 'Management', 'Analyst', 'speaker', 'Kernel', \
                    'Administrator', 'Learning', 'end', 'Stack', 'Lead', 'engine', \
                    'Framework', 'Test', 'Cyber', 'Office', 'Service', 'Business', \
                    'Design', 'Architecture', 'Security', 'Administration', 'Master', \
                    'Architect', 'Programmer', 'Analysis', 'Engine'):
            i = re.sub(r'\s' + word, '_' + word, i)
        i = i.split(' ')
        for j in i:
            if len(j) > 1 and j not in ('with', 'and', 'IT', 'to', 'in', 'for', 'or', 'Specialist', \
                                        'Development', 'developer', 'Developer', 'experience', 'of', \
                                        'Project', 'Coordinator', 'Developer', 'Solution', 'Expert', \
                                        'Product', 'Software', 'Release', 'Production', 'Owner', \
                                        'Application', 'Techno', 'Information', 'is', 'etc.', 'specific', \
                                        'Specific', 'Facilities', 'Benefits', 'Compensation', 'Packaged', \
                                        'Informatica', 'Vendor', 'BO', 'IQ', 'Center', 'Consulting', \
                                        'Infrastructure', 'Trainer', 'Professional', 'Practice', 'Assistant', \
                                        'Integrated', 'Candidate', 'Corporate', 'Domain', 'Contracting', \
                                        'Platform', 'Processing', 'Adventurer', 'exp', 'exp.', 'Engineering'):
                keywords.append(j)


    df = pd.DataFrame(sorted(Counter(keywords).items(), key=lambda x: x[1], reverse=True), columns=['tag', 'val']).iloc[:149]
    df['norm_val'] = df.val/df.val.iloc[0]
    df['val'] = df['norm_val']
    df['Date'] = re.findall('[0-9]{4}-[0-9]{2}-[0-9]{2}', file)[0]
    df[['Date', 'tag', 'val']].to_csv('luxoft/keywords_for_PowerBI' + '/' + file, index=False, encoding='utf-8', sep=',')
