xls="""
default_VotesAndPos_1/3_OfAllTerms	1	1	1	2	2	2	4	6	8	9
                      out_freq_svm	0	0	0	0,5	2	4	4,8	7	8,92	9
                      out_freq_sum	0	0	0	0	0	4	5,56	7	8	9
                   tfidf_domn_prod	0	0	0	0	0	3	4	7	9	9
                    freq_domn_prod	0	0	0	0	1	3	4	7	9	9
                        freq_ratio	1	1	1	1	2	3	3,6	6,01	9	9
                freq_domn_prod_rel	0	0	0	0	0	1	4	7	9	9
                       out_freq_cs	0	0	0	0	0	2	6,59	7	7,82	9
                         tfidf_sum	0	1	1	1	1	2	3	7	9	9
                    tfidf_domn_sum	0	1	1	1	1	2	3	7	9	9
                         freq_term	0	1	1	1	1	2	3	6,21	9	9
                          freq_doc	0	1	1	1	1	2	3	6	8	9
                       out_freq_rf	0	0	0	0	0	1	2,65	5,59	6,99	9
                  out_freq_rel_svm	0	0	1	1	1	1	2	3	9	9
                         tfidf_avg	1	1	1	1	1	2	2	4	7	9
                   out_freq_rel_cs	0	0	0	0	0	0	2	3	7	9
                  out_freq_rel_sum	0	0	0	0	0	1	1	3	7	9
                            random	0	0	0	0	0	0	1	4	6	9
             appear_in_all_domains	0,01	0,03	0,06	0,14	0,28	0,55	1,38	2,76	5,52	9
                   out_freq_rel_rf	0	0	0	0	0	0	0	2	6	9
               freq_domn_ratio_min	0	0	0	0	0	0	1	2	6	9

"""


for letter in list('abcdefghijklmnoprstuvz'):
    xls=xls.replace('_'+letter,letter.upper())

xls=xls.replace("\t\t","\t")
xls=xls.replace("%","\\%")
xls=xls.replace(" ","")

xls=xls.replace("\t"," & ")
xls=xls.replace("\n","\\\\\n")

print xls