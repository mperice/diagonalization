import os
import sys,string

from collections import defaultdict
from math import log
from create_random import generate_random
from create_ideal_world import *
from diagonalization_helpers import *
from pyroc import ROCData,plot_multiple_roc
from domain_outliers import find_domain_outliers
from domains_from_pubmed import abstracts_for_terms
from domains_from_file import generate_from_files
from domain_dictionaries import use_domain_dictionary
import random
print os.getenv('COMPUTERNAME')

if os.getenv('COMPUTERNAME')=="PORFAVOR-PC":
    prefix="D:/diagonalization/"
elif os.getenv('COMPUTERNAME')=='BOJAN_HP':
    prefix="W:/diagonalization/"
else:
    prefix="/home/matic/"

fetch_documents=True and False
sell=sys.argv[1]
#ROW ORDERING
print sell

if sell=="all":
    prefix+="all/"
    classes=["MIG","MAG"]
elif sell=="aut_cal":
    prefix+="aut_calc/"
    classes=["AUT","CAL"]
elif sell=="small":
    prefix+="small/"
    classes=["MIG","MAG"]
elif sell=="toy":
    prefix+="toy/"
    classes=["MIG","MAG"]
elif sell=="ideal_toy":
    _,b_term_list=generate_ideal(prefix,15,20,0.15)
    prefix+="ideal_toy/"
    classes=["MIG","MAG"]
elif sell=="kenyan":
    prefix+="kenyan/"
    classes=["LO","WE"]
elif sell=="pdr_rxp":
    prefix+="pdr_rxp/"
    classes=["PDR","RXP"]
elif sell=="whatif":
    prefix+="whatif_aesop/"
    classes=["WHAT-IF","AESOP"]
elif sell=="whatifv2":
    prefix+="whatif_aesop_v2/"
    classes=["WHAT-IF","AESOP"]
elif sell=="fact_aesop":
    prefix+="fact_aesop/"
    classes=["FACT","AESOP"]
elif sell=="pq_fact":
    prefix+="pq_fact/"
    classes=["PQ","FACT"]
elif sell=="pdr_rxp_abstracts":
    prefix+="pdr_rxp_abstracts/"
    if fetch_documents:
        abstracts_for_terms(prefix+"document_raw.txt",term1="(\"Arabidopsis\" OR Oryza OR Solanum OR Nicotiana OR plant) AND (signalling OR signaling OR \"defence\" OR \"defense\" OR \"ethylene\" OR \"jasmonate\" OR \"jasmonic acid\" OR \"salicylate\" OR \"salicylic acid\" OR \"pathogen\" OR \"virus\")",klass1="PDR",term2="(redox OR reduction OR oxidation) AND (potential OR state)",klass2="RXP")
        use_domain_dictionary(prefix+"document_raw.txt",prefix+"dictionaries")
    classes=["PDR","RXP"]
elif sell=="et_sa":
    prefix+="et_sa/"
    generate_from_files(prefix,"ET publications","ET","SA publications","SA","documents.txt","dictionaries")
    classes=["ET","SA"]
elif sell=="et_sa_abstracts":
    prefix+="et_sa_abstracts2/"
    if fetch_documents:
        abstracts_for_terms(prefix+"document_raw.txt",term1="(\"Arabidopsis\" OR \"Oryza\" OR \"Solanum\" OR \"Nicotiana\" OR \"plant\") AND ( \"salicylate\" OR \"salicylic acid\")",klass1="SA",term2="(\"Arabidopsis\" OR \"Oryza\" OR \"Solanum\" OR \"Nicotiana\" OR \"plant\") AND (\"ethylene\")",klass2="ET")
        use_domain_dictionary(prefix+"document_raw.txt",prefix+"dictionaries")
    classes=["ET","SA"]
elif sell=="pdr_rxp_small":
    prefix+="pdr_rxp_small/"
    classes=["PDR","RXP"]
else:
    words_per_doc=500
    generate_random(prefix,words_per_doc)
    prefix+="random"+str(words_per_doc)+"/"
    classes=["MIG","MAG"]

every=1

