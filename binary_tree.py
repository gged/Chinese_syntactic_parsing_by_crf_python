# -*- coding: cp936 -*-
'''
target:binary tree
author:hdz
time:2014-12-25 22:41:43
TODO:判断中心词，具体的多叉树的划分方法
'''
from copy import deepcopy
from CCG_tree import read_tree,node
from CCG_head import find_head

# file1='files/CTB.txt'
# file2='files/CTB_binary2.txt'
file1='files/ctb_8_test.txt'
file2='files/ctb_8_test_binary2.txt'
end_punc='， 。 ？ ！ ： '.decode('gbk').split(' ')
def check_all_leaf(t):
    for son in t.son:
        if not son.isleaf:
            return False
    return True
def binary_left(leftson,sons,tag):
    #check?
    new_son=[]
    new_son=[sons[0],sons[1]]
    new_node=node(atag=tag+'*')
    new_node.son=new_son
    
    if len(leftson)==0:
        return new_node
    else:
        return binary_left(leftson[:-1],[leftson[-1],new_node],tag)
def binary_right(rightson,sons,tag):
    #check?
    new_son=[]
    new_son=[sons[0],sons[1]]
    new_node=node(atag=tag+'*')
    new_node.son=new_son
    
    if len(rightson)==0:
        return new_node
    else:
        return binary_right(rightson[1:],[new_node,rightson[0]],tag)##right!!
def multi_2_binary_normal(t,tag):
    #((l h) r)
    if t.son[-1].isleaf and t.son[-1].word in end_punc:
        tt=deepcopy(t)
        tt.son=tt.son[:-1]
        new_son=multi_2_binary_normal(tt,tag)
        t.son=[new_son,t.son[-1]]
        return t
    ind=find_head(t)#find head
    new_son=[]
    if ind!=0:
        lnode=binary_left(t.son[:ind-1],t.son[ind-1:ind+1],tag)
    else:
        lnode=t.son[0]
    if ind==len(t.son)-1:
        lnode.tag=tag
        return lnode
    else:
        new_node=binary_right(t.son[ind+2:],[lnode,t.son[ind+1]],tag)
        new_node.tag=tag
        return new_node
def get_son_join(sonl,tag):
    new_node=node(atag=tag+'*')
    new_node.son=[sonl[-2],sonl[-1]]
    if len(sonl)==2:
        return new_node
    else:
        sonll=sonl[:-2]
        sonll.append(new_node)
        return get_son_join(sonll,tag)
def check_item_complete(t,tag):
    ###合并并列每一项中不是只有一个叶子的，生成一个新的节点
    nsonl=[]
    temp=[]
    for son in t.son:####
        if son.tag=='PU' or son.tag=='CC':
            if len(temp)!=0:
                if len(temp)==1:
                    nsonl.append(temp[0])
                else:#
                    nsonl.append(get_son_join(temp,tag))
            nsonl.append(son)
            temp=[]
        else:
            temp.append(son)
    if len(temp)!=0:
        if len(temp)!=len(t.son):
            if len(temp)==1:
                nsonl.append(temp[0])
            else:
                nsonl.append(get_son_join(temp,tag))
    if len(temp)!=len(t.son):
        t.son=nsonl
    if len(t.son)==3 and t.son[1].tag=='CC':#
        if not t.son[0].isleaf:
            t.son[0].tag=tag
        if not t.son[-1].isleaf:
            t.son[-1].tag=tag 
    return t

def multi_2_binary_trick(t,tag):#all leaf
    if len(t.son)<=2:
        return t
    elif t.son[-1].tag=='ETC' or t.son[-1].word in end_punc:#**等,**。
        tt=deepcopy(t)
        tt.son=tt.son[:-1]
        new_son=multi_2_binary_trick(tt,tag)
        t.son=[new_son,t.son[-1]]
        return t
    elif t.son[0].tag==t.son[-1].tag=='PU' and\
         len(t.son[0].word)==len(t.son[-1].word)==1 and\
         abs(ord(t.son[0].word)-ord(t.son[-1].word))==1:#"**",<>
        tt=deepcopy(t)
        tt.son=tt.son[1:-1]
        new_son1=multi_2_binary_trick(tt,tag)
        new_son2=node(atag=tag+'*')
        new_son2.son=[new_son1,t.son[-1]]
        t.son=[t.son[0],new_son2]####t.son[0]!!!
        return t
    t=check_item_complete(t,tag)###每一项都是完整的一项了
    if len(t.son)>2:
        t=get_son_join(t.son,tag)
        t.tag=t.tag.rstrip('*')

    ###check n1 cc n2
    return t
def binary_tree(t):
    if t.isleaf:
        return t
    new_son=[]
    for tson in t.son:
        new_son.append(binary_tree(tson))
    t.son=new_son
    if len(new_son)>2:
        if check_all_leaf(t):#son全是叶子
            t=multi_2_binary_trick(t,t.tag)
            #t.tag=t.tag.rstrip('*')
        else:#一般的
            t=multi_2_binary_normal(t,t.tag)
            #t.tag=t.tag.rstrip('*')
    return t
def binary_tree_main(t):
    #默认中心词是最后一个词
    if len(t.son)!=1:
        print t.show()
    else:
        t.son[0]=binary_tree(t.son[0])
    return t
def main():
    a=[x.strip().decode('utf8') for x in file(file1)]#[:10]
    res=[]
    for x in a:
        tid=x.split('\t')[0]
        t=read_tree(x)
        t2=binary_tree_main(t)
        w1=t.get_words()
        w2=t.get_words()
        if w1!=w2:
            print 1
        if t2!=None:
            res.append(tid+'\t'+t2.show())
        else:
            print a
        if len(res)%1000==0:
            print len(res)
    with open(file2,'w') as ff:
        ff.write('\n'.join(res).encode('utf8'))
    print len(res)
if __name__=='__main__':
    main()
    print 'done'
