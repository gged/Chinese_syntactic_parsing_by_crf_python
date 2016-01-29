# -*- coding: cp936 -*-
'''
target:piece parse->node
author:hdz
time:2014-10-17 12:52:22
S的处理和连续的单链三次
'''
import re
import cPickle
import copy
from piece_feature import get_nodel_feature
from piece_parse_model import piece_parse_model_test,piece_parse_model_test_pack
from CCG_tree import node,read_tree
from get_pcfg_prob import count_score
from piece_node_parse import get_undone,change_nodel
from get_new_tag_model import get_new_tag_pack_main
##from get_new_tag import tag_model_class
from configure import beam_size, pwd_path
file_name='files/tct_test_piece_parse.txt'
res_file='files/tct_test_piece_parsed.txt'

_file_name='files/CCG_piece_parse.txt'
_res_file='files/CCG_piece_parsed.txt'

piece_parse_tmp=pwd_path+'files/piece_parse_tmp'
##
is_test=True
is_test=False
#beam_size=1 #best tree size=4,appear also piece_joint_parse.py

def write_file(fn,res):
    with open(fn,'w') as ff:
        ff.write('\n'.join(res).encode('utf8','ignore'))
    #print 'write done'

def get_piece_parsed(nodel, tag_model, pcfg_model):#返回树节点结构
    kbest=[(nodel,0)] #keep k best,(nodes,  score)#diff:diff from last one
    while True:
        kbest,ktmp=get_undone(kbest,beam_size)
        if len(ktmp)==0:    #all finished
            break#[0]
        fts_l=[]
        for ndl in ktmp:
            fts=get_nodel_feature(ndl[0]) # get features
            fts_l.extend(fts)
            fts_l.append('')
        #tmp='tmp'#write feature file
        write_file(piece_parse_tmp,fts_l)
        crftag_l=piece_parse_model_test(piece_parse_tmp)#get result
        #print len(crftag_l),len(ktmp)
        if len(crftag_l)!=len(ktmp):
            #print crftag_l
            print 'number not match?piece_parse.py#get_piece_parsed'
        # new_ktmp=[]
        # for i in xrange(len(crftag_l)):
        #     # return: [(nodel, diff_node_index, new_tag_features)]
        #     new_ndl_l=change_nodel(ktmp[i][0],crftag_l[i])
        #     for new_ndl in new_ndl_l:
        #         new_ktmp.append((new_ndl[0],
        #             ktmp[i][1]+count_score(new_ndl[1],pcfg_model)))
        #         #count_score(pcfg_model,new_ndl[1])),the diff, new node, add up it's score
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
    return kbest#todo 每个子句都是前最佳然后拼在一起,不能只是单个子句最佳,done
######################################
def get_piece_parsed_pack(nodel_l):#多个处理
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
            fts=get_nodel_feature(nodel_l[i])
            fts_all.extend(fts)
            fts_all.append('')
            i+=1
        if len(indexl)==0:
            break
        write_file(tmp,fts_all)
        tags_all=piece_parse_model_test_pack(tmp)#get result
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
def get_final_kbest(dp_list,size,topk=[]):
    '''
    :param dp_list: n*beam matrix
    :return: top k
    '''
    for son in dp_list[0]:
        topk.append(([son[0]],son[1])) #node ,score
    for i in xrange(1,len(dp_list)):
        newtopk=[]
        for beam in topk:
            for son in dp_list[i]:
                newtopk.append((beam[0]+[son[0]],beam[1]+son[1]))
        newtopk=sorted(newtopk,key=lambda x:-x[1])
        topk=newtopk[:size]
    topk=topk[:size]
    # for x in topk:
    #     print x[1]
    #     for node in x[0]:
    #         print node.show(),
    #     print
    return topk
def piece_parsed_main_sen(treell, tag_model, pcfg_model={}):    #tag_model_class
    '''
    treell:piece(tl) list, like[[node,node],[node,],...]
    '''
    # todo, each node is kbest, how to get the top kbest node list,done
    dp_list=[]
    for tl in treell:
        kbest=get_piece_parsed(tl,tag_model,pcfg_model)
        # for x in kbest:
        #     print x[1],
        # print
        dp_list.append(kbest)
    #######
    final_kbest=get_final_kbest(dp_list,beam_size,[])#n*beam size matrix
    #######
    return final_kbest
def piece_parsed_main(fn,resf,ccg=[]):######main function
    if len(ccg)==0:#leafs in file
        ccg=get_ccg(fn)
    #####
    res=[]
    i=0
    for x in ccg:
        if x=='':
            res.append('')
            continue
        kbest=get_piece_parsed(x,{},{})
        t=kbest[0][0]
        res.append(t.show())
        i+=1
        if i%100==0:
            print i
    write_file(resf,res)
#批处理#
def piece_parsed_main_pack(fn,resf,ccg=[]):######main function
    if len(ccg)==0:#leafs in file
        ccg=get_ccg(fn)
    #####
    pack=100
    res=[]
    i=0
    while i<len(ccg):
        ts=get_piece_parsed_pack(ccg[i:i+pack])
        for t in ts:
            if t=='':
                res.append('')
            else:
                res.append(t.show())
        i+=pack
        if i%100==0:
            print i
##    t=get_piece_parsed(x)
##    res.append(t.show())
    write_file(resf,res)
def piece_parsed_test(fn,resf):
    def get_node_list(t):
        if t.isleaf:
            return [t]
        nl=[]
        for son in t.son:
            nl.extend(get_node_list(son))
        return nl
    ########
    ccg_lines=[x.strip().decode('utf8') for x in file(fn)]
    ccg=[]
    for line in ccg_lines:#change node to leaf list
        if len(line)==0:
            ccg.append('')
            continue
        ct=read_tree(line)##ccg
        nodel=get_node_list(ct)
        ccg.append(nodel)
    #leaf list to node
    #piece_parsed_main(fn,resf,ccg)####分块处理
    piece_parsed_main_pack(fn,resf,ccg)###批处理
if __name__=='__main__':
    pass
    #piece_parsed_test(file_name,res_file)
    #piece_parsed_test(_file_name,_res_file)
    #piece_parsed_test(test_file,test_res_file)
    print 'done'




