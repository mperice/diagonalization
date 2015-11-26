__author__ = 'matic'


file='C:\Users\matic\Desktop\Vocabularies\crossbee-terms-human\GO_biomart\mart_export_GO.txt'
ofile='C:\Users\matic\Desktop\Vocabularies\crossbee-terms-human\GO_biomart\GO_terms.txt'
with open(file,'r') as input_file:
    with open(ofile,'w') as output_file:

        for line in input_file:
            #print line
            if line.strip()!="":
                split=line.split("\t")
                if split[2]!='':
                    output_file.write(split[2]+"\n")