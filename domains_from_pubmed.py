from xml.dom import minidom

__author__ = 'matic'
from Bio import Entrez,Medline
import time
Entrez.email = "mperice@gmail.com"     # Always tell NCBI who you are

#term="(\"Arabidopsis\" OR \"Oryza\" OR \"Solanum\" OR \"Nicotiana\" OR \"plant\") AND (\"signalling\" OR \"signaling\" OR \"defence\" OR \"defense\" OR \"ethylene\" OR \"jasmonate\" OR \"jasmonic acid\" OR \"salicylate\" OR \"salicylic acid\" OR \"pathogen\" OR \"virus\")"

oa="open access[filter] AND "

#1. try
#term12="(redox OR reduction OR oxidation) AND (potential OR state)"
#term11="open access[filter] AND \"Arabidopsis thaliana\" AND (defence OR defense OR ethylene OR jasmonate OR \"jasmonic acid\" OR \"salicylate\" OR \"salicylic acid\" OR pathogen OR virus)"

#2. try
#term11='("Arabidopsis thaliana" OR Oryza OR Solanum OR Nicotiana) AND ("defence" OR "defense" OR "ethylene" OR "jasmonate" OR "jasmonic acid" OR "salicylate" OR "salicylic acid" OR "pathogen" OR "virus")'
#term12="((redox AND (potential OR state)) OR (reactive AND oxigen AND species))"


#glioblastoma
term11='(Glioma OR glioblastoma OR "glioblastoma multiforme2" OR GBM OR "brain cancer")'
term12='(AML OR "acute myeloid leukemia")'


print "D1: "+term11
print "D2: "+term12
#term+" AND fulltext[filter]"
search_results = Entrez.read(Entrez.esearch(db="pmc", term=oa+term11,reldate=365*10, datetype="pdat",  usehistory="y"))
print "D1 count",search_results["Count"]

search_results = Entrez.read(Entrez.esearch(db="pmc", term=oa+term12,reldate=365*10, datetype="pdat",  usehistory="y"))
print "D2 count", search_results["Count"]

search_results = Entrez.read(Entrez.esearch(db="pmc", term=oa+term11+" AND "+term12,reldate=365*10, datetype="pdat",  usehistory="y"))
print "D1+D2 count",search_results["Count"]



def abstracts_for_terms(filename,term1,klass1,term2,klass2,last_x_years=1,limit=10000000000):
    #filename="D:/diagonalization/et_sa/abstracts.txt"
    filename=filename.split(".")[0]
    out_handle=open(filename+".txt", "w")

    Entrez.email = "mperice@gmail.com"     # Always tell NCBI who you are

    #abstracts_for_term(term="(\"Arabidopsis\" OR \"Oryza\" OR \"Solanum\" OR \"Nicotiana\" OR \"plant\") AND (\"signalling\" OR \"signaling\" OR \"defence\" OR \"defense\" OR \"ethylene\" OR \"jasmonate\" OR \"jasmonic acid\" OR \"salicylate\" OR \"salicylic acid\" OR \"pathogen\" OR \"virus\")",klass="PDR",initial_i=abstracts_for_term("(redox OR reduction OR oxidation) AND (potential OR state)","RXP"))
    abstractsA=fulltext_for_term(filename,term=term11,last_x_years=last_x_years,limit=limit)
    abstractsC=fulltext_for_term(filename,term12,last_x_years=last_x_years,limit=limit)
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

import os.path
def fulltext_for_term(path,term,last_x_years=10,limit=1000000000000000,not_in=[]):
    search_results = Entrez.read(Entrez.esearch(db="pmc", term=oa+term,reldate=365*last_x_years, retmax=100000,datetype="pdat",  usehistory="y"))
    count = min([int(search_results["Count"]),limit])
    print "Found %i results" % count
    ids=search_results['IdList']#[0:limit]

    clean_by_name(ids,path)

    for i,id in enumerate(ids):
        if not id in not_in:
            file_name=path+"/"+id+".xml"
            if not os.path.exists(file_name):
                out_handle = open(file_name,'w')
                print "Going to download record %s, %i/%i" % (id,i+1,count)
                out_handle.write(get_single_fullarticle(id))
                out_handle.close()

                time.sleep(0.3)
    return ids

