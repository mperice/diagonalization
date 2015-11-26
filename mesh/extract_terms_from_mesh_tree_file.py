__author__ = 'matic'
from os import listdir
from collections import defaultdict

path='mesh_d2015.txt'
#files = [ f for f in listdir(path) if f!="synonims.txt" ]
ofile='mesh_terms_per_category.json'
level2=[]
category_of_a_terms=defaultdict(set)
entries=set()
#for file in files:
with open(path,'r') as input_file:
    for line in input_file:
        if line.strip()!="":
            if line.startswith("*NEWRECORD"):
                entries=set()
            elif line.startswith("MH = "):
                mesh_head=line[5:-1]
                entries.add(mesh_head.lower())
            elif line.startswith("ENTRY = "):
                new_entries=line[8:-1].split("|")
                for new_entry in new_entries:
                    entries.add(new_entry.lower())

            elif line.startswith("MN = "):
                category=line[5:-1].split(".")[0]

                for entry in entries:
                    ##PUT ADJECTIVES IN FRONT
                    #print entry
                    if not " and " in entry:
                        print entry
                        spl_entry=entry.split(", ")
                        spl_entry.reverse()

                        entry=" ".join(spl_entry)
                    category_of_a_terms[entry]=category



#print terms_per_category
# import cPickle
#
# with open(ofile,'w') as output_file:
#     cPickle.dump(category_of_a_terms,output_file)

mesh_terms_per_category=defaultdict(list)

for term,category in category_of_a_terms.items():
    mesh_terms_per_category[category].append(term)


# for k,v in mesh_terms_per_category.items():
#     mesh_terms_per_category[k]=list(v)
import json
json.dump(dict(mesh_terms_per_category),open(ofile,'w'))