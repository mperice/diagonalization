'''
Created on 17. avg. 2012

@author: matic
'''

from collections import defaultdict

def read_scores_from_file(txt):
    word_score=defaultdict(float)
    #ROW ORDERING
    
    try:
        hev_file=open(txt, 'r')
    except IOError as e:
        #print txt
        return False

    line = hev_file.readline()
    line = hev_file.readline()    # Invokes readline() method on file

    while line:
        if line!="\n":
            spl=line.split("\t")
            word_score[spl[1]]=float(spl[-1].split("\n")[0])
            

        line = hev_file.readline()
        
    hev_file.close()
    #print word_score
    return word_score
#read_scores_from_file()