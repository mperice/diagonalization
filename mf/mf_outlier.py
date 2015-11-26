import os
import sys,string
import numpy as np
#from create_ideal_world import *
#from diagonalization_helpers import *
from collections import defaultdict
print os.getenv('COMPUTERNAME')
from math import log

# if os.getenv('COMPUTERNAME')=="PORFAVOR-PC":
#     prefix="D:/diagonalization/"
# elif os.getenv('COMPUTERNAME')=='BOJAN_HP':
#     prefix="W:/diagonalization/"
# else:
#     prefix="/home/matic/"

fetch_documents=True and False
#sell=sys.argv[1]
#ROW ORDERING
#print sell

if 1==1:
    prefix="all/"
    classes=["MIG","MAG"]
    k=1000
else:
    prefix="toy/"
    classes=["A","C"]
    k=3

every=1

mig_mag_file=open(prefix+"documents.lndoc", 'r')
#full_text_file=open(prefix+"document_raw.txt", 'r')
#fline = full_text_file.readline()    # Invokes readline() method on file
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
        #not_splitted_full_text=fline.split("\n")[0]
        #print not_splitted_full_text
        #full_text_per_document[count]=not_splitted_full_text[(not_splitted_full_text.index("\t",not_splitted_full_text.index("\t")+1)+1):]
        #print i,spl[0]
        count+=1
    i+=1
    line = mig_mag_file.readline()
    #fline = full_text_file.readline()
#print "\n\nrow_perm:",row_perm_rev
mig_mag_file.close()
#full_text_file.close()


#TF-IDF and BOW
words = set()
#words_a = set()
#words_c = set()
for train in text_per_document.keys():
    for word in text_per_document[train]:
        words.add(word)
sorted_words = sorted(list(words))

for klass_i,klass in enumerate(classes):
    tf_idfs = {}
    domain_text_per_document={}
    for doc_id, text in text_per_document.items():
        if class_per_document[doc_id]==klass:
            domain_text_per_document[doc_id]=text

    # for train in text_per_document.keys():
    #     for word in text_per_document[train]:
    #         if class_per_document[train]==classes[0]:
    #             words_a.add(word)
    #         else:
    #             words_c.add(word)
    #
    # words=words_a.intersection(words_c)


    docs_containing_a_word_count=defaultdict(int)

    for train_words in domain_text_per_document.values():
        for word in set(train_words):
            docs_containing_a_word_count[word]+=1

    len_train_text=len(domain_text_per_document)
    words_sorted_by_frequency=sorted(docs_containing_a_word_count.items(),key=lambda a: a[1],reverse=True)
    #-----------------CALCULATE TF-IDFS-----------------
    print "\n\ncompute tf-idf"

    for train, train_words in domain_text_per_document.items():

        #print str(train_words)
        train_word_count=defaultdict(int)
        tf_idfs[train] = {}
        for word in train_words:
            train_word_count[word]+=1

        for word,tf in train_word_count.items():
            idf = log(len_train_text / float(docs_containing_a_word_count[word]))

            #print train, word, tf*idf
            tf_idfs[train][word] = tf * idf
    matrix=np.zeros(shape=(len(domain_text_per_document),len(words)))
    sorted_document_ids = sorted(list(domain_text_per_document.keys()))
    for i,doc_id in enumerate(sorted_document_ids):
        for j,word in enumerate(sorted_words):
            if word in tf_idfs[doc_id]:
                matrix[i,j]=tf_idfs[doc_id][word]
    if klass_i==0:
        A=matrix
    else:
        C=matrix
    #max_tfidf=max([item for t in tf_idfs.values() for item in t.values()])

if 1==0:
    from nmf import NMF
    nmf_mdl = NMF(A, num_bases=1000)
    nmf_mdl.factorize( niter=100,show_progress=True)
    #nP, nQ = matrix_factorization(R, P, Q, K)
    A_P=nmf_mdl.W
    A_Q=nmf_mdl.H
