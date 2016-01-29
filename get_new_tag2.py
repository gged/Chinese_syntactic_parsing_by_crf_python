# -*- coding: cp936 -*-
'''
target:node->get new node tag,train a model
author:hdz
time:2015-1-15 17:56:30
###now no word feature is used
classd={}:tag dict
dd={}:feature dict
tag_model_win_dt.pickle:dt model
'''
import re
import sys
import cPickle
from math import log
from CCG_head import CCG_head
from CCG_tree import read_tree
from sklearn import tree
import numpy as np
#get_node_new_tag(nl,i,flg[i])
sys.path.append('./temp/word2vec/')
#from distance import *
word2vec_len=50
# version='0405'
version='_0507_struct_test_pack'
_filename='files/CTB_binary2.txt'
_res_file='files/CTB_binary2_union_tag'+version#cmp to 2 add feature3,2,10
_res_file2='files/CTB_binary2_union_tag_svm'+version
# version='_1204_pcfg'
# _filename='files/CTB_binary_no_xing'
# _res_file='files/CTB_binary2_union_tag_crf'+version#cmp to 2 add feature3,2,10
# _res_file2='files/CTB_binary2_union_tag_svm'+version
####
_filename_test='files/ctb_8_test_binary2.txt'
_res_file_test='files/ctb_8_test_binary2_union_tag'+version#cmp to 2 add feature3,2,10
_res_file2_test='files/ctb_8_test_binary2_union_tag_svm'+version

feature_dict_file='files/feature_union_dict.pickle'+version
tag_dict_file='files/tag_union_dict.pickle'+version
# tag_model_file='model/tag_model_linux_dt.pickle'
tag_model_file='model/tag_union_model_linux_svm_01.pickle_all'

#######
class tag_model_class:
    def __init__(self,joint=False):
        self.tag_model=cPickle.load(file(tag_model_file,'rb'))
        self.feature_dict=cPickle.load(file(feature_dict_file,'rb'))
        self.tag_dict=cPickle.load(file(tag_dict_file,'rb'))
        self.feature_lenth=len(self.feature_dict)
    def get_model_xl(self,feature):
        xl=np.zeros(self.feature_lenth)
        xli=1
        for x in feature:
            if x=='NIL':
                xli+=1
                continue
            try:
                xl[self.feature_dict[str(xli)+x]]=1
            except:###
                pass
            xli+=1
        return xl
    def get_new_node(self,feature):#
        xl=self.get_model_xl(feature)
        #print np.array([xl]).shape
        pred = self.tag_model.predict(np.array([xl]))#
        #print pred
        tag='NP'###
        try:
            tag=self.tag_dict[int(pred[0])]
        except:
            print 'UNKNOWN'
        return tag
    def get_new_node_tl(self,tl,ind,flg):
        type_tag=2
        if flg==2:
            type_tag=1#unary
        feature=get_tag_feature_0429(tl,ind,type_tag)########!!!!!_0429
        return self.get_new_node(feature)
def write_file(fn,res):
    with open(fn,'w') as ff:
        ff.write('\n'.join(res).encode('utf8','ignore'))
    print 'write done'
def write_file_add(fn,res):
    with open(fn,'a') as ff:
        ff.write('\n'.join(res).encode('utf8','ignore')+'\n')
    print 'write done'
