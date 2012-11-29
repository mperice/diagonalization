'''
Created on 30. avg. 2012

@author: maticfg
'''

import random,string
from math import log
from collections import defaultdict

def generate_ideal(prefix,words_per_doc,corpus_per_cluster,percentage=0.01):
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
    

    words = set()

    
    tf_idfs = {}
    
    for train in trains_text.keys():
        for word in trains_text[train]:
            words.add(word)
            


    
    first_domain_corpus=set()
    second_domain_corpus=set()

    
    cluster_corpuses=[]
    for i in range(6):
        set1=set(random.sample(words, corpus_per_cluster))
        words-=set1
        
        if i%2==0:
            first_domain_corpus|=set1
        else:
            second_domain_corpus|=set1
            
        cluster_corpuses.append(set1)
    
    connecting_words_first=list(first_domain_corpus)[:8]
    connecting_words_second=list(second_domain_corpus)[:8]
    
    out_file = open(prefix+"ideal_toy/documents.lndoc", "wb")
    #f = open('trains.tab','w')
    
    
    for i,cluster_corpus in enumerate(cluster_corpuses):
        for j in range(20):
            selected_connecting_words=[w for w in (connecting_words_first if i%2==1 else connecting_words_second) if random.random()<percentage]
            print selected_connecting_words
            out_file.write(str(i*20+j+1)+"\t"+(["MIG","MAG"][i%2])+"\t"+string.join(random.sample(cluster_corpus,words_per_doc)+selected_connecting_words," ")+"\n")
            

    
    out_file.close()
#    print "writting to file",len(sorted_words)

    return "random"+str(words_per_doc),connecting_words_first+connecting_words_second



#generate_ideal(15,20)


