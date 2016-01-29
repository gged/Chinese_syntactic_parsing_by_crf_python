# -*- coding: cp936 -*-
'''
显示多叉树的情况
'''

from CCG_tree import read_tree,node

file1='files/CTB.txt'
file2='files/CTB_binary_check_long.txt'

def check_all_leaf(t):
    for son in t.son:
        if not son.isleaf:
            return False
    return True
def binary_tree(t):
    global res
    if t.isleaf:
        pass
    for tson in t.son:
        binary_tree(tson)
    #if len(t.son) in [3,4] and check_all_leaf(t):#>4
    if len(t.son)>2 and not check_all_leaf(t):#>4
        #print 1
        res.append(t.show())
def binary_tree_main(t):
    #默认中心词是最后一个词
    if len(t.son)!=1:
        print t.show()
    elif t.son[0].son[0].tag!='FRAG':
        binary_tree(t.son[0])
def main():
    global res
    a=[x.strip().decode('utf8') for x in file(file1)]#[:10]
    res=[]
    i=0
    for x in a:
        tid=x.split('\t')[0]
        t=read_tree(x)
        binary_tree_main(t)
        i+=1
        if i%1000==0:
            print i
    with open(file2,'w') as ff:
        ff.write('\n'.join(res).encode('utf8'))
    print len(res)
if __name__=='__main__':
    main()
    print 'done'