####
def get_tag_feature_0407(ts,ind,type_tag):#get a feature list
    #type_tag,1 for unary,2 for binary
    def get_a_leaf(t,son_n):#leaf info
        if t.isleaf:
            return [t.word,t.pos]
        else:
            return get_a_leaf(t.son[son_n],son_n)
    def get_head_child(ts,indd):
        #tag,head,head_pos,sontype,lleaf_w/p,rleaf_w/p
        if indd<0 or indd>=len(ts):
            return ['NIL','NIL','NIL','NIL','NIL','NIL','NIL','NIL']
        t=ts[indd]
        tag=t.tag
        if t.isleaf:
            tag='NIL'
        ftt=[tag, t.head, t.head_pos]####add t.tag
        if len(t.son)==0:
            ftt.append('2')###############2 for no son
            ftt.extend(['NIL','NIL','NIL','NIL'])
        else:
            if len(t.son)==1:###change:1-15,crf3.txt
                ftt.append('3')###############3 for single
            elif t.head==t.son[0].head:
                ftt.append('0')##############0 for first son is head
            else:
                ftt.append('1')##############1 for last son is head
            ftt.extend(get_a_leaf(t,0))
            ftt.extend(get_a_leaf(t,-1))
        return ftt
    ft=[]
    ft.append(str(type_tag))
    #ft.extend(get_head_child(ts,ind-2))
    ft.extend(get_head_child(ts,ind-1))
    ft.extend(get_head_child(ts,ind))
    ft.extend(get_head_child(ts,ind+1))
    ft.extend(get_head_child(ts,ind+2))
    return ft#'\t'.join(ft)
def get_tag_feature_0429(ts,ind,type_tag):#get a feature list
    #type_tag,1 for unary,2 for binary
    def get_struct_feature(t):
        struct_list=[t.tag,'#','#']
        if len(t.son)>0:
            struct_list[1]=t.son[0].tag
        if len(t.son)>1:
            struct_list[2]=t.son[-1].tag
        return '_'.join(struct_list)
    def get_struct_info(t):
        struct_lists=[]
        struct_lists.append(get_struct_feature(t))
        if len(t.son)>0:
            struct_lists.append(get_struct_feature(t.son[0]))
        else:
            struct_lists.append('#_#_#')
        if len(t.son)>1:
            struct_lists.append(get_struct_feature(t.son[-1]))
        else:
            struct_lists.append('#_#_#')
        return struct_lists
    def get_a_leaf(t,son_n):#leaf info
        if t.isleaf:
            return [t.word,t.pos]
        else:
            return get_a_leaf(t.son[son_n],son_n)
    def get_head_child(ts,indd):
        #tag,head,head_pos,sontype,lleaf_w/p,rleaf_w/p
        if indd<0 or indd>=len(ts):
            return ['NIL','NIL','NIL','NIL','NIL','NIL','NIL','NIL','NIL','NIL','NIL']
        t=ts[indd]
        tag=t.tag
        # if t.isleaf:#########!!!!!change
        #     tag='NIL'
        ftt=[tag, t.head, t.head_pos]####add t.tag
        ftt.extend(get_struct_info(t))
        if len(t.son)==0:
            ftt.append('2')###############2 for no son
            ftt.extend(['NIL','NIL','NIL','NIL'])
        else:
            if len(t.son)==1:###change:1-15,crf3.txt
                ftt.append('3')###############3 for single
            elif t.head==t.son[0].head:
                ftt.append('0')##############0 for first son is head
            else:
                ftt.append('1')##############1 for last son is head
            ftt.extend(get_a_leaf(t,0))
            ftt.extend(get_a_leaf(t,-1))
        return ftt
    ft=[]
    ft.append(str(type_tag))
    #ft.extend(get_head_child(ts,ind-2))
    ft.extend(get_head_child(ts,ind-1))
    ft.extend(get_head_child(ts,ind))
    ft.extend(get_head_child(ts,ind+1))
    ft.extend(get_head_child(ts,ind+2))

    return ft#'\t'.join(ft)
