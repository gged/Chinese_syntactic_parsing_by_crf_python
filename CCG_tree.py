# -*- coding: cp936 -*-
'''
target:read CCG parse tree,read_tree
author:hdz
time:2014-7-25 17:02:33
##----##
note:所有的原文的()最好变为中文的
##----##
'''
import re
import copy
import math
import random
pblank=re.compile('  +')
max_ind=10000

percent=-0.2

pbraces=re.compile('{[^{}]+?}')
class root:
    def __init__(self):
        self.isleaf=False
        self.tag='S'
        self.son=[]
        self.head=''
        self.head_pos=''
        self.level=0
    def __eq__(self,other):#equal
        return self.show_tree()==other.show_tree()
    def add_son(self,new_node):
        self.son.append(new_node)
    def show_S(self):
        ss=''
        for son in self.son:
            ss+=son.show()
        return '('+self.tag+' '+ss+')'
    def show(self):
        ss=''
        for son in self.son:
            ss+=son.show()
        return '('+' '+ss+' '+')'
    def show_tree(self):
        ss=''
        for son in self.son:
            ss=ss+son.show_tree()+'\n'
        ss=ss[:-1]
        return '('+' '+ss+' '+')'
    def show_pos(self):
        ss=''
        for son in self.son:
            ss+=son.show_pos()
        return '('+' '+ss+' '+')'
    def show_head(self):
        ss=''
        for son in self.son:
            ss+=son.show_head()
        return '('+self.head+'/'+self.head_pos+' '+ss+' '+')'
    def get_words(self):
        wl=[]
        for son in self.son:
            wl.extend(son.get_words())
        return wl
    def __str__(self):
        return self.show().encode('utf8')
class node:
    def __init__(self,aleaf=False,atag='',aword='',apos='',aparent='',ahead='',ahead_pos='',alevel=1):
        self.isleaf=aleaf
        self.tag=atag##
        self.word=aword#word
        self.pos=apos##
        self.parent=aparent#father
        self.level=alevel#deep
        self.son=[]#children
        self.head=ahead
        self.head_pos=ahead_pos
        #is leaf
        if self.isleaf:
            self.pos=atag
            self.head=aword
            self.head_pos=atag
    def add_son(self,new_node):
        self.son.append(new_node)
    def show_pos(self):
        if self.isleaf:
            return '('+self.pos+' '+self.word+')'
        else:
            ss=''
            for son in self.son:
                ss+=son.show_pos()
            return '('+self.tag+' '+ss+')'
    def show_head(self):
        if self.isleaf:
            return '('+self.pos+' '+self.word+')'
        else:
            ss=''
            for son in self.son:
                ss+=son.show_head()
            return '('+self.head+'/'+self.head_pos+' '+ss+')'
    def show(self):
        if self.isleaf:
            return '('+self.tag+' '+self.word+')'
        else:
            ss=''
            for son in self.son:
                ss+=son.show()
            if self.tag!='':
                return '('+self.tag+' '+ss+')'
            else:
                return ss
    def show_tree(self):
        if self.isleaf:
            return '('+self.tag+' '+self.word+')'
        else:
            ss=self.son[0].show_tree()
            for son in self.son[1:]:
                ss=ss+'\n'+'\t'*self.level+son.show_tree()
            return '('+self.tag+' '+ss+')'
    def get_words(self):
        if self.isleaf:
            return [(self.word,self.tag)]
        wl=[]
        for son in self.son:
            if son.isleaf:
                wl.append((son.word,son.tag))
            else:
                wl.extend(son.get_words())
        return wl
    def __str__(self):
        return self.show().encode('utf8')
################
def read_tree(s):
    ###string to tree###
    try:
        s=s.decode('utf8')
    except:
        #print 'no utf8!'
        pass
    s=pblank.sub(' ',s)##
    #s=s.replace('[','(').replace(']',')')
    if s.count('(')!=s.count(')'):
        print 'tree () number error'
        return None
    ########
    r=root()
    try:
        s=s.strip()#get rid of NO
        #print s
    except:
        print 'tree lenth error'
        return None
    s=change_for_CCG(s)
    nd,ind=precreate_tree(r,s,0,0)
    if nd==None:
        return None
    r.add_son(nd)
    ########
    return r
def change_for_CCG(s):
#old#
#'((NP-OBJ (QP (CD 一) (CLP (M 系列))) (CP (WHNP-3 (-NONE- *OP*)) (CP (IP (NP-SBJ (-NONE- *T*-3)) (VP (VV 规范) (NP-OBJ (NN 建设) (NN 市场)))) (DEC 的))) (NP (NN 文件))))'
#new#
#'1  [np 中国/nS  [np 传统/a  医学/n  ] ] ' 
    try:
        s=s[s.index('\t'):].strip()
    except:
        s=s.strip()
