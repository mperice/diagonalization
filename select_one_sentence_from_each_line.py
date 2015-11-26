__author__ = 'matic'
import random

with open('input.txt','r') as input_file:
    with open('output.rdf','w') as output_file:
        output_file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<rdf:RDF xmlns:data=\"http://conceptcreationtechnology.eu/resource/data#\"\n xmlns:dc=\"http://purl.oclc.org/DC/\"\n xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\">\n\n")
        i=1
        for line in input_file:
            if line.strip()!="":
                split=line.split(".")
                sentence=(random.choice(split))

                output_file.write("\t<rdf:Description rdf:about=\"http://conceptcreationtechnology.eu/resource/data#pubmed"+str(i)+"\">\n")
                output_file.write("\t\t<dc:Title>"+str(sentence)+"."+"</dc:Title>\n")
                output_file.write("\t</rdf:Description>\n\n")

                i+=1

        output_file.write("\n</rdf:RDF>")
