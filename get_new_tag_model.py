# -*- coding: cp936 -*-
'''
tag crf_test model
tag:NP,VP,S...
'''
import sys
import os
from get_new_tag2 import get_tag_feature_final
from configure import pwd_path, crfpath

FilePath='./files/'

test_file=FilePath+'get_tag_test'

#crfpath='/home/hdz/CRF/'
modelpath=pwd_path+'model/'
model_name=modelpath+'CTB_tag_union_crf_0505_sx3tag'#####2 for test

crftest=crfpath+'crf_test'
crftrain=crfpath+'crf_learn'

######
def get_res(fn,txt=''):#deal only one sen
    res=[]
    if txt=='':
        tags=[x.strip() for x in file(fn)]
    else:
        tags=txt.split('\n')
    p_sen=tags[0]
    #print p_sen
    for tag in tags[1:]:
        if len(tag)==0:#?
            continue
        tg=tag.split('\t')
        tg=tg[47:]###tag_feature num: 47
        p_node=[]
        for p in tg[0:4]:
            p_node.append(p.split('/'))
        res.append(p_node)
    return res
def get_tag_model_test(testf):
    #print 'test:',testf
    temp_file=testf+'.tag'
    cmd2='%s -v2 -m %s %s' % (crftest,model_name,testf)
    #cmd2='%s -v2 -m %s %s > %s' % (crftest,model_name,testf,temp_file)
    #print cmd2
    #os.system(cmd2+' & pause')#pause
    output=os.popen(cmd2)
    res_text=output.read()
    #print res_text
    #time.sleep(0.1)
    res=get_res(temp_file,res_text)
    return res
def get_res_pack(fn,txt=''):
    res_pack=[]
    if txt=='':
        tags=[x.strip() for x in file(fn)]
    else:
        tags=txt.split('\n')
    #print p_sen
    for tag in tags:
        if len(tag.strip())==0:#块分界
            continue
        if tag.find('\t')==-1:
            continue
        tg=tag.split('\t')
        tg=tg[47:]###tag_feature num: 47
        p_node=[]
        for p in tg[0:4]:
            p_node.append(p.split('/'))
        res_pack.append(p_node)
    return res_pack
def get_tag_model_test_pack(testf):
    #print 'test:',testf
    temp_file=testf+'.tag'
    cmd2='%s -v2 -m %s %s' % (crftest,model_name,testf)
    #cmd2='%s -v2 -m %s %s > %s' % (crftest,model_name,testf,temp_file)
    #print cmd2
    #os.system(cmd2+' & pause')#pause
    output=os.popen(cmd2)
    res_text=output.read()
    #print res_text
    #time.sleep(0.1)
    res=get_res_pack(temp_file,res_text)
    return res
def get_tag_main(test_file):
    res=get_tag_model_test(test_file)
    #tags=[x[0] for x in res]
    #print tags
    return res
def write_file(fn,string):
    with open(fn,'w') as ff:
        ff.write(string)
def get_new_tag_main(ts,ind,type_tag):
    tmp_file=pwd_path+'files/tmp_crf.tag'
    fts=get_tag_feature_final(ts,ind,type_tag)
    write_file(tmp_file,'\t'.join(fts).encode('utf8'))
    res=get_tag_main(tmp_file)
    #print res[0][0][0]
    return res[0][0][0]
def get_new_tag_pack_main(fts_l):
    tmp_file=pwd_path+'files/tmp_crf.tag'
    string=['\t'.join(fts).encode('utf8')+'\n' for fts in fts_l]
    write_file(tmp_file,'\n'.join(string))
    res_l=get_tag_model_test_pack(tmp_file)
    #print res[0][0][0]
    tag_l=[]
    for res in res_l:
        tag_l.append(res[0][0])
    return tag_l
if __name__=='__main__':
    pass
    print get_tag_main(test_file)#	NP-PN,	ADVP
    print 'done'