else:
    import nimfa
    fctr = nimfa.mf(A, seed = 'random_vcol', method = 'lsnmf', rank = k, max_iter = 100)
    fctr_res = nimfa.mf_run(fctr)
    A_P = fctr_res.fit.W
    A_Q = fctr_res.fit.H
    #print """Stats:
    #        - iterations: %d
    #        - final projected gradients norm: %5.3f
    #        - Euclidean distance: %5.3f
    #        - Sparseness basis: %5.3f, mixture: %5.3f""" % (fctr_res.fit.n_iter, fctr_res.distance(), fctr_res.distance(metric = 'euclidean'), A_P, A_Q)


import numpy as np
from scipy.stats import scoreatpercentile
#from scipy.stats import nanmedian

def fivenum(v):
    """Returns Tukey's five number summary (minimum, lower-hinge, median, upper-hinge, maximum) for the input vector, a list or array of numbers based on 1.5 times the interquartile distance"""
    try:
        np.sum(v)
    except TypeError:
        print('Error: you must provide a list or array of only numbers')
    q1 = scoreatpercentile(v[~np.isnan(v)],25)
    q3 = scoreatpercentile(v[~np.isnan(v)],75)
    iqd = q3-q1
    #md = nanmedian(v)
    whisker = 1.5*iqd
    return q3+whisker #np.nanmin(v), md-whisker, md, md+whisker, np.nanmax(v),


np.set_printoptions(precision=3)

import numpy.core.arrayprint as arrayprint
import contextlib

@contextlib.contextmanager
def printoptions(strip_zeros=True, **kwargs):
    origcall = arrayprint.FloatFormat.__call__
    def __call__(self, x, strip_zeros=strip_zeros):
        return origcall.__call__(self, x, strip_zeros)
    arrayprint.FloatFormat.__call__ = __call__
    original = np.get_printoptions()
    np.set_printoptions(**kwargs)
    yield
    np.set_printoptions(**original)
    arrayprint.FloatFormat.__call__ = origcall
