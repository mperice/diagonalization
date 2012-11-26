'''
Created on 3. sep. 2012

@author: matic
'''
from collections import defaultdict

def calculate_diag_colours(prefix,sorted_words,row_perm_rev,col_perm_rev,trains_class,classes):
    
    greens_per_word=defaultdict(int)
    blues_per_word=defaultdict(int)

    
    file=open(prefix+"min_flips_output_6_visual_banded_matrix.dat", 'r')
    line = file.readline()
    
    i=0
    while line:
        orig_i=row_perm_rev[i]
        for j,bin_value in enumerate((line.split("\n")[0]).split(" ")):
            word=sorted_words[col_perm_rev[j]]
            
            #if word=="plasma":
            #    print j
                
            if bin_value=="1":
                #print i,j
                greens_per_word[word]+=(1 if trains_class[orig_i]==classes[0] else 0)
                blues_per_word[word]+=(1 if trains_class[orig_i]==classes[1] else 0)

        line = file.readline()
        i+=1
    
    file.close()
    
    return greens_per_word,blues_per_word       



def calculate_colours(prefix,sorted_words,row_perm_rev,col_perm_rev,trains_class,classes):
    greens_per_word=defaultdict(int)
    blues_per_word=defaultdict(int)

    
    file=open(prefix+"min_flips_output_7_original_banded_matrix.dat", 'r')
    line = file.readline()
    
    i=0
    while line:
        orig_i=row_perm_rev[i]
        a=(line.split("\n")[0]).split(" ")
        for j,bin_value in enumerate((line.split("\n")[0]).split(" ")):
            word=sorted_words[col_perm_rev[j]]
            
            #if word=="plasma":
            #    print j
                
            if bin_value=="1":
                greens_per_word[word]+=(1 if trains_class[orig_i]==classes[0] else 0)
                blues_per_word[word]+=(1 if trains_class[orig_i]==classes[1] else 0)          #s"\n\t$('#redpin').redPin('addDot',i,"+pair[0]+","+pair[1]+","+trains_class[orig_i]+" "+trains_text[orig_i]+");")

        line = file.readline()
        i+=1
    
    file.close()
    
    return greens_per_word,blues_per_word       




#HEVRISTIC #1: no of documents of different colour than diag's colour
def hevristic1(greens_per_word,blues_per_word,greens_on_diag_per_word,blues_on_diag_per_word):
    all_words=set(greens_on_diag_per_word.keys()+blues_on_diag_per_word.keys())
    
    word_scores=[]
    for word in all_words:
        if greens_on_diag_per_word[word]==0 or blues_on_diag_per_word[word]==0: #if diag has one color per word
            word_scores.append([word,greens_per_word[word] if greens_on_diag_per_word[word]==0 else blues_per_word[word]])
        else:
            word_scores.append([word,0])
            
    word_scores.sort(key=lambda a:a[1],reverse=True)
    #print word_scores
    return word_scores#[[w,s*1./word_scores[0][1]] for w,s in word_scores]    
    
    
#HEVRISTIC #2: no of documents of different colour than diag's colour divided by the number of documents on the diagonal of the selected colour
def hevristic2(greens_per_word,blues_per_word,greens_on_diag_per_word,blues_on_diag_per_word):
    all_words=set(greens_on_diag_per_word.keys()+blues_on_diag_per_word.keys())
    
    word_scores=[]
    for word in all_words:
        if greens_on_diag_per_word[word]!=0 or blues_on_diag_per_word[word]!=0: #if diag has one color per word
            max_score=max(greens_on_diag_per_word[word], blues_on_diag_per_word[word])
            
            score=(blues_per_word[word] if greens_on_diag_per_word[word]==max_score else greens_per_word[word])*1./max_score
            word_scores.append([word,score])#greens_per_word[word] if greens_on_diag_per_word[word]==0 else blues_per_word[word]])
        else:
            word_scores.append([word,0])
            
    word_scores.sort(key=lambda a:a[1],reverse=True)
    #print word_scores
    return word_scores#[[w,s*1./word_scores[0][1]] for w,s in word_scores]    
    
    
    
#HEVRISTIC #3: 1/Hevristic2
def hevristic3(greens_per_word,blues_per_word,greens_on_diag_per_word,blues_on_diag_per_word):
    all_words=set(greens_on_diag_per_word.keys()+blues_on_diag_per_word.keys())
    
    word_scores=[]
    for word in all_words:
        if greens_on_diag_per_word[word]!=0 or blues_on_diag_per_word[word]!=0: #if diag has one color per word
            max_score=max(greens_on_diag_per_word[word], blues_on_diag_per_word[word])
            
            score=max_score*1./((blues_per_word[word] if greens_on_diag_per_word[word]==max_score else greens_per_word[word])+0.000000000000000000000001)
            word_scores.append([word,score])#greens_per_word[word] if greens_on_diag_per_word[word]==0 else blues_per_word[word]])
        else:
            word_scores.append([word,0])
            
    word_scores.sort(key=lambda a:a[1],reverse=True)
    #print word_scores
    return word_scores#[[w,s*1./word_scores[0][1]] for w,s in word_scores]


    
#HEVRISTIC #4: get color of diag, see the diag strength, diag_strength*ex_of_diff_colour/ex_of_diag_colou
def hevristic4(greens_per_word,blues_per_word,greens_on_diag_per_word,blues_on_diag_per_word):
    all_words=set(greens_on_diag_per_word.keys()+blues_on_diag_per_word.keys())
    
    word_scores=[]
    for word in all_words:
        if greens_on_diag_per_word[word]!=0 or blues_on_diag_per_word[word]!=0: #if diag has one color per word
            max_score=max(greens_on_diag_per_word[word], blues_on_diag_per_word[word])
            print greens_per_word[word] , greens_on_diag_per_word[word],blues_per_word[word],blues_on_diag_per_word[word],max_score
            
            if (greens_per_word[word] if greens_on_diag_per_word[word]==max_score else blues_per_word[word])!=0:
                score=max_score*1.*(blues_per_word[word] if greens_on_diag_per_word[word]==max_score else greens_per_word[word])/(greens_per_word[word] if greens_on_diag_per_word[word]==max_score else blues_per_word[word])
            else:
                score=0
            word_scores.append([word,score])#greens_per_word[word] if greens_on_diag_per_word[word]==0 else blues_per_word[word]])
        else:
            word_scores.append([word,0])
            
    word_scores.sort(key=lambda a:a[1],reverse=True)
    #print word_scores
    return word_scores#[[w,s*1./word_scores[0][1]] for w,s in word_scores]    
