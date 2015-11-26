print "start\tOK"


import os
import sys,string
os.chdir('C:\Users\matic\workspace\crossbee\crossbee\Content\Data')
print os.getcwd()
from collections import defaultdict
from math import log

from diagonalization_helpers import *
from pyroc import ROCData,plot_multiple_roc

import json
prefix=""
every=1

#full_text_file=open(prefix+"document_raw.txt", 'r')
#hevristic_scores=prefix+"HevrisitcsScores.txt"
#fline = full_text_file.readline()    # Invokes readline() method on file
text_per_document={}
full_text_per_document={}
class_per_document={}

# >>> import hashlib
# >>> int(hashlib.md5('Hello, world!').hexdigest(), 16)
# 144653930895353261282233826065192032313L

count=0
#CONVERT DOCUMENT STRING TO
prefix=sys.argv[1]+"/"
print "File in:", prefix
#prefix='C:\\Users\\matic\\AppData\\Local\\Temp\\aahpoqs5.lcp\\'
dataset_file=open(prefix+"documents.lndoc", 'r')
line = dataset_file.readline()    # Invokes readline() method on file
text_per_document={}
class_per_document={}


i=0
count=0

while line:
    if line!="\n" and i%every==0:
        spl=line.split("\t")
        class_per_document[count]=spl[1]
        text_per_document[count]=spl[2].split("\n")[0].split(" ")
        if "" in text_per_document[count]:
            text_per_document[count].remove("")

        count+=1
    i+=1
    line = dataset_file.readline()
dataset_file.close()
classes=list(set(class_per_document.values()))

#TF-IDF and BOW
words = set()
tf_idfs = {}

for train in text_per_document.keys():
    for word in text_per_document[train]:
        words.add(word)

word_count=defaultdict(int)
for document_text in text_per_document.values():
    for word in set(document_text):
        word_count[word]+=1

len_train_text=len(text_per_document)
words_sorted_by_frequency=sorted(word_count.items(),key=lambda a: a[1],reverse=True)
#-----------------CALCULATE TF-IDFS-----------------
print "compute tf-idf"
for train, train_words in text_per_document.items():
    train_word_count=defaultdict(int)
    tf_idfs[train] = {}
    for word in train_words:
        train_word_count[word]+=1
    
    for word,tf in train_word_count.items():
        idf = log(len_train_text / float(word_count[word]))
        tf_idfs[train][word] = tf * idf


sorted_words = sorted(list(words))
#nums=0
#tfnnull=0
#max_tfidf=max([item for t in tf_idfs.values() for item in t.values()])


with_inverse=False
inverse_only=False

# if with_inverse:
#     write_to_init_file_inv(class_per_document,text_per_document,sorted_words,prefix+"init.dat_inv")
#     write_to_init_file(class_per_document,text_per_document,sorted_words,prefix+"init.dat")
#     _,col_perm_rev_inv=get_permutations(prefix,filename=prefix+"init_inv.dat")
#     col_perm_rev,row_perm_rev=get_permutations(prefix,filename=prefix+"init.dat")
# elif inverse_only:
#     col_perm_rev_inv=False
#     write_to_init_file_inv(class_per_document,text_per_document,sorted_words,prefix+"init.dat_inv")
#     col_perm_rev,row_perm_rev=get_permutations(prefix,filename=prefix+"init_inv.dat")
# else:
col_perm_rev_inv=False
write_to_init_file(class_per_document,text_per_document,sorted_words,prefix+"init.dat")
col_perm_rev,row_perm_rev=get_permutations(prefix)

col_perm={}
for k,v in col_perm_rev.items():
    col_perm[v]=k

col_perm_inv=False
if col_perm_rev_inv:
    col_perm_inv={}
    for k,v in col_perm_rev_inv.items():
        col_perm_inv[v]=k



#-----------------CROSSBEE SCORES-----------------
jursic_word_score=False
max_word_score=False

#-----------------HEVRISTICS-----------------
from hevristic_functions import *