mig_mag_file=open(prefix+"documents.lndoc", 'r')
full_text_file=open(prefix+"document_raw.txt", 'r')
hevristic_scores=prefix+"HevrisitcsScores.txt"
fline = full_text_file.readline()    # Invokes readline() method on file
line = mig_mag_file.readline()    # Invokes readline() method on file
text_per_document={}
full_text_per_document={}
class_per_document={}


i=0
count=0

while line:
    if line!="\n" and i%every==0:
        spl=line.split("\t")
        #print spl
        class_per_document[count]=spl[1]
        text_per_document[count]=spl[2].split("\n")[0].split(" ")
        if "" in text_per_document[count]:
            text_per_document[count].remove("")

        #print spl[2],"" in text_per_document[count]
        not_splitted_full_text=fline.split("\n")[0]
        print not_splitted_full_text
        full_text_per_document[count]=not_splitted_full_text[(not_splitted_full_text.index("\t",not_splitted_full_text.index("\t")+1)+1):]
        #print i,spl[0]
        count+=1
    i+=1
    line = mig_mag_file.readline()
    fline = full_text_file.readline()
#print "row_perm:",row_perm_rev
mig_mag_file.close()
full_text_file.close()


#TF-IDF and BOW
words = set()
tf_idfs = {}

for train in text_per_document.keys():
    for word in text_per_document[train]:
        words.add(word)

word_count=defaultdict(int)

for train_words in text_per_document.values():
    for word in set(train_words):
        word_count[word]+=1

len_train_text=len(text_per_document)
words_sorted_by_frequency=sorted(word_count.items(),key=lambda a: a[1],reverse=True)
#-----------------CALCULATE TF-IDFS-----------------
print "compute tf-idf"

for train, train_words in text_per_document.items():
    
    #print str(train_words)
    train_word_count=defaultdict(int)
    tf_idfs[train] = {}
    for word in train_words:
        train_word_count[word]+=1
    
    for word,tf in train_word_count.items():
        idf = log(len_train_text / float(word_count[word]))

        #print train, word, tf*idf
        tf_idfs[train][word] = tf * idf
        
sorted_words = sorted(list(words))
sw_file=open(prefix+"sorted_words.txt",'w')
for sw in sorted_words:
    sw_file.write(sw+"\n")
sw_file.close()
nums=0
tfnnull=0
max_tfidf=max([item for t in tf_idfs.values() for item in t.values()])


with_inverse=False
inverse_only=False

if with_inverse:
    write_to_init_file_inv(class_per_document,text_per_document,sorted_words,prefix+"init.dat_inv")
    write_to_init_file(class_per_document,text_per_document,sorted_words,prefix+"init.dat")
    _,col_perm_rev_inv=get_permutations(prefix,filename=prefix+"init_inv.dat")
    col_perm_rev,row_perm_rev=get_permutations(prefix,filename=prefix+"init.dat")
elif inverse_only:
    col_perm_rev_inv=False
    write_to_init_file_inv(class_per_document,text_per_document,sorted_words,prefix+"init.dat_inv")
    col_perm_rev,row_perm_rev=get_permutations(prefix,filename=prefix+"init_inv.dat")
else:
    col_perm_rev_inv=False
    write_to_init_file(class_per_document,text_per_document,sorted_words,prefix+"init.dat")
    col_perm_rev,row_perm_rev=get_permutations(prefix,filename=prefix+"init.dat")

col_perm={}
for k,v in col_perm_rev.items():
    col_perm[v]=k

col_perm_inv=False
if col_perm_rev_inv:
    col_perm_inv={}
    for k,v in col_perm_rev_inv.items():
        col_perm_inv[v]=k



#-----------------CROSSBEE SCORES-----------------
from read_hevristic_scores import read_scores_from_file
jursic_word_score=read_scores_from_file(hevristic_scores)

max_word_score=False
if jursic_word_score:
    max_word_score=max(jursic_word_score.values())*1.

    

#-----------------HEVRISTICS-----------------
from hevristic_functions import *

print len(sorted_words),len(row_perm_rev),len(col_perm_rev)
greens_per_word,blues_per_word=calculate_colours(prefix,sorted_words,row_perm_rev,col_perm_rev,class_per_document,classes)
greens_on_diag_per_word,blues_on_diag_per_word=calculate_diag_colours(prefix,sorted_words,row_perm_rev,col_perm_rev,class_per_document,classes)
labels=['Hevristika1','Hevristika2','Hevristika3','Hevristika4']


