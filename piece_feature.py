# -*- coding: cp936 -*-
'''
target:transform a pieces data to crf format for pieces parse
author:hdz
time:2014-10-13 21:45:48
#B,BI,EI,E,S,O
'''
import re
import cPickle
from CCG_head import CCG_head
from CCG_tree import read_tree
from find_piece_5 import version
filename='files/ctb_8_test_right_split_res.txt'
res_file='files/ctb_8_test_right_piece_crf_no_xing.txt'

_filename='files/CTB_binary2_split.txt'+version
_res_file='files/CTB_binary2_piece_crf_no_xing.txt'+version#crfcmp to 2 add feature3,2,1,0

pbracket=re.compile('{[^{}]+?}')
nounl=['n','nR','nS','nP','vN','nO','rN','aN']

feature_list=range(22)
##feature_list=[str(x) for x in feature_list]
#######
def write_file(fn,res):
    with open(fn,'w') as ff:
        ff.write('\n'.join(res).encode('utf8','ignore'))
    print 'write done'
def write_file_add(fn,res):
    with open(fn,'a') as ff:
        ff.write('\n'.join(res).encode('utf8','ignore')+'\n')
    print 'write done'
####
def get_feature(ts,ind):#a tree list
    #ti-2,ti-1,ti,ti+1,ti+2#
##    def get_head(t):
##        return [t.head,t.head_pos]
    def get_head_child(t):
        ftt=[t.tag.rstrip('*'),t.head,t.head_pos]####add t.tag
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
    ###
    ft.extend(get_head_child(ts[ind]))
    ###
    #print ft
    return '\t'.join(ft)
def get_nodel_feature(nodel):
    res=[]
    for i in range(len(nodel)):
        res.append(get_feature(nodel,i))
    return res
def get_tree_list(t):
    #son's level==-1 or isleaf=>to be joined
    tl=[]#all nodes 
    tgl=[]#node tags
    #是否是叶子节点或者终止节点(已被处理后的节点level=-1)
    if (t.son[0].isleaf or t.son[0].level==-1) and\
       len(t.son)==2 and\
       (t.son[1].isleaf or t.son[1].level==-1):
        t.son[0].level=-1
        t.son[1].level=-1
        t.level=-1#####CHANGE, 变为处理后的节点
        if t.head==t.son[0].head:###
            #return [t.son[0],t.son[1]],[t.tag+'_B',t.tag+'_BI'],t
            return [t.son[0],t.son[1]],['B','BI'],t
        #return [t.son[0],t.son[1]],[t.tag+'_EI',t.tag+'_E'],t
        return [t.son[0],t.son[1]],['EI','E'],t
    if len(t.son)==1 and (t.son[0].isleaf or t.son[0].level==-1):
        t.son[0].level=-1
        t.level=-1
        #return [t.son[0]],[t.tag+'_S'],t
        return [t.son[0]],['S'],t
    elif t.son[0].isleaf or t.son[0].level==-1:
        tl.append(t.son[0])
        tgl.append('O')
    else:
        _tl,_tgl,_tson=get_tree_list(t.son[0])
        tl.extend(_tl)
        tgl.extend(_tgl)
        t.son[0]=_tson
    if len(t.son)==2:
        if t.son[1].isleaf or t.son[1].level==-1:
            tl.append(t.son[1])
            tgl.append('O')
        else:
            _tl,_tgl,_tson=get_tree_list(t.son[1])
            tl.extend(_tl)
            tgl.extend(_tgl)
            t.son[1]=_tson
    return tl,tgl,t
def tree_get_feature(tree):#a root
    if tree.isleaf:#
        return []
    features=[]
    while True:
        if tree.level==-1 or\
           (len(tree.son)==1 and tree.son[0].level==-1):
            #only one node,no need to reduce
            break
        treel,tagl,tree=get_tree_list(tree)
        i=0
        while i<len(treel):
            feature=get_feature(treel,i)
            features.append(feature+'\t'+tagl[i])
            i+=1
        features.append('')#a section
    ######
    return features
def update_level(t,lv=0):####划分节点层次
    t.level=lv
    if t.isleaf:
        return t
    newson=[]
    ##no two son###
    if len(t.son)>2:
        print t.show()###error
##    if len(t.son)==1:
##        t=t.son[0]
##        while not t.isleaf and len(t.son)==1:
##            t=t.son[0]
    for son in t.son:
        nd=update_level(son,lv+1)
        newson.append(nd)
    t.son=newson
    return t
def CCG_feature_main(src_file,resf):
    tl=[x.strip().decode('utf8') for x in file(src_file)]
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
        features=tree_get_feature(t)
        res.extend(features)
        i+=1
        if i%10000==0:
            print i
            write_file_add(resf,res)
            res=[]
    write_file_add(resf,res)
if __name__=='__main__':
    pass
    # CCG_feature_main(filename,res_file)
    CCG_feature_main(_filename,_res_file)
    ##to get train and test##
    #CCG_feature_main_test(_filename,'files/piece_parse_train.txt')
    print 'done'



