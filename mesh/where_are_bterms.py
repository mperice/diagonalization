bterms="""5 ht
5 hydroxytryptamine
5 hydroxytryptamine receptor
anti aggregation
anticonvulsant
anti inflammatory
antimigraine
arterial spasm
brain serotonin
calcium antagonist
calcium blocker
calcium channel
calcium channel blocker
cerebral vasospasm
convulsion
convulsive
coronary spasm
cortical spread depression
diltiazem
epilepsy
epileptic
epileptiform
hypoxia
indomethacin
inflammatory
nifedipine
paroxysmal
platelet aggregation
platelet function
prostacyclin
prostaglandin
prostaglandin e1
prostaglandin synthesis
reactivity
seizure
serotonin
spasm
spread
spread depression
stress
substance p
vasospasm
verapamil"""

bterms2="""
22q11 2
deletion syndrome
asbestos
Bcl 2
bombesin
calmodulin
radiation
maternal hypothyroxinemia
synaptic
synaptic plasticity
type 1 diabetes
ulcerative colitis
working memory
"""

bterms=set(bterms.split("\n"))
print bterms
from collections import defaultdict
path='mesh_d2015.txt'
#files = [ f for f in listdir(path) if f!="synonims.txt" ]
level2=[]
category_of_a_terms=defaultdict(int)
entries=set()
#for file in files:
with open(path,'r') as input_file:
    for line in input_file:
        if line.strip()!="":
            if line.startswith("*NEWRECORD"):
                entries=set()
            elif line.startswith("MH = "):
                mesh_head=line[5:-1]
                entries.add(mesh_head.lower())
            elif line.startswith("ENTRY = "):
                new_entries=line[8:-1].split("|")
                for new_entry in new_entries:
                    entries.add(new_entry.lower())

            elif line.startswith("MN = "):
                category=line[5:-1].split(".")[0]

                for entry in entries:
                    ##PUT ADJECTIVES IN FRONT
                    #print entry
                    if not " and " in entry:
                        print entry
                        spl_entry=entry.split(", ")
                        spl_entry.reverse()

                        entry=" ".join(spl_entry)
                    category_of_a_terms[entry]=category

                    # spl_entry=entry.split(", ")
                    # for spl_e in spl_entry:
                    #     if len(spl_e)>3:
                    #         category_of_a_terms[spl_e]=split

categories=defaultdict(int)

#print category_of_a_terms.items()[0::4]
#print (bterms)
bbb=set()
for bterm in bterms:
    for term in category_of_a_terms.keys():
        #if len(set(term.lower().split(" ")) &  set(bterm.lower().split(" ")))>0: #==len(set(term.lower().split(" "))):
        if term==bterm:
            print "jej za: "+bterm
        #if len(set(term.lower().split(" ")) ==len(set(term.lower().split(" "))):
            #print bterm,"||",term, "|||",category_of_a_terms[term]
            categories[category_of_a_terms[term][0]]+=1
            bbb.add(bterm.lower())


print categories
print len(bbb)

