# -*- coding: cp936 -*-
'''
target:find_CCG_head
author:hdz
time:2014-7-28 12:40:04
TODO:get head table,find all pos meaning
'''
import re
import cPickle

is_test=True
is_test=False
######
#tag:(0/1,[head]),o for left
head_table={
    'ADJP':(1,['ADJP','JJ']),
    'ADVP':(1,['ADVP','AD']),
    'CP':(1,['CP','IP']),
    'DNP':(1,['DNP','DEG']),
    'DP':(0,['DP','DT']),
    'INTJ':(0,['INTJ','IJ']),
    'IP':(1,['IP','VP']),
    'LCP':(1,['LCP','LC']),
    'NP':(1,['NP','NN','NT','NR','QP']),
    'NP-PN':(1,['NP','NN','NT','NR','QP']),
    'PP':(0,['PP','P']),
    'QP':(1,['QP','CD','OD']),
    'VP':(1,['VP','VA','VC','VE','VV','BA','LB','VCD','VSB','VRD','VNV','VCP']),
    'VV':(1,['VV']),
    'VA':(1,['VA']),
    'VE':(1,['VE']),
    'VC':(1,['VC']),
    'VCD':(1,['VCD','VV','VA','VC','VE']),
    'VRD':(1,['VRD','VV','VA','VC','VE']),
    'VSB':(1,['VSB','VV','VA','VC','VE']),
    'VCP':(1,['VCP','VV','VA','VC','VE']),
    'VNV':(1,['VNV','VV','VA','VC','VE']),
    'FRAG':(0,['NP','NN','NT','NR','VCD','VV','VA','VC','VE','VP'])####add by hdz
    }

def find_head(t):#return index
    if len(t.son)==1:
        return 0
    tag=t.tag
    if tag.endswith('*'):
        tag=tag.rstrip('*')
    try:
        di,tb=head_table[tag]
        if di==0:#left
            for i in range(len(t.son)):
                if t.son[i].head_pos in tb:
                    return i
            return 0
        else:
            i=len(t.son)-1
            while i>=0:
                if t.son[i].head_pos in tb:
                    return i
                i-=1
            return len(t.son)-1
    except:
        pass
    return len(t.son)-1
def CCG_head(t):
    if t.isleaf:
        t.head=t.word
        t.head_pos=t.pos
        #print t.head,t.head_pos
        return t
    else:
        for son in t.son:
            nson=CCG_head(son)
        if len(t.son)==1:#unary
            t.head=t.son[0].head
            t.head_pos=t.son[0].head_pos
        elif len(t.son)==2:
            direct=find_head(t)
            if direct==2:#无结果，默认1
                pass
                #print t.show()
                t.head=t.son[1].head
                t.head_pos=t.son[1].head_pos
            elif direct==0:# 0 for left
                t.head=t.son[0].head
                t.head_pos=t.son[0].head_pos
            else:# 1 for right
                t.head=t.son[1].head
                t.head_pos=t.son[1].head_pos
            #print t.head,t.head_pos
        else:
            pass
            print '3 son?'
    return t
def write_file(fn,res):
    with open(fn,'w') as ff:
        ff.write('\n'.join(res).encode('utf8','ignore'))
    print 'write done'
def CCG_head_main(fn,resf):
    allt=cPickle.load(open(fn,'rb'))
    print 'trees:',len(allt)
    i=0
    res=[]
    temp=[]
    while len(allt)>0:
        i+=1
        if i%1000==0:
            print i
        t=allt.pop(0)
        if t=='':####blank
            res.append('')####
            if is_test:temp.append('')
            continue
        #print i+1
        t=CCG_head(t)
        res.append(t)
        if is_test:temp.append(t.show_pos()+'\t\t\t'+t.head+'/'+t.head_pos)
    #####
    cPickle.dump(res,open(resf,'wb'),True)
    if is_test:write_file('files/temp',temp)
    #return res
if __name__=='__main__':
    pass
    #CCG_head_main(new_CCG_pos_file,new_CCG_head_file)
    #CCG_head_main(new_test_CCG_pos_file,new_test_CCG_head_file)
    #
    CCG_head_main(filename,file_head)
    #CCG_head_main(_filename,_file_head)
    print 'done'






