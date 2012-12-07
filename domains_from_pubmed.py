__author__ = 'matic'
from Bio import Entrez,Medline

def abstracts_for_terms(filename,term1,klass1,term2,klass2,last_x_years=8,limit=10000000000):
    #filename="D:/diagonalization/et_sa/abstracts.txt"
    open(filename, "w").close()
    Entrez.email = "mperice@gmail.com"     # Always tell NCBI who you are

    #abstracts_for_term(term="(\"Arabidopsis\" OR \"Oryza\" OR \"Solanum\" OR \"Nicotiana\" OR \"plant\") AND (\"signalling\" OR \"signaling\" OR \"defence\" OR \"defense\" OR \"ethylene\" OR \"jasmonate\" OR \"jasmonic acid\" OR \"salicylate\" OR \"salicylic acid\" OR \"pathogen\" OR \"virus\")",klass="PDR",initial_i=abstracts_for_term("(redox OR reduction OR oxidation) AND (potential OR state)","RXP"))
    abstracts_for_term(filename,term=term1,klass=klass1,initial_i=abstracts_for_term(filename,term2,klass2,last_x_years=last_x_years,limit=limit),last_x_years=last_x_years,limit=limit)
    #abstracts_for_term(term="\"salicylic acid\" AND ethylene AND \"arabidopsis thaliana\"",klass="inters",initial_i=3289)

def abstracts_for_term(filename,term,klass,initial_i=0,last_x_years=80,limit=10000000000):
    search_results = Entrez.read(Entrez.esearch(db="pubmed", term=term,reldate=365*last_x_years, datetype="pdat",  usehistory="y"))
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