def get_tag_feature_0505(ts,ind,type_tag):#get a feature list
    #type_tag,1 for unary,2 for binary
    def get_node_tag(ts,indd2):
        if indd2<0 or indd2>=len(ts):
            return 'NIL'
        else:
            return ts[indd2].tag.rstrip('*')
    def get_struct_feature(t):
        struct_list=[t.tag.rstrip('*'),'#','#']
        if len(t.son)>0:
            struct_list[1]=t.son[0].tag.rstrip('*')
        if len(t.son)>1:
            struct_list[2]=t.son[-1].tag.rstrip('*')
        return '_'.join(struct_list)
    def get_struct_info(t):
        struct_lists=[]
        struct_lists.append(get_struct_feature(t))
        if len(t.son)>0:
            struct_lists.append(get_struct_feature(t.son[0]))
        else:
            struct_lists.append('#_#_#')
        if len(t.son)>1:
            struct_lists.append(get_struct_feature(t.son[-1]))
        else:
            struct_lists.append('#_#_#')
        return struct_lists
    def get_a_leaf(t,son_n):#leaf info
        if t.isleaf:
            return [t.word,t.pos]
        else:
            return get_a_leaf(t.son[son_n],son_n)
    def get_head_child(ts,indd):
        #tag,head,head_pos,sontype,lleaf_w/p,rleaf_w/p
        if indd<0 or indd>=len(ts):
            return ['NIL','NIL','NIL','NIL','NIL','NIL','NIL',
                    'NIL','NIL','NIL','NIL','NIL','NIL','NIL']
        t=ts[indd]
        tag=t.tag.rstrip('*')
        # if t.isleaf:#########!!!!!change
        #     tag='NIL'
        node_len=len(ts[indd].get_words())
        ftt=[str(int(log(node_len,2))),tag, t.head, t.head_pos]####add t.tag
        # ftt=[tag, t.head, t.head_pos]####add t.tag
        t_show=ts[indd].show()
        ftt.append(str(t_show.count('NP')))
        ftt.append(str(t_show.count('VP')))
        ftt.extend(get_struct_info(t))
        if len(t.son)==0:
            ftt.append('2')###############2 for no son
            ftt.extend(['NIL','NIL','NIL','NIL'])
        else:
            if len(t.son)==1:###change:1-15,crf3.txt
                ftt.append('3')###############3 for single
            elif t.head==t.son[0].head:
                ftt.append('0')##############0 for first son is head
            else:
                ftt.append('1')##############1 for last son is head
            ftt.extend(get_a_leaf(t,0))
            ftt.extend(get_a_leaf(t,-1))
        return ftt
    def get_sx3tag_feature(ts,indd,t_t):
        ftt=[0,0]
        if t_t==1:
            ftt[0]='_'.join([get_node_tag(ts,indd-1),get_node_tag(ts,indd)])
            ftt[1]='_'.join([get_node_tag(ts,indd),get_node_tag(ts,indd+1)])
        elif t_t==2:
            ftt[0]='_'.join([get_node_tag(ts,indd-1),get_node_tag(ts,indd),
                             get_node_tag(ts,indd+1)])
            ftt[1]='_'.join([get_node_tag(ts,indd),get_node_tag(ts,indd+1),
                             get_node_tag(ts,indd+2)])
        else:
            print '?????'
        return ftt
    #############
    ft=[]
    ft.append(str(type_tag))
    #ft.extend(get_head_child(ts,ind-2))
    ft.extend(get_head_child(ts,ind-1))
    ft.extend(get_head_child(ts,ind))
    ft.extend(get_head_child(ts,ind+1))
    ft.extend(get_head_child(ts,ind+2))
    ######
    ft.extend(get_sx3tag_feature(ts,ind,type_tag))
    ######
    return ft#'\t'.join(ft)
