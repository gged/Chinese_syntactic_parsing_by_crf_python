# -*- coding: cp936 -*-
__author__ = 'hdz'
'''
server for piece_parse.py and piece_joint_parse.py
'''

from CCG_tree import node
from get_new_tag_model import get_new_tag_main
from collections import defaultdict
from get_new_tag2 import get_tag_feature_final

is_test=True
is_test=False

def get_new_nodel(nl,flg): # tag model, node list, tag model(if any)
    # get new nodel list by the crf tag
    # return: [(nodel, diff_node)]
    # todo find kbest one by one changed and record the diff,done
    nodel_l=[]
    i=0
    while i<len(flg):
        if flg[i]!=3:
            new_nl=nl[:i]
            if flg[i]==0:#####BBBBB######
                a=node()
                a.son=[nl[i],nl[i+1]]
                a.head=nl[i].head
                a.head_pos=nl[i].head_pos
                #new_nl=nl[:i]
                new_nl.append(a)
                new_nl+=nl[i+2:]
                #nodel_l.append(a)
                i+=1
            elif flg[i]==1:####EEEEE###
                a=node()
                a.son=[nl[i],nl[i+1]]
                a.head=nl[i+1].head
                a.head_pos=nl[i+1].head_pos
                #new_nl=nl[:i]
                new_nl.append(a)
                new_nl+=nl[i+2:]
                #nodel_l.append(a)
                i+=1
            elif flg[i]==2:############SSSS######
                a=node()
                a.son=[nl[i]]
                a.head=nl[i].head
                a.head_pos=nl[i].head_pos
                #new_nl=nl[:i]
                new_nl.append(a)
                new_nl+=nl[i+1:]
                #nodel_l.append(a)
            else:
                print '?'
            if flg[i]==2:
                # fts=get_tag_feature_final(ts,ind,type_tag)
                fts=get_tag_feature_final(nl,i,1)
                nodel_l.append((new_nl,i,fts))# new node list, diff son
            else:
                # todo,attention!!!!!!<<i-1>>
                fts=get_tag_feature_final(nl,i-1,2)
                nodel_l.append((new_nl,i-1,fts))# new node list, diff son
            #nodel_l[-1].tag=ntag
        else:
            pass
            #nodel_l.append(nl[i])
        i+=1 ################todo,notify
    return nodel_l
def find_change(nl,flg,tgs):
    #to find a max prob for change the tree
    #print tgs
    maxprob=-1.0
    indi=0
    flgtp=0
    i=0
    if is_test:print len(nl)
    while i<len(nl):#####可以优化
        ###
        if i+1<len(nl):
            prob1=tgs[i][1]['B']*tgs[i+1][1]['BI']
            prob2=tgs[i][1]['EI']*tgs[i+1][1]['E']
            if prob1>maxprob:
                maxprob=prob1
                indi=i
                flgtp=0
            if prob2>maxprob:
                maxprob=prob2
                indi=i
                flgtp=1
        ########hdz
        if len(nl[i].son)!=1 or nl[i].son[0].isleaf:
            # todo,in case of S->S->S bug,done
            prob3=tgs[i][1]['S']#**2#
            if prob3>maxprob:
                maxprob=prob3
                indi=i
                flgtp=2
        ########
        i+=1
    if is_test:print flgtp
    flg[indi]=flgtp
    if flgtp!=2:
        flg[indi+1]=flgtp
    return flg
def check_SSS(nl,flg,tgs):
    '''
    check SSS error
    '''
    #SSS=False
    i=0
    while i<len(nl):
        if flg[i]==2:
            try:
                if len(nl[i].son)==1:
                    #SSS=True
                    flg[i]=3
                    #break
            except:
                1
        i+=1
    # if SSS:flg=find_change(nl,flg,tgs,no_S=True)
    return flg
def change_nodel(nl,tgs):
    # return: [(nodel, diff_node)]
    # print len(nl),len(tgs)
    i=0
    flag=[]# record the crf tag
    while i<len(nl):
        #0 for B,1 for E,2 for single,3 for other
        #################################
        if tgs[i][0]=='B' and i+1<len(nl) and tgs[i+1][0]=='BI':
            flag.extend([0,0])#two son
            i+=1
        elif tgs[i][0]=='EI' and i+1<len(nl) and tgs[i+1][0]=='E':
            flag.extend([1,1])#two son
            i+=1
        elif tgs[i][0]=='S' and\
             (len(nl[i].son)!=1 or nl[i].son[0].isleaf):
             # todo,in case of S->S->S bug,done
            flag.append(2)
        else:
            flag.append(3)#pass
        i+=1
    if flag.count(3)==len(flag):####no change
        if is_test:print 'ddd'
        flag=find_change(nl,flag,tgs)
    #print flag
    #flag=check_SSS(nl,flag,tgs) #S->S->S bug, at most two S tags
    ####
    nodel=get_new_nodel(nl,flag)
    return nodel
#######################
# def get_piece_parsed(tm,nodel):#返回树节点结构
#     while True:
#         if len(nodel)==1:
#             return nodel[0]
#         fts=get_nodel_feature(nodel)
#         #tmp='tmp'#write feature file
#         write_file(piece_parse_tmp,fts)
#         crftags=piece_parse_model_test(piece_parse_tmp)#get result
#         nodel=change_nodel(tm,nodel,crftags)
#         #print nodel
#     return nodel[0]#最后只剩下一个节点
########################
def get_undone(kb,beam_size): #split finished and todo may be be the same tree
    newkb=[]
    string_d=defaultdict(int)
    for nl in kb: #todo,delete the same tree
        string=''.join([node.show() for node in nl[0]])
        if string_d[string]==0:
            newkb.append(nl)
            string_d[string]+=1
    kb=list(newkb)
    kb=sorted(kb,key=lambda x:-x[-1])               #sorted by pcfg
    kb=kb[:beam_size]                               #best beam_size
    done=[item for item in kb if len(item[0])==1]   #todo 假如是单枝的可能还要继续,done
    undone=[item for item in kb if len(item[0])!=1]
    return done,undone

if __name__=='__main__':
    pass
    print 'done'