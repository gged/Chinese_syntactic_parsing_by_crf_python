
# -*- coding: cp936 -*-
'''
target:eval CCG tree, LP,LR,F,(0CB,1CB,2CBS)
author:hdz
time:2014-9-18 22:18:38
'''
import cPickle
from CCG_tree import read_tree
from CTB_main import version
piece_file=None
#test
#version='_tag_struct_sx3tag_no_xing_real'

# right_file='files/a_right.txt'
# test_file='files/a_res.txt'

right_file='files/ctb_8_test_right.txt'
# right_file='files/ctb_8_test.txt'
# test_file='files/ctb_8_stanford_self_pcfg'
# test_file='files/ctb_8_stanford_pcfg_res_no_binary'
# test_file='files/ctb_8_stanford_factored_res_no_binary'
# test_file='files/ctb_8_stanford_factored_res'
# test_file='files/ctb_8_stanford_pcfg_res'
#version='_tag_struct_sx3tag_no_xing_real'
test_file='files/ctb_8_test_binary2_res.txt'+version

# right_file='files/right.mrg'
# test_file='files/result_utf8.mrg'#berkerley
##piece_file='files/piece_joint_test.pickle'
ignore_tag=False#True#

##############
def set_level(t,start):
    if t.isleaf:
        t.level=start
        return t,start+1
    newson=[]
    for son in t.son:
        ns,start=set_level(son,start)
        newson.append(ns)
    if not newson[0].isleaf:
        newson[0].level=newson[0].son[0].level
    if not newson[-1].isleaf:
        newson[-1].level=newson[-1].son[-1].level
    t.son=newson
    return t,start
def get_son_num(t):#  what the ????
    if t.isleaf:
        return 0
    num=len(t.son)
    for son in t.son:
        num+=get_son_num(son)
    return num
def get_tpls(t):
    tpls=set()
    if t.isleaf:
        return set([])
##    if len(t.son)>1:#####
##        tpls.add((t.son[0].level,t.son[-1].level))
    tag=t.tag.strip('*')
    if tag.find('-')!=-1:
        tag=tag.split('-')[0]
    if tag!='':
        if ignore_tag==False:
            tpls.add((tag,t.son[0].level,t.son[-1].level)) #consider tag
        else:
            tpls.add((t.son[0].level,t.son[-1].level))      #ignore tag
        # tpls.add((t.son[0].level,t.son[-1].level,get_son_num(t)))
        # tpls.add((tag,t.son[0].level,t.son[-1].level,get_son_num(t)))
    for son in t.son:
        tpls.update(get_tpls(son))
    return tpls
def count_piece_num(fn):
    ts=cPickle.load(open(fn,'rb'))
    #ts=ts[1:16]
    num=0
    for piece in ts:
        if piece!='':
            p,end=set_level(piece,0)
            tpls=get_tpls(p)
            num+=len(tpls)
    return num
def get_phrase_struct(t):
    t,end=set_level(t,0)
    tpls=get_tpls(t.son[0])#
    return tpls
def get_two_eval(rt,tt):
    tpl1=get_phrase_struct(rt)
    tpl2=get_phrase_struct(tt)
    # print tpl1
    # print tpl2
    right=tpl1.intersection(tpl2)
    #print len(right),len(tpl2),len(tpl1)
    return len(right),len(tpl2),len(tpl1)
def parse_eval_main(rightf,testf,pf=None):
    rtrees=[x.strip().decode('utf8') for x in file(rightf)]
    ttrees=[x.strip().decode('utf8') for x in file(testf)]
    right=0
    get_all=0
    right_all=0
    i=0###############
    print 'trees num:',len(rtrees),len(ttrees)
    print '##########'
    longsen=0
    while i<len(rtrees):
        if len(rtrees[i])==0:
            i+=1
            continue
        rt=read_tree(rtrees[i])
        word_len=len(rt.get_words())
        #print word_len
        if word_len<20:
            i+=1
            continue
        longsen+=1
        tt=read_tree(ttrees[i])
        ri,ga,ra=get_two_eval(rt,tt)
        right+=ri
        get_all+=ga
        right_all+=ra
##        if not ga==ra==ri:
##            print 'right',rtrees[i]
##            print 'wrong',ttrees[i]
        i+=1
    ##########
    print '##########',longsen
    if get_all*right_all*right==0:
        print 'error,F=LP=LR=0'
        return None
    print right_all,get_all,right
    if pf!=None:
        num=count_piece_num(pf)
        get_all-=num
        right_all-=num
        right-=num
    LP=right*1.0/get_all
    LR=right*1.0/right_all
    F=2*LP*LR/(LP+LR)
    print right_all,get_all,right
    print 'LP:',round(LP,4)
    print 'LR:',round(LR,4)
    print 'F1:',round(F,4)
    return LP,LR,F


if __name__=='__main__':
    #parse_eval_main(right_file,test_file)
    parse_eval_main(right_file,test_file,piece_file)
    #count_piece_num(piece_file)
    print 'done'