hevristics=[hevristic1,hevristic2,hevristic3,hevristic4]
scores=[sorted(hevristic(greens_per_word,blues_per_word,greens_on_diag_per_word,blues_on_diag_per_word),key=lambda a: (1 if greens_per_word.get(a[0])!=0 and blues_per_word.get(a[0])!=0 else 0),reverse=True) for hevristic in hevristics]
if jursic_word_score:
    scores_crossbee=[(word,score/max_word_score) for word,score in jursic_word_score.items()]# if greens_per_word.has_key(word) or blues_per_word.has_key(word)]
    scores_crossbee.sort(key=lambda a:a[1],reverse=True)
    scores.append(scores_crossbee)
    labels.append('Crossbee')


#b-term generation
if sell!="ideal_toy":
    b_term_list=['5_ht','5_hydroxytryptamine','5_hydroxytryptamine_receptor','anti_aggregation','anticonvulsant','anti_inflammatory','antimigraine','arterial_spasm','brain_serotonin','calcium_antagonist','calcium_blocker','calcium_channel','calcium_channel_blocker','cerebral_vasospasm','convulsion','convulsive','coronary_spasm','cortical_spread_depression','diltiazem','epilepsy','epileptic','epileptiform','hypoxia','indomethacin','inflammatory','nifedipine','paroxysmal','platelet_aggregation','platelet_function','prostacyclin','prostaglandin','prostaglandin_e1','prostaglandin_synthesis','reactivity','seizure','serotonin','spasm','spread','spread_depression','stress','substance_p','vasospasm','verapamil']

b_terms=set(word for word in b_term_list if greens_per_word.get(word)!=0 and blues_per_word.get(word)!=0)

print [(word,greens_per_word.get(word),blues_per_word.get(word)) for word in b_term_list]
print b_term_list
print b_terms

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
print "generate ROC drawing"
roc_data = [ROCData(#score)
    [(1 if word in b_terms else 0, score)#-random.random()/10000000000000000000000.)#+(100 if greens_per_word.get(word)!=0 and blues_per_word.get(word)!=0 else 0)) 
     for word, score in sscores]# if greens_per_word.get(word)!=0 and blues_per_word.get(word)!=0]
) for sscores in scores]


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

    best_hevristic_scores_permutation[j]=score_j


fille=open(prefix+"hevristic4_scores.txt", "w")
for word,score in scores[3][:100]:
    fille.write(str(int(score*100)/100.).replace(".",",")+"\t"+word+"\t"+str(greens_per_word[word])+"\t"+str(blues_per_word[word])+"\n")
fille.close()
draw_matrix(sorted_words,jursic_word_score,max_word_score,col_perm_rev,row_perm_rev,class_per_document,
    prefix+"6_after_scores_perm",prefix+"min_flips_output_7_original_banded_matrix",b_terms,best_hevristic_scores_permutation,classes)

fille=open(prefix+"AUC_scores.txt", "w")
for i,roc in enumerate(roc_data):
    fille.write(labels[i]+"\tAUC:\t"+str(roc.auc())+"\n")
    #print labels[i],"AUC:\t"+str(roc.auc())
fille.close()


if sell in ["whatif","pq_fact","fact_aesop","whatifv2"]:
    fille=open(prefix+"generate_document_combinations_from_domains.txt", "w")
    for word,score in scores[3][:8]:
        for doc_id,klass in class_per_document.items():
            if klass==classes[0] and word in text_per_document[doc_id]:
                for doc2_id,klass2 in class_per_document.items():
                    if klass2==classes[1] and word in text_per_document[doc2_id]:
                        #print "a",word,"b"
                        fille.write(word+": "+full_text_per_document[doc_id]+" "+full_text_per_document[doc2_id]+"\n")
    fille.close()




    #plot_multiple_roc(roc_data,'B-term ROC Curves, DB:'+sell,include_baseline=True,labels=labels,file_name=sell)

#trains_class[0]="MAG"

