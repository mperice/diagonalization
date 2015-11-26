__author__ = 'matic'


__author__ = 'matic'
from os import listdir

path='mtrees2014.txt'
#files = [ f for f in listdir(path) if f!="synonims.txt" ]
ofile='toplevels.txt'
level2=[]
#for file in files:
with open(path,'r') as input_file:
    for line in input_file:
        if line.strip()!="":
            print line
            split=line.split("\n")[0].split(";")
            level_split=split[1].split(".")
            if len(level_split)==1:
                level2.append((level_split[0],split[0]))

level1=[
['A','Anatomy',[]],
['B','Organisms',[]],
['C','Diseases',[]],
['D','Chemicals and Drugs',[]],
['E','Analytical, Diagnostic and Therapeutic Techniques and Equipment',[]],
['F','Psychiatry and Psychology',[]],
['G','Phenomena and Processes',[]],
['H','Disciplines and Occupations',[]],
['I','Anthropology, Education, Sociology and Social Phenomena',[]],
['J','Technology, Industry, Agriculture',[]],
['K','Humanities',[]],
['L','Information Science',[]],
['M','Named Groups',[]],
['N','Health Care',[]],
['V','Publication Characteristics',[]],
['Z','Geographicals',[]]
]
for abb,text in level2:
    index=[a[0] for a in level1].index(abb[0])
    level1[index][2].append((abb,text))

import json
with open(ofile,'w') as output_file:
    json.dump(level1,output_file)