def get_tag_feature_final(ts,ind,type_tag):#get a feature list
    #type_tag,1 for unary,2 for binary
    def get_node_tag(ts,indd2):
        if indd2<0 or indd2>=len(ts):
            return 'NIL'
        else:
            return ts[indd2].tag.rstrip('*')
    def get_struct_feature(t):
        struct_list=[t.tag.rstrip('*'),'#','#']
        if len(t.son)>0:
            struct_list[1]=t.son[0].tag.rstrip('*')
        if len(t.son)>1:
            struct_list[2]=t.son[-1].tag.rstrip('*')
        return '_'.join(struct_list)
    def get_struct_info(t):
        struct_lists=[]
        struct_lists.append(get_struct_feature(t))
        if len(t.son)>0:
            struct_lists.append(get_struct_feature(t.son[0]))
        else:
            struct_lists.append('#_#_#')
        if len(t.son)>1:
            struct_lists.append(get_struct_feature(t.son[-1]))
        else:
            struct_lists.append('#_#_#')
        return struct_lists
    def get_a_leaf(t,son_n):#leaf info
        if t.isleaf:
            return [t.word,t.pos]
        else:
            return get_a_leaf(t.son[son_n],son_n)
    def get_head_child(ts,indd):
        #tag,head,head_pos,sontype,lleaf_w/p,rleaf_w/p
        if indd<0 or indd>=len(ts):
            return ['NIL','NIL','NIL','NIL','NIL','NIL',
                    'NIL','NIL','NIL','NIL','NIL']
        t=ts[indd]
        tag=t.tag.rstrip('*')
        # if t.isleaf:#########!!!!!change
        #     tag='NIL'
        ftt=[tag, t.head, t.head_pos]####add t.tag
        # ftt=[tag, t.head, t.head_pos]####add t.tag
        ftt.extend(get_struct_info(t))
        if len(t.son)==0:
            ftt.append('2')###############2 for no son
            ftt.extend(['NIL','NIL','NIL','NIL'])
        else:
            if len(t.son)==1:###change:1-15,crf3.txt
                ftt.append('3')###############3 for single
            elif t.head==t.son[0].head:
                ftt.append('0')##############0 for first son is head
            else:
                ftt.append('1')##############1 for last son is head
            ftt.extend(get_a_leaf(t,0))
            ftt.extend(get_a_leaf(t,-1))
        return ftt
    def get_sx3tag_feature(ts,indd,t_t):
        ftt=['NIL','NIL']
        if t_t==1:
            ftt[0]='_'.join([get_node_tag(ts,indd-1),get_node_tag(ts,indd)])
            ftt[1]='_'.join([get_node_tag(ts,indd),get_node_tag(ts,indd+1)])
        elif t_t==2:
            ftt[0]='_'.join([get_node_tag(ts,indd-1),get_node_tag(ts,indd),
                             get_node_tag(ts,indd+1)])
            ftt[1]='_'.join([get_node_tag(ts,indd),get_node_tag(ts,indd+1),
                             get_node_tag(ts,indd+2)])
        else:
            print '?????'
        return ftt
    #############
    ft=[]
    ft.append(str(type_tag))
    #ft.extend(get_head_child(ts,ind-2))
    ft.extend(get_head_child(ts,ind-1))
    ft.extend(get_head_child(ts,ind))
    ft.extend(get_head_child(ts,ind+1))
    ft.extend(get_head_child(ts,ind+2))
    ######
    ft.extend(get_sx3tag_feature(ts,ind,type_tag))
    ######
    #ft.append()
    ######
    return ft#'\t'.join(ft)
###################
# def get_words_word2vec(wl):
#     vec=get_words_vec(wl)
#     #-10~10
#     vec=[max(min(int(x//1),20),-20) for x in vec]
#     vec=[str(x) for x in vec]
#     return '\t'.join(vec)
def get_tag_feature(ts,ind,type_tag):#get a feature list
    #old feature+no *
    #type_tag,1 for unary,2 for binary
    def get_a_leaf(t,son_n):#leaf info
        if t.isleaf:
            #t.word,
            words.append(t.word)
            return [t.pos]
        else:
            return get_a_leaf(t.son[son_n],son_n)
    def get_head_child(ts,indd):
        #tag,head,head_pos,sontype,lleaf_w/p,rleaf_w/p
        if indd<0 or indd>=len(ts):
            return ['NIL','NIL','NIL','NIL','NIL']
        t=ts[indd]
        tag=t.tag
        if t.isleaf:
            tag='NIL'
        ftt=[tag, t.head_pos]####add t.tag
        #, t.head
        words.append(t.head)
        if len(t.son)==0:
            ftt.append('2')###############2 for no son
            ftt.extend(['NIL','NIL'])
        else:
            if len(t.son)==1:###change:1-15,crf3.txt
                ftt.append('3')###############3 for single
            elif t.head==t.son[0].head:
                ftt.append('0')##############0 for first son is head
            else:
                ftt.append('1')##############1 for last son is head
            ftt.extend(get_a_leaf(t,0))
            ftt.extend(get_a_leaf(t,-1))
        return ftt
    ft=[]
    words=[]
    ft.append(str(type_tag))
    #ft.extend(get_head_child(ts,ind-2))
    ft.extend(get_head_child(ts,ind-1))
    ft.extend(get_head_child(ts,ind))
    ft.extend(get_head_child(ts,ind+1))
    ft.extend(get_head_child(ts,ind+2))
    #ft.extend(words)
    #ft.append(get_words_word2vec(words))
    return ft#'\t'.join(ft)
