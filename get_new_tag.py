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
import cPickle
from CCG_head import CCG_head
from CCG_tree import read_tree
from sklearn import tree
import numpy as np
#get_node_new_tag(nl,i,flg[i])
version='_0405'
# version=''
_filename='files/CTB_binary2_split.txt'
_res_file='files/CTB_binary2_split_tag'+version#cmp to 2 add feature3,2,10
_res_file2='files/CTB_binary2_split_tag_svm'+version


feature_dict_file='files/feature_dict.pickle'+version
tag_dict_file='files/tag_dict.pickle'+version
# tag_model_file='model/tag_model_linux_dt.pickle'
tag_model_file='model/tag_model_linux_svm_01.pickle_all'


_filename_joint='files/CTB_binary2_piece_joint.pickle'
_res_joint_file='files/CTB_binary2_split_joint_tag'+version#cmp to 2 add feature3,2,10
_res_joint_file2='files/CTB_binary2_split_tag_joint_svm'+version


feature_dict_joint_file='files/feature_joint_dict.pickle'+version
tag_dict_joint_file='files/tag_joint_dict.pickle'+version
#tag_model_joint_file='model/tag_joint_model_linux_dt.pickle'
tag_model_joint_file='model/tag_joint_model_linux_svc_01.pickle_all'


#######
class tag_model_class:
    def __init__(self,joint=False):
        if joint==False:#piece parse
            self.tag_model=cPickle.load(file(tag_model_file,'rb'))
            self.feature_dict=cPickle.load(file(feature_dict_file,'rb'))
            self.tag_dict=cPickle.load(file(tag_dict_file,'rb'))
            self.feature_lenth=len(self.feature_dict)
        else:#joint parse
            self.tag_model=cPickle.load(file(tag_model_joint_file,'rb'))
            self.feature_dict=cPickle.load(file(feature_dict_joint_file,'rb'))
            self.tag_dict=cPickle.load(file(tag_dict_joint_file,'rb'))
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
        feature=get_tag_feature(tl,ind,type_tag)
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
def get_tag_feature(ts,ind,type_tag):#get a feature list
    #type_tag,1 for unary,2 for binary
    def get_head_child(t):
        tag=t.tag
        if t.isleaf:
            tag='NIL'
        ftt=[tag,t.head_pos]####add t.tag
        if len(t.son)==0:
            ftt.append('2')###############2 for no son
            #ftt.extend(['NIL','NIL'])
        elif len(t.son)==1:###change:1-15,crf3.txt
            ftt.append('3')###############3 for single
            #ftt.extend(['NIL','NIL'])
        elif t.head==t.son[0].head:
            ftt.append('0')##############0 for first son is head
            #ftt.extend(get_head(t.son[1]))
        else:
            ftt.append('1')##############1 for last son is head
            #ftt.extend(get_head(t.son[0]))
        return ftt
    ft=[]
    none_tag=['NIL','NIL','NIL']
    ###
    if ind-1>=0:
        ft.extend(get_head_child(ts[ind-1]))
    else:
        ft.extend(none_tag)
    ft.extend(get_head_child(ts[ind]))###
    if type_tag==2:
        if ind+1<len(ts):
            ft.extend(get_head_child(ts[ind+1]))
        else:
            ft.extend(none_tag)
        if ind+2<len(ts):
            ft.extend(get_head_child(ts[ind+2]))
        else:
            ft.extend(none_tag)
    else:####type_tag==1
        ft.extend(none_tag)
        if ind+1<len(ts):
            ft.extend(get_head_child(ts[ind+1]))
        else:
            ft.extend(none_tag)
    ###
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
        if tree.level==True:#or (len(tree.son)==1 and tree.son[0].level==True):
            #only one node,no need to reduce
            break
        treel,tagl,tree=get_tree_tag_list(tree)
        i=0
        while i<len(treel):
            if tagl[i]!='O':###有tag
                type_tag=2####2叉
                if tagl[i].split('_')[1]=='S':#单叉
                    type_tag=1
                feature=get_tag_feature(treel,i,type_tag)
                features.append(tagl[i].split('_')[0]+\
                                '\t'+'\t'.join(feature))
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
    for ft in res:
        if len(ft)==0:
            continue
        ftl=ft.split('\t')
        nft=[]
        i=1#######
        for x in ftl[1:]:#0 for tag
            if x=='NIL':
                i+=1
                continue
            nft.append(get_dd(str(i)+x))
                ####str(i),diff in 2:NN,4:NN
            # except:
            #     dd[x]=str(ddj)
            #     ddj+=1
            #     nft.append(get_dd(str(i)+x))####
            i+=1
        nft=sorted(nft)
        nft=[str(x)+':1' for x in nft]
        nft.insert(0,get_class(ftl[0]))
        newres.append('\t'.join(nft))
    write_file(resf,newres)
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
        #####???####
        if t.tag=='S' and len(t.son)==1:
            t=t.son[0]
        t=CCG_head(t)
        t=update_level(t)
        features=tree_get_tag_feature(t)
        res.extend(features)
        i+=1
        if i%10000==0:
            print i
            write_file_add(resf,res)
            res=[]
    write_file_add(resf,res)
def get_file_and_dict():
    global classd,classi,dd,ddj
    classd={}
    dd={}
    classi=1
    ddj=0
    CTB_split_tag_main(_filename,_res_file)
    get_svm_format(_res_file,_res_file2)
    print classi,ddj##
    tagd=dict(zip([int(x) for x in classd.values()],
                  classd.keys()))
    cPickle.dump(tagd,file(tag_dict_file,'wb'))
    cPickle.dump(dd,file(feature_dict_file,'wb'))
def CTB_split_tag_main_joint(src_file,resf):
    print 'load pickle'
    tl=cPickle.load(open(src_file,'rb'))
    print len(tl)
    res=[]
    #####
    a=open(resf,'w')
    a.close()
    #####
    i=0
    for t in tl:
        if len(t.get_words())==1:
            continue
        if t.tag=='S' and len(t.son)==1:
            t=t.son[0]
        t=CCG_head(t)
        ###t=update_level(t)
        features=tree_get_tag_feature(t)
        res.extend(features)
        i+=1
        if i%1000==0:
            print i
            write_file_add(resf,res)
            res=[]
    write_file_add(resf,res)
def get_file_and_dict_joint():
    global classd,classi,dd,ddj
    classd={}
    dd={}
    classi=1
    ddj=0
    print 'start get joint tag'
    CTB_split_tag_main_joint(_filename_joint,_res_joint_file)
    get_svm_format(_res_joint_file,_res_joint_file2)
    print classi,ddj##
    tagd=dict(zip([int(x) for x in classd.values()],
                  classd.keys()))
    cPickle.dump(tagd,file(tag_dict_joint_file,'wb'))
    cPickle.dump(dd,file(feature_dict_joint_file,'wb'))
if __name__=='__main__':
    pass
    #tag_model=tag_model_class()
    #get_file_and_dict()
    #get_file_and_dict_joint()
    print 'done'










    
    
