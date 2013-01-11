__author__ = 'matic'
import os,re

#replaces all keys from dict with its' values
def replace_all(text, dic):
    for i, j in sorted(dic.iteritems(),key=lambda a: len(a[0].split(" ")),reverse=True):
        #print i
        i=i.replace("[","\[").replace("]","\]").replace("(","\(").replace(")","\)").replace(".","\.").replace("'","\'")
        rxstr=r'(?:(?<=\s)|(?<=^))'+i+r'(?=\s|$)'
        count=len(re.findall(rxstr, text))
        #print i
        #text = re.sub(r'(?i)\b'+i+r'\b', j, text)#text.replace(i, j)
        text = re.sub(rxstr, j, text)
    return text,count

def count(file_name, dic):
    file_name=file_name.split(".")[0]
    fajl=open(file_name+".txt", 'r')
    line = fajl.readline()
    cnt=0
    while line:
        if line!="\n":
            for word in dic.keys():
                a=line.count(word)
                #print word,a
                cnt+=a

        line = fajl.readline()
    fajl.close()
    return cnt


def use_domain_dictionary(file_name,dictionaries_path):
    file_name=file_name.split(".")[0]
    dictionary={}
    dict_names=os.listdir(dictionaries_path)

    for dict_name in dict_names:
        fajl=open(dictionaries_path+"/"+dict_name, 'r')


        line = fajl.readline()    # Invokes readline() method on file

        while line:
            if line!="\n":
                #spl=line.split("\t")
                #print dict_name
                #print dict_name
                terms=line.replace("_"," ").replace("\n ","\n").split("\n")[0].replace("  "," ").replace("  "," ").replace(", ",",").split(",")
                terms=[asd for asd in terms if asd!=""]
                first_term=terms[0]

                for term in terms:
                    dictionary[term]=first_term
            line = fajl.readline()
            #print "row_perm:",row_perm_rev
        fajl.close()
    print dictionary

    bterms_fajl=open(file_name+"_dict_keys.txt", 'w')
    for bterm in set(dictionary.values()):
        bterms_fajl.write(bterm+",")
    bterms_fajl.close()


    fajl=open(file_name+".txt", 'r')
    new_fajl=open(file_name+"_dict.txt", 'w')

    line = fajl.readline()    # Invokes readline() method on file
    count=0
    while line:
        if line!="\n":
            lod=line.split("\n")[0]
            replaced,countt=replace_all(lod,dictionary)
            new_fajl.write(replaced+"\n")
            count+=countt
        line = fajl.readline()
        #print "row_perm:",row_perm_rev
    fajl.close()
    new_fajl.close()

    print count#(file_name+"_dict.txt",dictionary)

#use_domain_dictionary("pdr","dictionaries")