with printoptions(precision=4, suppress=True, strip_zeros=False):
    print "\n\nA",A.shape
    print A
    print "\n\nA_P",A_P.shape
    print A_P
    print "\n\nA_Q", A_Q.shape
    print A_Q

    from numpy.linalg import pinv
    C_Q=A_Q
    #C_P=np.divide(C,C_Q)

    #print C_P

    #C_Q_inv=nimfa.utils.linalg.inv_svd(C_Q) #pinv(C_Q)
    C_Q_inv=pinv(C_Q)
    print C.shape
    print C_Q_inv.shape
    C_P=np.dot(C,C_Q_inv)

    print "\n\nC",C.shape
    print C
    print "\n\nC_Q", C_Q.shape
    print C_Q
    print "\n\nC_Q_inv", C_Q_inv.shape
    print C_Q_inv
    print "\n\nC_Q x C_Q_inv"
    print np.dot(C_Q,C_Q_inv)

    print "\n\nC_P",C_P.shape
    print C_P


    print "\n\nC_P x C_Q"
    print np.dot(C_P,C_Q)


    #adfaf= sum(C_P[0,:])
    #print C_P[0]
    #print "asdad",adfaf
    #print [sum(line) for i,line in enumerate(C_P)]
    #top_lines=[(sum([a if a>=0 else 0 for a in line.all()]),i) for i,line in enumerate(C_P)]
    #top_lines=sorted([(sum([a if a>=0 else 0 for a in line]),i) for i,line in enumerate(C_P)],reverse=True)
    top_lines=sorted([(sum([a**4 for a in list(line)]),i) for i,line in enumerate(C_P.getA())],reverse=True)
    count=1
    outlier_threshold= fivenum(np.array([a[0] for a in top_lines]))

    second_domain_docs=sorted([(idd,text) for idd,text in text_per_document.items() if class_per_document[idd]==classes[1]])

    outliers="9, 19, 56, 58, 65, 67, 76, 79, 100, 111, 119, 140, 141, 143, 157, 174, 188, 201, 219, 233, 242, 259, 314, 336, 351, 356, 357, 363, 371, 375, 381, 415, 424, 426, 428, 510, 520, 528, 602, 624, 625, 636, 674, 675, 677, 696, 709, 710, 711, 714, 747, 764, 766, 769, 770, 780, 792, 793, 797, 852, 906, 908, 914, 915, 920, 946, 961, 981, 987, 994, 1017, 1038, 1040, 1055, 1066, 1067, 1077, 1088, 1090, 1092, 1103, 1112, 1121, 1130, 1140, 1160, 1164, 1183, 1213, 1219, 1227, 1235, 1236, 1237, 1251, 1255, 1257, 1258, 1269, 1272, 1275, 1285, 1286, 1300, 1303, 1333, 1343, 1344, 1416, 1419, 1449, 1452, 1454, 1464, 1469, 1471, 1477, 1514, 1528, 1542, 1551, 1558, 1617, 1628, 1630, 1631, 1636, 1648, 1649, 1652, 1657, 1699, 1715, 1719, 1740, 1741, 1745, 1761, 1774, 1775, 1780, 1785, 1799, 1804, 1831, 1865, 1868, 1895, 1896, 1904, 1905, 1906, 1936, 1957, 1963, 1968, 1973, 1977, 1980, 1994, 1999, 2005, 2030, 2055, 2056, 2083, 2114, 2136, 2145, 2189, 2199, 2206, 2221, 2223, 2227, 2231, 2243, 2279, 2280, 2291, 2298, 2302, 2314, 2316, 2359, 2370, 2388, 2402, 2405, 2408, 2416, 2421, 2502, 2514, 2637, 2674, 2760, 2766, 2846, 3013, 3062, 3136, 3156, 3183, 3239, 3371, 3385, 3420, 3485, 3552, 3588, 3592, 3597, 3614, 3644, 3693, 3715, 3720, 3773, 3779, 3784, 3796, 3801, 3806, 3866, 3971, 3989, 4006, 4029, 4137, 4163, 4164, 4166, 4171, 4310, 4328, 4355, 4385, 4423, 4489, 4497, 4512, 4593, 4667, 4674, 4762, 4808, 4809, 4810, 4821, 4853, 4904, 4909, 4911, 4980, 4989, 5013, 5026, 5159, 5191, 5207, 5212, 5378, 5414, 5456, 5498, 5503, 5512, 5521, 5524, 5558, 5578, 5591, 5656, 5667, 5697, 5802, 5808, 5813, 5819, 5877, 5897, 5963, 5989, 6012, 6107, 6124, 6129, 6139, 6174, 6198, 6245, 6257, 6267, 6268, 6319, 6334, 6346, 6357, 6360, 6397, 6459, 6533, 6534, 6558, 6559, 6571, 6611, 6614, 6635, 6734, 6789, 6856, 6872, 6906, 6909, 6924, 6969, 7001, 7064, 7083, 7107, 7121, 7141, 7144, 7152, 7176, 7178, 7181, 7218, 7227, 7308, 7314, 7337, 7346, 7403, 7404, 7411, 7474, 7480, 7481, 7526, 7564, 7568, 7570, 7577, 7638, 7689, 7694, 7743, 7761, 7763, 7767, 7786, 7789, 7800, 7808, 7865, 7896, 7935, 7940, 7983"
    outliers=[int(o) for o in outliers.split(", ")]

    for score,i in top_lines: #[:50]:
        if score>0:#outlier_threshold:
            orig_i=second_domain_docs[i][0]
            if orig_i in outliers:
                print count,score,i+1,class_per_document[orig_i], second_domain_docs[i][1] #, # C_P[i]
                print domain_text_per_document[orig_i]
            count+=1


    import matplotlib.pyplot as plt
    import matplotlib.colors as colors

    data = np.array(C_P)
    fig, ax = plt.subplots()
    colormap = colors.LinearSegmentedColormap.from_list('g-r cmap', ['g', 'r'])
    heatmap = ax.pcolor(data, cmap=plt.get_cmap('Blues'))
    ax.invert_yaxis()

    #plt.yticks(np.arange(len(row_labels))+0.5, row_labels)
    plt.title('Heatmap %d, %d' % (1, 1))
    plt.show()
    #plt.savefig('results/5perc_graphs/heatmap-%d-%d.png' % (target, idx))