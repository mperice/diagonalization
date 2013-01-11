__author__ = 'matic'
from Bio import Entrez,Medline
import time
def abstracts_for_terms(filename,term1,klass1,term2,klass2,last_x_years=8,limit=10000000000):
    #filename="D:/diagonalization/et_sa/abstracts.txt"
    filename=filename.split(".")[0]
    out_handle=open(filename+".txt", "w")

    Entrez.email = "mperice@gmail.com"     # Always tell NCBI who you are

    #abstracts_for_term(term="(\"Arabidopsis\" OR \"Oryza\" OR \"Solanum\" OR \"Nicotiana\" OR \"plant\") AND (\"signalling\" OR \"signaling\" OR \"defence\" OR \"defense\" OR \"ethylene\" OR \"jasmonate\" OR \"jasmonic acid\" OR \"salicylate\" OR \"salicylic acid\" OR \"pathogen\" OR \"virus\")",klass="PDR",initial_i=abstracts_for_term("(redox OR reduction OR oxidation) AND (potential OR state)","RXP"))
    abstractsA=abstracts_for_term(filename,term=term1,last_x_years=last_x_years,limit=limit)
    abstractsC=abstracts_for_term(filename,term2,last_x_years=last_x_years,limit=limit)
    intersectionAC=set([a[0] for a in abstractsA])&set([a[0] for a in abstractsC])

    #print [a[0] for a in abstractsA],[a[0] for a in abstractsC],intersectionAC
    print len(abstractsA),len(abstractsC),len(intersectionAC)
    i=1
    for pmid,a in abstractsA:
        if not pmid in intersectionAC:
            out_handle.write(str(i)+"\t!"+klass1+"\t"+a+"\n")
            i+=1
    for pmid,a in abstractsC:
        if not pmid in intersectionAC:
            out_handle.write(str(i)+"\t!"+klass2+"\t"+a+"\n")
            i+=1
    out_handle.close()


    out_handle_i=open(filename+"_domain_intersetion.txt", "w")
    i=1
    for pmid,a in abstractsA:
        if pmid in intersectionAC:
            out_handle_i.write(str(i)+"\t!INTERS\t"+a+"\n")
            i+=1
    out_handle_i.close()

    #abstracts_for_term(term="\"salicylic acid\" AND ethylene AND \"arabidopsis thaliana\"",klass="inters",initial_i=3289)

def abstracts_for_term(filename,term,last_x_years=3,limit=10000000000):
    search_results = Entrez.read(Entrez.esearch(db="pubmed", term=term,reldate=365*last_x_years, datetype="pdat",  usehistory="y"))
    count = min([int(search_results["Count"]),limit])
    print "Found %i results" % count
    rez=[]
    batch_size = 50
    #out_handle = open(filename, "a")
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

            if record.has_key("AB"):
                rez.append([record["PMID"],record["AB"]])
                #out_handle.write(str(i+initial_i+start+1)+"\t!"+klass+"\t"+record["AB"]+"\n")
        time.sleep(5)
    #out_handle.close()
    return rez

#abstracts_for_terms("document_raw.txt",term1="(\"Arabidopsis\" OR \"Oryza\" OR \"Solanum\" OR \"Nicotiana\" OR \"plant\") AND ( \"salicylate\" OR \"salicylic acid\")",klass1="SA",term2="(\"Arabidopsis\" OR \"Oryza\" OR \"Solanum\" OR \"Nicotiana\" OR \"plant\") AND (\"ethylene\")",klass2="ET")
