from HTMLParser import HTMLParser

__author__ = 'matic'
import xml.etree.ElementTree as ET
import os,re

rx = re.compile("&#([0-9]+);|&#x([0-9a-fA-F]+);")

def fix_xml(input):
    if input:
        input=HTMLParser().unescape(input)
        import re

        # unicode invalid characters
        RE_XML_ILLEGAL = u'([\u0000-\u0008\u000b-\u000c\u000e-\u001f\ufffe-\uffff])' + \
                         u'|' + \
                         u'([%s-%s][^%s-%s])|([^%s-%s][%s-%s])|([%s-%s]$)|(^[%s-%s])' % \
                          (unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
                           unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
                           unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
                           )
        input = re.sub(RE_XML_ILLEGAL, "", input)

        # ascii control characters
        input = re.sub(r"[\x01-\x1F\x7F]", "", input)

    return input.encode('utf-8','replace').replace("&","and")


def generate_in_dir(dir_name,name,num=1000000000000000):
    old_dir=os.getcwd()
    os.chdir(dir_name)
    filelist = [ f for f in os.listdir('.') if f[-3:]=='xml' and not 'article_set' in f ]
    print filelist,len(filelist)

    with open(name+'_article_set_'+str(num)+'.xml',"w") as output_file:
        output_file.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n<!DOCTYPE pmc-articleset PUBLIC \"-//NLM//DTD ARTICLE SET 2.0//EN\" \"http://dtd.nlm.nih.gov/ncbi/pmc/articleset/nlm-articleset-2.0.dtd\">\n<pmc-articleset>\n")

        for f in filelist[:num]:
            with open(f, "r") as myfile:
                output_file.write("    <article ")

                txt=myfile.read() #.replace('\n', '')
                print f
                #tree = ET.fromstring(data)
                #root = tree.getroot()
                #print txt
                output_file.write(txt.split("<article ")[1].split("</article>")[0])
                output_file.write("</article>\n")
                #article_elements=tree.findall('article')
                #for aaaa in article_elements:
                #    xml_string=ET.tostring(aaaa)
                #    fixed_xml=fix_xml(xml_string)
                #    output_file.write(fixed_xml+"\n")
        output_file.write("</pmc-articleset>")

    os.chdir(old_dir)
    return None



for num in [None,100,1000]:
    generate_in_dir('D:\diagonalization\glio_aml\domain1','glio',num)
    generate_in_dir('D:\diagonalization\glio_aml\domain2','aml',num)
    generate_in_dir('D:\diagonalization\PD_RP\domain1','pd',num)
    generate_in_dir('D:\diagonalization\PD_RP\domain2','rp',num)
#generate_in_dir('D:\\diagonalization\\tmp')