def get_single_fullarticle(pmc_id="3691888"):
    fetch_handle = Entrez.efetch(db="pmc",
            retmode="xml",
            id=pmc_id)   #        webenv=search_results["WebEnv"],            query_key=search_results["QueryKey"])
    #records=Medline.parse(fetch_handle)
    #records=Entrez.parse(fetch_handle)
    #print fetch_handle.readline()
    #print fetch_handle.readline()
    #record=minidom.parseString(fetch_handle.read())
    #from Bio.Blast import NCBIXML


    #for record in records:
    #    print record
    return fetch_handle.read()

def clean_by_name(ids,path):
    old_dir=os.getcwd()
    os.chdir(path)
    filelist = [ f for f in os.listdir('.') if not f[0:-4] in ids ]
    print filelist,len(filelist)
    for f in filelist:
        os.remove(f)
    os.chdir(old_dir)
    return None

#abstracts_for_terms("document_raw.txt",term1="(\"Arabidopsis\" OR \"Oryza\" OR \"Solanum\" OR \"Nicotiana\" OR \"plant\") AND ( \"salicylate\" OR \"salicylic acid\")",klass1="SA",term2="(\"Arabidopsis\" OR \"Oryza\" OR \"Solanum\" OR \"Nicotiana\" OR \"plant\") AND (\"ethylene\")",klass2="ET")


#term="(\"Arabidopsis\" OR \"Oryza\" OR \"Solanum\" OR \"Nicotiana\" OR \"plant\") AND ( \"salicylate\" OR \"salicylic acid\")"
#print Entrez.esearch(db="pmc", term=term+" AND free fulltext\[filter\]",reldate=365*14, datetype="pdat",  usehistory="y")
#intersection_ids=fulltext_for_term("intersection",term11+" AND "+term12,10)
#fulltext_for_term("domain1",term11,10,not_in=intersection_ids)
#fulltext_for_term("domain2",term12,10,not_in=intersection_ids)


#fulltext_for_term("tmp","",limit=100000) #random articles





"""
Mnemonic  Description
 25      AB        Abstract
 26      CI        Copyright Information
 27      AD        Affiliation
 28      IRAD      Investigator Affiliation
 29      AID       Article Identifier
 30      AU        Author
 31      FAU       Full Author
 32      CN        Corporate Author
 33      DCOM      Date Completed
 34      DA        Date Created
 35      LR        Date Last Revised
 36      DEP       Date of Electronic Publication
 37      DP        Date of Publication
 38      EDAT      Entrez Date
 39      GS        Gene Symbol
 40      GN        General Note
 41      GR        Grant Number
 42      IR        Investigator Name
 43      FIR       Full Investigator Name
 44      IS        ISSN
 45      IP        Issue
 46      TA        Journal Title Abbreviation
 47      JT        Journal Title
 48      LA        Language
 49      LID       Location Identifier
 50      MID       Manuscript Identifier
 51      MHDA      MeSH Date
 52      MH        MeSH Terms
 53      JID       NLM Unique ID
 54      RF        Number of References
 55      OAB       Other Abstract
 56      OCI       Other Copyright Information
 57      OID       Other ID
 58      OT        Other Term
 59      OTO       Other Term Owner
 60      OWN       Owner
 61      PG        Pagination
 62      PS        Personal Name as Subject
 63      FPS       Full Personal Name as Subject
 64      PL        Place of Publication
 65      PHST      Publication History Status
 66      PST       Publication Status
 67      PT        Publication Type
 68      PUBM      Publishing Model
 69      PMC       PubMed Central Identifier
 70      PMID      PubMed Unique Identifier
 71      RN        Registry Number/EC Number
 72      NM        Substance Name
 73      SI        Secondary Source ID
 74      SO        Source
 75      SFM       Space Flight Mission
 76      STAT      Status
 77      SB        Subset
 78      TI        Title
 79      TT        Transliterated Title
 80      VI        Volume
 81      CON       Comment on
 82      CIN       Comment in
 83      EIN       Erratum in
 84      EFR       Erratum for
 85      CRI       Corrected and Republished in
 86      CRF       Corrected and Republished from
 87      PRIN      Partial retraction in
 88      PROF      Partial retraction of
 89      RPI       Republished in
 90      RPF       Republished from
 91      RIN       Retraction in
 92      ROF       Retraction of
 93      UIN       Update in
 94      UOF       Update of
 95      SPIN      Summary for patients in
 96      ORI       Original report in
 97      """