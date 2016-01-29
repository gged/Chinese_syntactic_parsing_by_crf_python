# -*- coding: cp936 -*-
import sys
import os
import time
from configure import pwd_path, crfpath
test_file='test.txt'#file to test

FilePath='./file/'

#crfpath='/home/hdz/CRF/'
modelpath=pwd_path+'model/'
#model_name=modelpath+'CTB_piece_joint_model_1_15'#####2 for test
model_name=modelpath+'CTB_piece_joint_model_0525_no_xing'#####2 for test
#model_name=modelpath+'CTB_piece_joint_model_no_xing_7_5_pieces_len_5_BME'
crftest=crfpath+'crf_test'
crftrain=crfpath+'crf_learn'

#'S','B','BI','EI','E','O'
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
        if len(tag)==0:
            continue
        tg=tag.split('\t')
        tg=tg[-7:]#maxtag/p,t1/p1,...,t5/p5
        p_node=[]
        p_node.append(tg[0].split('/')[0])
        p_node.append({})
        for p in tg[1:]:
            pt=p.split('/')
            p_node[1][pt[0]]=eval(pt[1])
        res.append(p_node)
    return res
def get_res_kbest(fn,txt=''):#deal only one sen
    if txt=='':
        tags=[x.strip() for x in file(fn)]
    else:
        tags=[x.strip() for x in txt.split('\n')]
    p_sen=tags[0] #probably of sen
    #print p_sen
    res=[]
    resl=[]
    for tag in tags[:]:
        if len(tag)==0:#?
            continue
        if tag.find('\t')==-1:#sen probably
            if len(res)!=0:
                resl.append(res)
                res=[]
            elif len(resl)!=0:
                print 'res=0?piece_joint_model.py#55'
            continue
        tg=tag.split('\t')
        tg=tg[-7:]#maxtag/p,t1/p1,...,t5/p5
        p_node=[]
        p_node.append(tg[0].split('/')[0])
        p_node.append({})
        for p in tg[1:]:
            pt=p.split('/')
            p_node[1][pt[0]]=eval(pt[1])
        res.append(p_node)
    if len(res)==0:
        print 'res=0?piece_parse_model.py#get_res_kbest'
    resl.append(res)
    return resl
def piece_joint_model_test(testf):
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
    #res=get_res(temp_file,res_text)    #old
    #return res
    resl=get_res_kbest(temp_file,res_text) # kbest
    return resl
def get_res_pack(fn,txt=''):#deal only one sen
    res_pack=[]
    if txt=='':
        tags=[x.strip() for x in file(fn)]
    else:
        tags=txt.split('\n')
    start=True
    #print p_sen
    for tag in tags:
        if len(tag)==0:#块分界
            start=True
            continue
        if start==True:
            p_sen=tags[0]#块概率，无用
            res_pack.append([])
            start=False
            continue
        tg=tag.split('\t')
        tg=tg[-6:]#maxtag/p,t1/p1,...,t5/p5
        p_node=[]
        p_node.append(tg[0].split('/')[0])
        p_node.append({})
        for p in tg[1:]:
            pt=p.split('/')
            p_node[1][pt[0]]=eval(pt[1])
        res_pack[-1].append(p_node)
    return res_pack
def piece_joint_model_test_pack(testf):
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
def piece_joint_main():
    res=piece_joint_model_test(test_file)
    tags=[x[0] for x in res]
    print tags
    return res
if __name__=='__main__':
    pass
    print 'model:',model_name
    res=piece_joint_main()
    for x in res:
        print x
    print 'done'