print len(sorted_words),len(row_perm_rev),len(col_perm_rev)
greens_per_word,blues_per_word=calculate_colours(prefix,sorted_words,row_perm_rev,col_perm_rev,class_per_document,classes)
greens_on_diag_per_word,blues_on_diag_per_word=calculate_diag_colours(prefix,sorted_words,row_perm_rev,col_perm_rev,class_per_document,classes)
labels=['Hevristika1','Hevristika2','Hevristika3','Hevristika4']


hevristics=[hevristic1,hevristic2,hevristic3,hevristic4]
scores=[sorted(hevristic(greens_per_word,blues_per_word,greens_on_diag_per_word,blues_on_diag_per_word),key=lambda a: (1 if greens_per_word.get(a[0])!=0 and blues_per_word.get(a[0])!=0 else 0),reverse=True) for hevristic in hevristics]



#b-term generation
# if sell!="ideal_toy":
#     b_term_list=['5_ht','5_hydroxytryptamine','5_hydroxytryptamine_receptor','anti_aggregation','anticonvulsant','anti_inflammatory','antimigraine','arterial_spasm','brain_serotonin','calcium_antagonist','calcium_blocker','calcium_channel','calcium_channel_blocker','cerebral_vasospasm','convulsion','convulsive','coronary_spasm','cortical_spread_depression','diltiazem','epilepsy','epileptic','epileptiform','hypoxia','indomethacin','inflammatory','nifedipine','paroxysmal','platelet_aggregation','platelet_function','prostacyclin','prostaglandin','prostaglandin_e1','prostaglandin_synthesis','reactivity','seizure','serotonin','spasm','spread','spread_depression','stress','substance_p','vasospasm','verapamil']
#
# b_terms=set(word for word in b_term_list if greens_per_word.get(word)!=0 and blues_per_word.get(word)!=0)
#
# print [(word,greens_per_word.get(word),blues_per_word.get(word)) for word in b_term_list]
# print b_term_list
# print b_terms
b_terms=set([])
#-----------------DRAW IMAGES-----------------
draw_matrix(sorted_words,jursic_word_score,max_word_score,identity_permutation(len(col_perm_rev)),identity_permutation(len(row_perm_rev)),class_per_document,
    prefix+"1_inital",prefix+"init",b_terms,{},classes)
draw_matrix(sorted_words,jursic_word_score,max_word_score,col_perm_rev,row_perm_rev,class_per_document,
    prefix+"2_after_col_perm",prefix+"min_flips_output_2_columns_permuted_matrix",b_terms,col_perm_inv,classes)
draw_matrix(sorted_words,jursic_word_score,max_word_score,col_perm_rev,row_perm_rev,class_per_document,
    prefix+"3_banded_matrix",prefix+"min_flips_output_6_visual_banded_matrix",b_terms,col_perm_inv,classes)
draw_matrix(sorted_words,jursic_word_score,max_word_score,col_perm_rev,row_perm_rev,class_per_document,
    prefix+"5_after_row_perm",prefix+"min_flips_output_7_original_banded_matrix",b_terms,col_perm_inv,classes)

#-----------------GENERATE JAVASCRIPT FILE-----------------

#doc_outliers=find_domain_outliers(prefix,class_per_document)
#generate_js_file(sorted_words,jursic_word_score,max_word_score,col_perm_rev,row_perm_rev,class_per_document,text_per_document,prefix,b_terms,greens_per_word,blues_per_word,classes,col_perm_rev_inv,col_perm_inv,doc_outliers)

#-----------------PLOT ROC-----------------
print "Results"
#create image where word columns are sorted by hevristic4 scores
best_hevristic_scores_permutation={}
hevristic_4_words_by_score=[a[0] for a in scores[3]]
missing_j=len(hevristic_4_words_by_score)
for j,old_j in col_perm_rev.items():
    word=sorted_words[old_j]
    if word in hevristic_4_words_by_score:
        score_j=hevristic_4_words_by_score.index(word)
    else:
        score_j=missing_j
        missing_j+=1

for word,score in scores[3]:
    print "%s\t%d" % (word,score)

draw_matrix(sorted_words,jursic_word_score,max_word_score,col_perm_rev,row_perm_rev,class_per_document,
    prefix+"6_after_scores_perm",prefix+"min_flips_output_7_original_banded_matrix",b_terms,best_hevristic_scores_permutation,classes)


#print json.dumps(word,score in scores[3])