def get_tree_tag_list(t):
    #son's level==-1 or isleaf=>to be joined
    tl=[]#all nodes 
    tgl=[]#node tags
    #是否是叶子节点或者终止节点(已被处理后的节点level=-1)
    if (t.son[0].isleaf or t.son[0].level==True) and\
       len(t.son)==2 and\
       (t.son[1].isleaf or t.son[1].level==True):
        t.son[0].level=True
        t.son[1].level=True
        t.level=True#####CHANGE, 变为处理后的节点
        if t.head==t.son[0].head:###
            return [t.son[0],t.son[1]],[t.tag+'_B',t.tag+'_BI'],t
            #return [t.son[0],t.son[1]],['B','BI'],t
        return [t.son[0],t.son[1]],[t.tag+'_EI',t.tag+'_E'],t
        #return [t.son[0],t.son[1]],['EI','E'],t
    if len(t.son)==1 and (t.son[0].isleaf or t.son[0].level==True):
        t.son[0].level=True
        t.level=True
        return [t.son[0]],[t.tag+'_S'],t
        #return [t.son[0]],['S'],t
    elif t.son[0].isleaf or t.son[0].level==True:
        tl.append(t.son[0])
        tgl.append('O')
    else:
        _tl,_tgl,_tson=get_tree_tag_list(t.son[0])
        tl.extend(_tl)
        tgl.extend(_tgl)
        t.son[0]=_tson
    if len(t.son)==2:
        if t.son[1].isleaf or t.son[1].level==True:
            tl.append(t.son[1])
            tgl.append('O')
        else:
            _tl,_tgl,_tson=get_tree_tag_list(t.son[1])
            tl.extend(_tl)
            tgl.extend(_tgl)
            t.son[1]=_tson
    return tl,tgl,t
def tree_get_tag_feature(tree):#a root
    if tree.isleaf:#
        return []
    features=[]
    while True:
        if tree.level==True or (len(tree.son)==1 and tree.son[0].level==True):
            #only one node,no need to reduce
            break
        treel,tagl,tree=get_tree_tag_list(tree)
        i=0
        while i<len(treel):
            if tagl[i]!='O':###有tag
                type_tag=2####2叉
                if tagl[i].split('_')[1]=='S':#单叉
                    type_tag=1
                feature=get_tag_feature_final(treel,i,type_tag)
                # features.append(tagl[i].split('_')[0]+\
                #                 '\t'+'\t'.join(feature))
                features.append('\t'.join(feature)+\
                                '\t'+tagl[i].split('_')[0].rstrip('*'))
                if type_tag!=1:
                    i+=1
            i+=1
        #features.append('')#a section####!!!
    ######
    return features
def update_level(t):####划分节点层次
    t.level=False
    if t.isleaf:
        t.level=True
        return t
    newson=[]
    ##no two son###
    if len(t.son)>2:
        print t.show()###error
    for son in t.son:
        nd=update_level(son)
        newson.append(nd)
    t.son=newson
    return t
def get_svm_format(fn,resf):
    def get_class(cl):
        global classd,classi
        try:
            classd[cl]
        except:
            classd[cl]=str(classi)
            classi+=1
        return classd[cl]
    def get_dd(cl):
        global dd,ddj
        try:
            dd[cl]
        except:
            dd[cl]=ddj
            ddj+=1
        return dd[cl]
    ###############
    res=[x.strip() for x in file(fn)]
    newres=[]
    count_num={}
    for ft in res:
        if len(ft)==0:
            continue
        ftl=ft.split('\t')
        if len(ftl[0])==0:#tag is empty
            continue
        nft=[]
        i=1
        ######except word2vec feature
        for x in ftl[1:-word2vec_len]:
            if x=='NIL':
                i+=1
                continue
            nft.append(get_dd(str(i)+x))
            # count_num[str(i)+x]=count_num.get(str(i)+x,0)+1
            i+=1
        nft=sorted(nft)
        nft=[str(x)+':1' for x in nft]
        ###
        i=1
        #######word2vec feature index
        vec_ft=[]
        for x in ftl[-word2vec_len:]:
            vec_ft.append(str(i)+':'+x)
            i+=1
        ###
        vec_ft.extend(nft)
        vec_ft.insert(0,get_class(ftl[0]))
        newres.append('\t'.join(vec_ft))
    #####
    write_file(resf,newres)
    # useless=0
    # for key in count_num.keys():
    #     if count_num[key]<=10:
    #         useless+=1
    # print 'less:',useless
