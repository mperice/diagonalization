__author__ = 'matic'

filename="D:/diagonalization/pdr_rxp/documents.txt"
open(filename, "w").close()
from Bio import Entrez,Medline
Entrez.email = "mperice@gmail.com"     # Always tell NCBI who you are

def abstracts_for_term(term="Opuntia[ORGN]",klass="OPU",initial_i=0,limit=10000000000):
    global filename
    search_results = Entrez.read(Entrez.esearch(db="pubmed", term=term,reldate=365*4, datetype="pdat",  usehistory="y"))
    count = min([int(search_results["Count"]),limit])
    print "Found %i results" % count

    batch_size = 50
    out_handle = open(filename, "a")
    for start in range(0,count,batch_size):
        end = min(count, start+batch_size)
        print "Going to download record %i to %i" % (start+1, end)
        fetch_handle = Entrez.efetch(db="pubmed",
            rettype="medline", retmode="text",
            retstart=start, retmax=batch_size,
            webenv=search_results["WebEnv"],
            query_key=search_results["QueryKey"])
        #data = fetch_handle.read()
        #fetch_handle.close()
        records=Medline.parse(fetch_handle)
        for i,record in enumerate(records):
            #print
            if record.has_key("AB"):
                out_handle.write(str(i+initial_i+start+1)+"\t!"+klass+"\t"+record["AB"]+"\n")
    out_handle.close()
    return count

abstracts_for_term(term="(\"Arabidopsis\" OR \"Oryza\" OR \"Solanum\" OR \"Nicotiana\" OR \"plant\") AND (\"signalling\" OR \"signaling\" OR \"defence\" OR \"defense\" OR \"ethylene\" OR \"jasmonate\" OR \"jasmonic acid\" OR \"salicylate\" OR \"salicylic acid\" OR \"pathogen\" OR \"virus\")",klass="PDR",initial_i=abstracts_for_term("(redox OR reduction OR oxidation) AND (potential OR state)","RXP"))