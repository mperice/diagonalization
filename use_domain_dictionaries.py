__author__ = 'matic'
import os


#replaces all keys from dict with its' values
def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

def count(file_name, dic):
    fajl=open(file_name+".lndoc", 'r')
    line = fajl.readline()
    cnt=0
    while line:
        if line!="\n":
            for word in dic.keys():
                cnt+=line.count(word)

        line = fajl.readline()
    fajl.close()
    return cnt


def use_domain_dictionary(file_name,dictionaries_path):

    dictionary={}
    dict_names=os.listdir(dictionaries_path)

    for dict_name in dict_names:
        fajl=open(dictionaries_path+"/"+dict_name, 'r')


        line = fajl.readline()    # Invokes readline() method on file

        while line:
            if line!="\n":
                #spl=line.split("\t")
                #print dict_name

                terms=line.split("\n")[0].split(",")
                first_term=terms[0]
                for term in terms:
                    dictionary[term]=first_term
            line = fajl.readline()
            #print "row_perm:",row_perm_rev
        fajl.close()
    print dictionary


    fajl=open(file_name+".lndoc", 'r')
    new_fajl=open(file_name+"_dict.lndoc", 'w')

    line = fajl.readline()    # Invokes readline() method on file

    while line:
        if line!="\n":
            lod=line.split("\n")[0]
            new_fajl.write(replace_all(lod,dictionary)+"\n")
        line = fajl.readline()
        #print "row_perm:",row_perm_rev
    fajl.close()
    new_fajl.close()

    print count(file_name+"_dict.lndoc",dictionary)

use_domain_dictionary("pdr","dictionaries")

