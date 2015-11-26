#!/usr/local/bin/python
# coding: latin-1
__author__ = 'matic'
#Tweeter txt file preprocessing


import re
import csv

#input = re.sub(r"[\x01-\x1F\x7F]", "", input)
path="D:/diagonalization/whatif_aesop_v2/"
sts=set()
with open(path+"input.csv",'r') as input_file:
    #reader = csv.reader(input_file)

    for line in input_file:
        #print line
        if line.strip()!="":
            #print "1"
            #new_txt = re.sub(r"(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?", "", line,flags=re.I)
            new_txt = re.sub(r"(https:[/][/]|http:[/][/]|www.)[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(:[a-zA-Z0-9]*)?/?([a-zA-Z0-9\-\._\?\,\'/\\\+&amp;%\$#\=~])*","",line,flags=re.I)
            #new_txt = re.sub(r"(^|\s|[â€ś])@([a-z0-9_]+:*)", "", new_txt,flags=re.I)
            new_txt = re.sub(r"â€.", "", new_txt,flags=re.I)
            new_txt = re.sub(r"@([a-z0-9_]+:*)", "", new_txt,flags=re.I)
            new_txt = re.sub(r"(^|\s)#([a-z0-9_]+:*)", "", new_txt,flags=re.I)
            if new_txt[0]==" ":
                new_txt=new_txt[1:]
            print new_txt
            new_txt = re.sub(r"[^[\sa-z0-9_\.,\!\?\(\)\"'\:]", "", new_txt,flags=re.I)
            new_txt=new_txt.replace("RT ","").replace("http://t.","").replace("  "," ").replace("  "," ").replace("  "," ")

            print new_txt
            sts.add(new_txt)#.encode('utf-8','ignore'))

with open(path+"output_whatifs.txt",'w') as output_file:
    for st in sts:
        output_file.write(st)
