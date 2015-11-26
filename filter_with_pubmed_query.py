__author__ = 'matic'
pd_vs_rp=1
if pd_vs_rp:
    #PLANT DEFENSE RESPONSE VS REDOX POTENTIAL
    domainA="pd"
    domainC="rp"
    #queryA="Arabidopsis thaliana AND (defence OR defense OR ethylene OR jasmonate OR \"jasmonic acid\" OR \"salicylate\" OR \"salicylic acid\" OR pathogen OR virus)"
    #queryC="(redox OR reduction OR oxidation) AND (potential OR state)"
    queryA=[["Arabidopsis thaliana","Oryza", "Solanum", "Nicotiana"],["defence","defense","ethylene", "jasmonate", "jasmonic acid", "salicylate", "salicylic acid", "pathogen", "virus"]]
    queryRP="((redox AND (potential OR state)) OR (reactive AND oxigen AND species))"
    file="D:/crossbee databases/dataset_pd_rp_all.txt"
else:
    #GLIO VS AML
    domainA="glio"
    domainC="aml"
    #D1: (Glioma OR glioblastoma OR "glioblastoma multiforme2" OR GBM OR "brain cancer")
    #D2: (AML OR "acute myeloid leukemia")
    queryA=[["Glioma", "glioblastoma", "glioblastoma multiforme2", " GBM","brain cancer"]]
    queryC=[[" AML", "acute myeloid leukemia"]]
    file="D:/crossbee databases/dataset_glio_aml_all.txt"

def selected_by_query(text2,query):
    text=text2.lower()
    #print "glioma" in text
    for and_cond in query:
        if type(and_cond)==list:
            at_least_one_present=False
            for or_cond in and_cond:
                if or_cond.lower() in text:
                    at_least_one_present=True
                    break
            if not at_least_one_present:
                return False
        else:
            if not and_cond.lower() in text:
                return False
    return True

def selected_for_RP(text):
    return selected_by_query(text,["redox",["potential","state"]]) or selected_by_query(text,["reactive", "oxigen","species"])

if __name__ == "__main__":
    filename,ending=file.split(".")
    with open(file,'r') as input_file:
        with open(filename+"_filtered."+ending,'w') as output_file:
            for line in input_file:
                #print line
                if line.strip()!="":
                    #print "1"
                    split=line.split("\t")
                    #print split[1][1:],domainA
                    if split[1][1:]==domainA and selected_by_query(line,queryA):
                        print domainA
                        output_file.write(line)
                    elif split[1][1:]==domainC and selected_for_RP(line) if pd_vs_rp else selected_by_query(line,queryC):
                        print domainC
                        output_file.write(line)