__author__ = 'matic'
from os import listdir

path='tair'
files = [ f for f in listdir(path) if f!="synonims.txt" ]
ofile='tair\\synonyms.txt'
print files
with open(ofile,'w') as output_file:
    for file in files:
        with open(path+'\\'+file,'r') as input_file:
            i=0
            for line in input_file:
                if i>0 and line.strip()!="":
                    split=line.split("\t")
                    #print split
                    if len(split)>1:
                        output_file.write(split[1])
                        if len(split)>5:
                            output_file.write("\t"+split[5].replace(";",","))
                        output_file.write("\n")
                i+=1


#sinonime s TAIR-a za Arabidopsis thaliano