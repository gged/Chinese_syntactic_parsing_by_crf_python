# -*- coding: cp936 -*-
import sys,time
from MultiTree import *
import pygraphviz as pgv
from configure import pwd_path
'''
default graph file:tree.png
G.add_node(u"经理", fontname="Microsoft YaHei", shape="rect", style="rounded", fontsize=18) #雅黑
G.add_node(u"秘书", fontname="SimHei") #黑体
G.add_node(u"小兵", fontname="SimSun") #宋体
G.add_node(u"小卒", fontname="Kaiti") #楷体
'''

default_coding='gbk'

class treeWriter():
    def __init__(self, tree):
        self.num = 1       #mark each visible node as its key
        self.tree = tree
        self.fontname="Microsoft YaHei"
        
    def write(self, outfile = 'tree.png'):
        def writeHelp(root, A):
            if not root:
                return
            
            p = str(self.num)
            self.num += 1###
            A.add_node(p, label = root.elem,fontname=self.fontname)
            son_num=[]
            nnsons=list(root.nsons)
            ###inorder more decent###
            if len(nnsons)==2:
                nnsons.insert(1,None)
            if len(nnsons)==0:###leaves have not circle
                n=A.get_node(p)
                n.attr['color']='white'
            for son in nnsons:
                if son==None:
                    anum = str(self.num)
                    self.num += 1
                    A.add_node(anum, style = 'invis')
                    A.add_edge(p,anum, style = 'invis')
                    son_num.append(anum)
                    continue
                anum=writeHelp(son, A)
                A.add_node(anum, label = son.elem)
                A.add_edge(p,anum)
                son_num.append(anum)
            if son_num!=[]:
                B = A.add_subgraph(son_num, rank = 'same')
                for i in xrange(0,len(son_num)-1):
                    B.add_edge(son_num[i], son_num[i+1], style = 'invis')
            
            return p  #return key root node
        ##########
        self.A = pgv.AGraph(directed=False,strict=True)#arrow
        #self.A.node_attr['shape']='rect'
        #self.A.node_attr['color']='black'
        writeHelp(self.tree.root, self.A)
        self.A.graph_attr['epsilon']='0.001'
        #print self.A.string() # print dot file to standard output
        self.A.layout('dot') # layout with dot
        #'neato'|'dot'|'twopi'|'circo'|'fdp'|'nop'
        self.A.draw(outfile) # write to file        
def draw_graph(text,ind):
    try:
        sen=text.strip()
        print 'show',sen
        if not sen.startswith('(') or\
                not sen.endswith(')'):
            print 'tree error'
            return
        tree = MultiTree()
        tree.createTree(sen)
        writer = treeWriter(tree)
        outfile=pwd_path+'graph/'+str(ind)+'_'+time.strftime('%m-%d-%H:%M:%S')+'.png'
        writer.write(outfile)
        del tree, writer
        #return '/home/hdz/Desktop/QA/tree.png'
        print outfile
    except:
        print 'error'
def draw_graph_main(text):
    ind=0
    for sen in text.split('\n'):
        if len(sen.strip())<=1:
            continue
        draw_graph(sen,ind)
        ind+=1
if __name__ == '__main__':
    tree = MultiTree()
    ##sen a CTB tree##
    sen='(IP (VP (ADVP (AD 全面))(VP (VV 推行)(NP (NP (NN 教育)(NN 收费))(NP (NN 公示)(NN 制度)))))(PU 。))'
    sen='(IP (IP (NP (CP (IP (NP (ADJP (JJ 超级))(NP (NN 病菌)))(VP (VV 出现)))(DEC 的))(NP (NN 根源)))(VP (VV 在于)(IP (NP (NN 人们))(VP (PP (P 在)(LCP (IP (VP (VV 患病)))(LC 时)))(VP (VV 滥用)(NP (NN 抗生素)))))))(PU 。))'
    tree.createTree(sen.decode(default_coding))
##    print '###'
##    tree.preorderTravel()
##    print '###'
    writer = treeWriter(tree)
    if len(sys.argv) > 1:#your graph file name
        outfile = sys.argv[1]
        writer.write(outfile) #write result to outfile
    else:
        writer.write() #write result to tree.png
    

