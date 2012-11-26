'''
Created on 21. avg. 2012

@author: matic
'''


from collections import defaultdict


#word_score=defaultdict(float)
##ROW ORDERING
#file=open("documents.txt", 'r')
#output_file=open("toy_example.txt",'wb')
#line = file.readline()
#
#i=0
#count=1
#while line:
#    if line!="\n" and i%280==0:
#        output_file.write(str(count)+line[line.find("\t"):])
#        count+=1
#
#    line = file.readline()
#    i+=1
#file.close()
#output_file.close()




word_score=defaultdict(float)
#ROW ORDERING
file=open("all/documents.txt", 'r')
output_file=open("small/documents.txt",'wb')
line = file.readline()

i=0
count=1
while line:
    if line!="\n" and i%5==0:
        output_file.write(str(count)+line[line.find("\t"):])
        count+=1

    line = file.readline()
    i+=1
file.close()
output_file.close()