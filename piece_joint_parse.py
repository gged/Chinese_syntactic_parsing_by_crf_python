# -*- coding: cp936 -*-
'''
target:pieces joint->tree
author:hdz
time:2014-10-29 13:09:35
'''
import re
import cPickle
import copy
from piece_joint_feature import get_piece_joint_feature
from piece_joint_model import piece_joint_model_test,piece_joint_model_test_pack
from CCG_tree import node,read_tree
from get_pcfg_prob import count_score
from piece_node_parse import get_undone,change_nodel
from get_new_tag_model import get_new_tag_pack_main
from configure import beam_size,pwd_path
##from get_new_tag import tag_model_class

file_name='files/tct_test_piece_parse_head.txt.pickle'
res_file='files/tct_test_jointed.txt'

##_file_name='files/CCG_piece_parsed.txt'
##_res_file='files/CCG_parsed.txt'

test_file='files/piece_joint_test.pickle'
test_res_file='files/piece_jointed_test.txt'

piece_joint_tmp=pwd_path+'files/piece_joint_tmp'
##
is_test=True
is_test=False
from configure import beam_size
#beam_size=1 #best tree size=4,appear also piece_parse.py


def write_file(fn,res):
    with open(fn,'w') as ff:
        ff.write('\n'.join(res).encode('utf8','ignore'))
    #print 'write done'
#######################
# def get_piece_joint(nodel,tm,pcfg_model):#返回树节点结构
#     '''
#     nodel:a piece list(kbest), like[p1,p2,...]
#     '''
#     while True:
#         if len(nodel)==1:
#             return nodel[0]
#         fts=get_piece_joint_feature(nodel)
#         #tmp='tmp'#write feature file
#         write_file(piece_joint_tmp,fts)
#         tags=piece_joint_model_test(piece_joint_tmp)#get result
#         nodel=change_nodel(tm,nodel,tags)
#     return nodel[0]
#######################
def get_piece_joint(kbest,tag_model,pcfg_model):#返回树节点结构
    '''
    nodel:a piece list(kbest), like[p1,p2,...]
    '''
    #kbest=[(nodel,0)] #keep k best,(nodes,  score)#diff:diff from last one
    #kbest=list(nodel)
    while True:
        kbest,ktmp=get_undone(kbest,beam_size)
        if len(ktmp)==0:    #all finished
            break #return the final tree
        fts_l=[]
        for ndl in ktmp:
            fts=get_piece_joint_feature(ndl[0]) # get features
            fts_l.extend(fts)
            fts_l.append('')
        #tmp='tmp'#write feature file
        write_file(piece_joint_tmp,fts_l)
        crftag_l=piece_joint_model_test(piece_joint_tmp)#get result
        if len(crftag_l)!=len(ktmp):
            print 'number not match?piece_parse.py#get_piece_parsed'
        new_ndl_l=[]
        fts_l=[]
        for i in xrange(len(crftag_l)): # pack the tag crf task to be faster
            # return: [(nodel, diff_node_index, new_tag_features)]
            new_ndl_tmp=change_nodel(ktmp[i][0],crftag_l[i])
            new_ndl_l.append(new_ndl_tmp)
            fts_l.extend([x[2] for x in new_ndl_tmp])
        new_tag_l=get_new_tag_pack_main(fts_l)
        tag_index=0
        new_ktmp=[]
        for i in xrange(len(crftag_l)):
            for new_ndl in new_ndl_l[i]:
                # new_ndl=(nodel, diff_node_index, new_tag_features)
                new_ndl[0][new_ndl[1]].tag=new_tag_l[tag_index]
                tag_index+=1
                new_ktmp.append((new_ndl[0],
                    ktmp[i][1]+count_score(new_ndl[0][new_ndl[1]],pcfg_model)))
                #count_score(pcfg_model,new_ndl[1])),the diff, new node, add up it's score
        kbest.extend(new_ktmp)
        #print nodel
    kbest=[(x[0][0],x[1]) for x in kbest] #only the node left
    return kbest#最后只剩下一个节点
def get_piece_joint_pack(nodel_l):#多个处理
    resl=[]
    tmp='tmp'#write feature file
    while True:
        indexl=[]
        fts_all=[]
        i=0
        while i<len(nodel_l):
            if len(nodel_l[i])<=1:
                i+=1
                continue
            indexl.append(i)
            fts=get_piece_joint_feature(nodel_l[i])
            fts_all.extend(fts)
            fts_all.append('')
            i+=1
        if len(indexl)==0:
            break
        write_file(tmp,fts_all)
        tags_all=piece_joint_model_test_pack(tmp)#get result
        i=0
        for tags in tags_all:
            nodel_l[indexl[i]]=change_nodel(nodel_l[indexl[i]],tags)
            i+=1
    ####
    for x in nodel_l:
        if x=='':
            resl.append('')
        else:
            resl.append(x[0])
    return resl
def get_ccg(fn):#####ready to write#
    ccg_lines=[x.strip().decode('utf8') for x in file(fn)]
    ccg=[]
    nodel=[]
    for line in ccg_lines:#read leaves to list and save
        if len(line)==0:
            ccg.append(nodel)
            nodel=[]
            ccg.append('')
            continue
        ct=read_tree(line)##ccg
        nodel.append(ct)
    if len(nodel)!=0:
        ccg.append(nodel)
    return ccg

def piece_joint_main(fn,resf,ccg=[]):######main function
    if len(ccg)==0:#leafs in file
        ccg=get_ccg(fn)
    #####
    res=[]
    i=0
    for x in ccg:
        if x=='':
            res.append('')
            continue
        t=get_piece_joint(x,{},{})
        res.append(t.show())
        i+=1
        if i%100==0:
            print i
    write_file(resf,res)
#批处理#
def piece_joint_main_pack(fn,resf,ccg=[]):######main function
    if len(ccg)==0:#leafs in file
        ccg=get_ccg(fn)
    #####
    pack=100
    res=[]
    i=0
    while i<len(ccg):
        ts=get_piece_joint_pack(ccg[i:i+pack])
        for t in ts:
            if t=='':
                res.append('')
            else:
                res.append(t.show())
        i+=pack
        if i%100==0:
            print i
##    t=get_piece_joint(x)
##    res.append(t.show())
    write_file(resf,res)
def piece_joint_test(fn,resf):
    def get_node_list(t):
        if t.isleaf:
            return [t]
        nl=[]
        for son in t.son:
            nl.extend(get_node_list(son))
        return nl
    ########
    ccg_lines=cPickle.load(open(fn,'rb'))
    ccg=[]
    i=0
    temp=[]
    for line in ccg_lines:#change node to leaf list
        if line=='':
            ccg.append(temp)
            temp=[]
            continue
        temp.append(line)
    if len(temp)!=0:
        ccg.append(temp)
    #leaf list to node
    #piece_joint_main(fn,resf,ccg)####分块处理
    piece_joint_main_pack(fn,resf,ccg)###批处理
if __name__=='__main__':
    pass
    #piece_joint_test(file_name,res_file)
    piece_joint_test(test_file,test_res_file)
    print 'done'




