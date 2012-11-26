'''
Created on 30. avg. 2012

@author: matic
'''

import random,string
from math import log
from collections import defaultdict

def generate_random(prefix,words_per_doc):
    #ROW ORDERING
    if 1==1:
        mig_mag_file=open(prefix+"all/documents.lndoc", 'r')
        #hevristic_scores="all/HevristicsScores.txt"
        every=5
    
    line = mig_mag_file.readline()    # Invokes readline() method on file
    trains_text={}
    trains_class={}
    
    
    i=0
    count=0
    
    while line:
        if line!="\n" and i%every==0:
            spl=line.split("\t")
            print spl
            trains_class[count]=spl[1]
            trains_text[count]=spl[2].split("\n")[0].split(" ")
            #print i,spl[0]
            count+=1
        i+=1
        line = mig_mag_file.readline()
    #print "row_perm:",row_perm_rev
    mig_mag_file.close()
    
    
    #TF-IDF and BOW
    words = set()
    tf_idfs = {}
    
    for train in trains_text.keys():
        for word in trains_text[train]:
            words.add(word)
    
    word_count=defaultdict(int)
    
    for train_words in trains_text.values():
        for word in set(train_words):
            word_count[word]+=1
    

    out_file = open(prefix+"random"+str(words_per_doc)+"/documents.lndoc", "wb")
    #f = open('trains.tab','w')
    
    for i in range(len(trains_class)):
        out_file.write(str(i+1)+"\t"+(random.choice(["MIG","MAG"]))+"\t"+string.join(random.sample(words,words_per_doc)," ")+"\n")
    
    out_file.close()
#    print "writting to file",len(sorted_words)

    return "random"+str(words_per_doc)



#generate_random(5)