##    sp=s.split(' ')
##    temp=[]
##    for x in sp:
##        if x.find('/')==-1:
##            temp.append(x)
##        else:
##            xx=x.split('/')[::-1]
##            temp.append('('+' '.join(xx)+')')
##    s=' '.join(temp)
##    #s='( '+s+' )'
##    #print 'change:',s
    return s
def precreate_tree(t,ss,ind,lv):
    #tree,ss,ind,level
    def get_tag(ss2,ind2):
        i=ind2
        #print ss2[i]
        while ss2[i]!=' ' and ss2[i]!=')':
            i+=1
        #print 'item',ss2[ind2:i]
        atag=ss2[ind2:i].strip()
        return atag,i
    def get_word(ss2,ind2):
        i=ind2
        #print ss2[i]
        while ss2[i]!=' ' and ss2[i]!=')':
            i+=1
        #print 'item',ss2[ind2:i]
        aword=ss2[ind2:i].strip()
        if aword=='':###(PU )#blank
            aword=' '
        return aword,i
    def test_item(ss2,ind2):
        while ss2[ind2]==' ':
            ind2+=1
        #print 'test',ss2[ind2]
        return ss2[ind2],ind2
    ##############
    try:
        #print 'new',ss[ind:]
        if ss[ind]=='(':
            tag,ind=get_tag(ss,ind+1)
            ch,ind=test_item(ss,ind+1)
            if ch=='(':#not leaf
                #print 'not:',ss[ind:]
                nd=node(atag=tag,aparent=t,alevel=lv+1)
                while ch=='(':
                    new_nd,ind=precreate_tree(t,ss,ind,lv+1)
                    nd.add_son(new_nd)###son
                    ch,ind=test_item(ss,ind)
                return nd,ind+1#end#)
            else:#leaf
                word,ind=get_word(ss,ind)
                #print 'leaf',word
                nd=node(aleaf=True,atag=tag,aword=word,aparent=t,alevel=lv+1)
                return nd,ind+1#end#)
    except:
        return None,max_ind
#######
def write_file(fn,res):
    with open(fn,'w') as ff:
        ff.write('\n'.join(res).encode('utf8','ignore'))
    print 'write done'
def get_word_file(fn,resf,resf2):
    global percent
    kind={}
    fp=open(fn,'r')
    res=[]
    res2=[]
    i=0
    for line in fp:
        if len(line.strip())!=0:       
            t=read_tree(line)
            wl=t.get_words()
            for w in wl:
                tag=w[1]
                tag=pbraces.sub('',tag)
                try:
                    kind[tag]+=1
                except:
                    kind[tag]=1
            wl=[x[0]+' '+pbraces.sub('',x[1]) for x in wl]
            wl.append('')#
            if random.random()>percent:
                res.extend(wl)
            else:
                res2.extend(wl)
        i+=1
        if i%1000==0:
            print i
            print len(res),len(res2)
    print 'all:',len(res),len(res2)
    print 'kind:',len(kind)
    a=kind.keys()
    a=sorted(a,key=lambda x:-kind[x])
    a=[x+'\t'+str(kind[x]) for x in a]
    write_file('files/kind.txt',a)
    write_file(resf,res)
    write_file(resf2,res2)
def get_sen(t):
    if t.isleaf:
        return t.word
    else:
        sen=''
        for son in t.son:
            sen=sen+get_sen(son)
        return sen
def get_sentence(fn,resf):
    lines=[x.strip().decode('utf8') for x in file(fn)]
    res=[]
    i=0
    for line in lines:
        if len(line.strip())>0:
            ind=line.split('\t')[0]
            t=read_tree(line)
            sen=get_sen(t)
            res.append(ind+'\t'+''.join(sen))
        i+=1
        if i%1000==0:
            print i


    write_file(resf,res)
if __name__=='__main__':
    pass
    ####
    #get_sentence('files/testCCG.txt','files/testCCG_sen.txt')
    #get_sentence('files/CCGBank-NewsAcd-Ver20.ccg','files/CCGBank_sen.txt')
    #get_word_file('files/testCCG.txt','files/CCG_word.txt','files/ddd')
    #get_word_file('files/CCGBank-NewsAcd-Ver20.ccg','files/CCG_word.txt','files/ddd')
    #get_pos_file('files/ParsEval-2010-Task22.CPT','files/pos_train.txt','files/pos_test.txt')
    s='''chtb_001.fid	( (IP (NP (NP-PN (NR 上海)(NR 浦东))(NP (NP* (NP* (NN 开发)(CC 与))(NN 法制))(NN 建设)))(VP (VV 同步))) )'''.decode('gbk')

    t=read_tree(s)
    print t.show()
    print t.show_tree()
    wl=t.get_words()
    #print wl
    for x in wl:
        print x[0],x[1]
    print 'done'











