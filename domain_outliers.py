from matplotlib import rc_file_defaults

__author__ = 'matic'
import orange

print "Before generate"

print "After generate"
import random

def find_domain_outliers(prefix,document_classes,learner = orange.BayesLearner):
    document_classes[4]="MAG"

    #CREATE ORANGE FILE
    fajl=open(prefix+"temp.dat", 'r')
    orange_fajl=open("temp_orange.tab", 'w')
    #file_text = fajl.read().replace(" ","\t")


    line = fajl.readline()
    num_attts=len(line.split("\n")[0].split(" "))
    print num_attts
    for i in range(num_attts):
        orange_fajl.write("w"+str(i)+"\t")
    orange_fajl.write("klass\n")
    for _ in range(num_attts):
        orange_fajl.write("d\t")
    orange_fajl.write("d\n")

    for _ in range(num_attts):
        orange_fajl.write("\t")
    orange_fajl.write("c\n")
    i=0
    while line:
        if line!="\n":
            words=line.split("\n")[0].replace(" ","\t")
            orange_fajl.write(words+"\t"+document_classes[i]+"\n")
        line = fajl.readline()
        i+=1
    fajl.close()

    orange_fajl.close()


    # TEST
    data = orange.ExampleTable("temp_orange.tab")

    # SET DOCUMENT META IDS
    misses = orange.FloatVariable("doc_id")
    id = orange.newmetaid()
    data.domain.addmeta(id, misses)

    for i,ex in enumerate(data):
        ex["doc_id"]=i
        print i, ex


    #K-MEANS
    k = 10
    noisyIndices = []
    selection = orange.MakeRandomIndicesCV(data, folds=k)
    count_noisy = [0]*k
    print 'Before for loop'
    for test_fold in range(k):
        train_data = data.select(selection, test_fold, negate=1)
        test_data = data.select(selection, test_fold)
        #print "\t\t", "Learned on", len(train_data), "examples"
        #file.flush()
        print 'Before classifier construction'
        #print learner.hovername if learner.hovername != None else "ni hovernamea"
        classifier = learner(train_data)
        print 'After classifier construction'
        for example in test_data:
            exclassified = classifier(example)
            if exclassified != None and exclassified != example.getclass():
                # selection_filter[int(example[meta_id].value)] = 0
                noisyIndices.append(int(example["doc_id"].value))
                count_noisy[test_fold] += 1
            # END test_data
        print str(int((test_fold+1)*1.0/k*100))+"/100"
    print noisyIndices
    return noisyIndices