def get_svm_format_test(fn,resf):
    def get_class(cl):
        return classd[cl]
    def get_dd(cl):
        return dd[cl]
    ###############
    res=[x.strip() for x in file(fn)]
    newres=[]
    count_num={}
    for ft in res:
        if len(ft)==0:
            continue
        ftl=ft.split('\t')
        if len(ftl[0])==0:#tag is empty
            continue
        try:
            classd[ftl[0]]
        except:
            continue
        nft=[]
        i=1
        ######except word2vec feature
        for x in ftl[1:-word2vec_len]:
            if x=='NIL':
                i+=1
                continue
            try:
                nft.append(get_dd(str(i)+x))
            except:
                pass
            # count_num[str(i)+x]=count_num.get(str(i)+x,0)+1
            i+=1
        nft=sorted(nft)
        nft=[str(x)+':1' for x in nft]
        ###
        i=1
        #######word2vec feature index
        vec_ft=[]
        for x in ftl[-word2vec_len:]:
            vec_ft.append(str(i)+':'+x)
            i+=1
        ###
        vec_ft.extend(nft)
        vec_ft.insert(0,get_class(ftl[0]))
        newres.append('\t'.join(vec_ft))
    #####
    write_file(resf,newres)
#############
def CTB_split_tag_main(src_file,resf):
    tl=[x.strip().decode('utf8') for x in file(src_file)]#[:10]
    print len(tl)
    res=[]
    #####
    a=open(resf,'w')
    a.close()
    #####
    i=0
    for line in tl:
        if len(line)==0:
            continue
        t=read_tree(line)
        if len(t.get_words())==1:
            continue
        if t.tag=='S' and len(t.son)==1:
            t=t.son[0]
        t=CCG_head(t)
        t=update_level(t)
        features=tree_get_tag_feature(t)
        res.extend(features)
        i+=1
        if i%2000==0:
            print i
            write_file_add(resf,res)
            res=[]
    write_file_add(resf,res)
def get_file_and_dict(srcf1,resf2,resf3):
    global classd,classi,dd,ddj
    classd={}
    dd={}
    classi=1
    ddj=word2vec_len+1###word2vec feature start from 1~word2vec_len
    CTB_split_tag_main(srcf1,resf2)
    #get_svm_format(resf2,resf3)
    print 'tag_num:',classi
    print 'feature_num:',ddj##
    tagd=dict(zip([int(x) for x in classd.values()],
                  classd.keys()))
    cPickle.dump(tagd,file(tag_dict_file,'wb'))
    cPickle.dump(dd,file(feature_dict_file,'wb'))
def get_test_file(srcf1,resf2,resf3):
    global classd,dd
    # tagd=cPickle.load(file(tag_dict_file,'rb'))
    # dd=cPickle.load(file(feature_dict_file,'rb'))
    # classd=dict(zip(tagd.values(),
    #                 [str(x) for x in tagd.keys()] ))
    CTB_split_tag_main(srcf1,resf2)
    #get_svm_format_test(resf2,resf3)
if __name__=='__main__':
    pass
    #load_word2vec('./temp/word2vec/word2vec_train_vec50.txt')
    #tag_model=tag_model_class()
    # get_file_and_dict(_filename,_res_file,_res_file2)
    # get_test_file(_filename_test,_res_file_test,_res_file2_test)
    get_test_file(_filename,_res_file,_res_file2)
    print 'done'








    
    
