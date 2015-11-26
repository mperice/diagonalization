with open('aesop_larger_with_titles.txt','r') as input_file:
    with open('aesop.rdf','w') as output_file:
        output_file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<rdf:RDF xmlns:data=\"http://conceptcreationtechnology.eu/resource/data#\"\n xmlns:dc=\"http://purl.oclc.org/DC/\"\n xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\">\n\n")
        i=1
        for line in input_file:
            if line.strip()!="":
                split=line.split("\t")
                title=split[2]
                moral=split[3].split("\n")[0]

                output_file.write("\t<rdf:Description rdf:about=\"http://conceptcreationtechnology.eu/resource/data#moral"+str(i)+"\">\n")
                output_file.write("\t\t<dc:Title>"+str(title)+"</dc:Title>\n")
                output_file.write("\t\t<dc:Moral>"+str(moral)+"</dc:Moral>\n")
                output_file.write("\t</rdf:Description>\n\n")

                i+=1

        output_file.write("\n</rdf:RDF>")
