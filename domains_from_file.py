__author__ = 'matic'


from collections import defaultdict
from domain_dictionaries import use_domain_dictionary
import os

def generate_from_files(prefix,domainA,klassA,domainC,klassC,ouput_file_name,dictionary_dir=False):
    filename=prefix+"/"+ouput_file_name
    open(filename, "w").close()

    file_namesA=set(os.listdir(prefix+"/"+domainA))
    file_namesC=set(os.listdir(prefix+"/"+domainC))

    interestion= file_namesA.intersection(file_namesC)
    generate_for_one_domain(prefix,domainA,klassA,interestion,filename)
    generate_for_one_domain(prefix,domainC,klassC,interestion,filename)
    print interestion

    if dictionary_dir:
        use_domain_dictionary(filename,prefix+"/"+dictionary_dir)


def generate_for_one_domain(prefix,dir_name,klass,file_name_not_in,full_output_file_name):
    i=1+ sum(1 for line in open(full_output_file_name)) #lines already in file

    output_file=open(full_output_file_name, 'a')
    file_names=os.listdir(prefix+"/"+dir_name) #all files in dir
    for dict_name in file_names:
        if dict_name not in file_name_not_in:
            fajl=open(prefix+"/"+dir_name+"/"+dict_name, 'r')
            text=fajl.read().replace("\n ","\n").replace("\n"," ").replace("  "," ").replace("  "," ")
            text=text[1:-1] if text[0]==" " else text
            #print dict_name, text
            output_file.write(str(i)+"\t!"+klass+"\t"+text+"\n")
            #print i
            i+=1


    output_file.close()


#generate_from_files("D:/diagonalization/kenyan/KenyanData/","TekstiLO","LO","TekstiWE","WE","kenyan.txt")
#generate_from_files("D:/diagonalization/et_sa_abstracts","ET publications","ET","SA publications","SA","documents.txt","dictionaries")