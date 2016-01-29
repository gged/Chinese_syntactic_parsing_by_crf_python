# -*- coding: cp936 -*-
__author__ = 'hdz'
'''
get pcfg prob for kbest(beam search)
'''
from CCG_tree import node,read_tree
from collections import defaultdict
from math import log
import cPickle
file_name='files/ctb_8_test_binary2.txt'
_file_name='files/CTB_binary_no_xing'
pcfg_pickle_file='model/CTB_binary_no_xing_pcfg'
pcfg_d=defaultdict(lambda:defaultdict(int)) #

def record_tree_pcfg(node):
    if node.isleaf:
        return
    f_tag=node.tag.strip('*')
    if f_tag!='':
        son_tag=[son.tag for son in node.son]
        pcfg_d[f_tag][tuple(son_tag)]+=1
    for son in node.son:
        record_tree_pcfg(son)
def count_pcfg_prob(fn):
    # get the prob model, attention to the 'tag*'
    global pcfg_d
    pcfg_d.clear()
    pcfg_model={}
    i=0
    for line in file(fn):
        tree=read_tree(line)
        record_tree_pcfg(tree)
        i+=1
        if i%1000==0:
            print 'get pcfg prob:',i,len(pcfg_d)
    for f_tag in pcfg_d:
        total=sum(pcfg_d[f_tag].values())
        pcfg_model[f_tag]={}
        for son_tag in pcfg_d[f_tag]:
            # log
            pcfg_model[f_tag][son_tag]=log(1.0*pcfg_d[f_tag][son_tag]/total)
    cPickle.dump(pcfg_model,file(pcfg_pickle_file,'w'))
    return pcfg_model
def get_node_pcfg_prob(pcfg_model,f_tag, son_tag):
    try:
        return pcfg_model[f_tag][tuple(son_tag)]
    except:
        #print 'zero pcfg prob:', f_tag, tuple(son_tag)
        return log(0.0001)
    #return 1.0
def count_score(nodel,pcfg_model): # get the tree score
    # todo get pcfg, done
    father_tag=nodel.tag
    son_tag=[son.tag for son in nodel.son]
    prob=get_node_pcfg_prob(pcfg_model, father_tag, son_tag)
    return prob
if __name__=='__main__':
    #d=count_pcfg_prob(file_name)
    #d=count_pcfg_prob(_file_name)
    d=cPickle.load(file(pcfg_pickle_file,'r'))
    print len(d)
    print d.keys()
    #print d['NP'][('VV','NP',)]# tuple
    print d['VP'][('VV','NP',)]# tuple
    print d['ADVP'][tuple(['AD'])]# tuple
    print 'done'


