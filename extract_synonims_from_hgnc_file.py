__author__ = 'matic'


__author__ = 'matic'
from os import listdir

path='C:\\Users\\matic\\Desktop\\crossbee-terms-human\\hgnc'
files = [ f for f in listdir(path) if f!="synonims.txt" ]
ofile='C:\\Users\\matic\\Desktop\\crossbee-terms-human\\hgnc\\synonims.txt'
print files
with open(ofile,'w') as output_file:
    for file in files:
        with open(path+'\\'+file,'r') as input_file:
            for line in input_file:
                if line.strip()!="":
                    split=line.split("\t")
                    if split[1]!='':
                        output_file.write(split[1]+"\t"+split[5]+"\n")