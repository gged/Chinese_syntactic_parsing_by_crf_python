# -*- coding: cp936 -*-
'''
target:pieces parse
piece_parse_sen(sen,flag)
#0 for 未切分
#1 for 已切分
#2 for 已切分，且有词性
author:hdz
time:2014-11-3 20:24:03
'''
import sys
import time
# from get_new_tag import tag_model_class
from get_new_tag2 import tag_model_class
from split_model_test import split_sen
from piece_parse import piece_parsed_main_sen
from piece_joint_parse import get_piece_joint
from CCG_tree import read_tree,root
from treeWriter import draw_graph_main
from read_pos_json import read_pos_json
#from get_pcfg_prob import count_pcfg_prob
import cPickle
#version='_tag_struct_sx3tag_no_xing_real'
#version='_tag_struct_sx3tag_no_xing_real_len_5_BME'
from configure import beam_size,pwd_path
from get_CTB_POS import get_CTB_POS,get_CTB_SEG_POS
#version='_tag_struct_sx3tag_no_xing_real_len_5_BME_beam_'+str(beam_size)#
#version='_tag_struct_sx3tag_no_xing_real_beam_'+str(beam_size)
version='_tag_struct_sx3tag_no_xing_real_beam_'+str(beam_size)

test_file=pwd_path+'files/ctb_8_test_binary2.txt'
result_file=pwd_path+'files/ctb_8_test_binary2_res.txt'+version
pcfg_pickle_file=pwd_path+'model/CTB_binary_no_xing_pcfg'

def write_file(fn,res):
    with open(fn,'w') as ff:
        ff.write('\n'.join(res).encode('utf8','ignore'))
    #print 'write done'
def CTB_parse_main(sen,tag_models,pcfg_model):    #tag_model_class, sentence
    ##split to pieces##
    pieces=split_sen(sen)
    #print len(pieces)
    ##piece parse##
    kbest=piece_parsed_main_sen(pieces,tag_models[0],pcfg_model)
    #return tl
    ##piece joint##
    trees=get_piece_joint(kbest,tag_models[1],pcfg_model)
    res=[]
    for node in trees: #transfer into root
        r=root()
        r.son=[node[0]]
        r.head=node[0].head #head
        r.head_pos=node[0].head_pos
        res.append([r,node[1]])
    #return tl
    #return (pieces,tl,tree)
    return res
def CTB_parse_sen(sen,flag,tag_models,pcfg_model):
    '''
    sen:a sentence when flag==0,ABC\
        a segmented sentence when flag==1,A B C\
        a word with pos list when flag==2,[word+\t+pos,...]
    flag:a flag for sen data type
    '''
    if flag==2: #2 for 已pos
        tree=CTB_parse_main(sen,tag_models,pcfg_model)
        return tree
    else:
        print 'flag(0~2)'
    return None
class CTB_class(object):
    def __init__(self):
        self.tag_models=[{},{}]# empty, tag's model based on crf model
        self.pcfg_model=cPickle.load(file(pcfg_pickle_file,'r'))
    def CTB_api(self,wl): ##wl=[(word,tag),...]
        if len(wl)==0:
            return None
        trees=CTB_parse_sen(wl,2,self.tag_models,self.pcfg_model)
        return trees
def CTB_parser_main(res,tag,out_file):
    wll=[]
    if tag=='4':
        for sen in res.split('\n'):
            if len(sen.strip())<=1:
                continue
            t=read_tree(sen)
            wl=t.get_words()#[(word,pos),,,]
            wll.append(wl)
    else:
        for sen in res.split('\n'):
            if len(sen.strip())<=1:
                continue
            wl=[]
            sen=sen.replace('  ',' ')
            pos_list=sen.split(' ')
            old_word=''
            for pos in pos_list:
                ind=pos.rfind('/')
                if ind==-1:
                    old_word=pos+' '
                    continue
                word=old_word+pos[:ind]
                old_word=''
                tag=pos[ind+1:]
                wl.append((word,tag))
            wll.append(wl)
    ctb=CTB_class()
    treel=[]
    for wl in wll:
        # print wl
        tree=ctb.CTB_api(wl)
        #print tree
        if tree is not None:
            treel.append(tree[0][0].show())
        else:
            treel.append('error')
    if out_file!='no':
        write_file(out_file,treel)
    else:
        for tree in treel:
            print tree
def CTB_main(psj=None,sen=None):
##    sen=raw_input('请输入中文句子~\n')
##    sen=sen.decode('gbk')
##    print 'sen:',sen
    ###tag model###todo old tag model
    #tag_model=tag_model_class(joint=False)
    #tag_joint_model=tag_model_class(joint=True)
    #tag_models=[tag_model,tag_joint_model]
    tag_models=[{},{}]# empty, tag's model based on crf model
    pcfg_model=cPickle.load(file(pcfg_pickle_file,'r'))
    #tag_models=[tag_model,tag_model]
    wll=[]
    if sen!=None:
        #sen='( (IP (IP (NP-PN (NR 上海)(NR 浦东))(VP (VP (LCP (NP (NT 近年))(LC 来))(VP (VCD (VV 颁布)(VV 实行))(VP* (AS 了)(NP (CP (IP (VP (VV 涉及)(NP (NP (NP (NN 经济)(NP* (PU 、)(NP* (NN 贸易)(NP* (PU 、)(NP* (NN 建设)(NP* (PU 、)(NP* (NN 规划)(NP* (PU 、)(NP* (NN 科技)(NP* (PU 、)(NN 文教)))))))))))(ETC 等))(NP (NN 领域)))))(DEC 的))(NP* (QP (CD 七十一)(CLP (M 件)))(NP (NN 法规性)(NN 文件)))))))(VP* (PU ，)(VP (VP* (VV 确保)(AS 了))(NP (DNP (NP (NP-PN (NR 浦东))(NP (NN 开发)))(DEG 的))(NP* (ADJP (JJ 有序))(NP (NN 进行))))))))(PU 。)) )'
        #sen=sen.decode('gbk')
        t=read_tree(sen)
        wl=t.get_words()#[(word,pos),,,]
        wll=[wl]
    if psj!=None:
        wll=read_pos_json(psj)
    #0for 未切分,1 for 已切分,2 for 已pos
    treel=[]
    for wl in wll:
        print wl
        treel.append(CTB_parse_sen(wl,2,tag_models,pcfg_model))
    #print tree.show()
    return treel
def test_main(tf,resf):#测试语料,已经句法分析的树
    print time.asctime()
    begin_time=time.time()
    #test_main(test_file,result_file)
    # #######
    sentence='( (CP (CP (IP (NP (CP (IP (VP (ADVP (AD 经常))(VP (VV 引发)(NP (NN 问题)))))(DEC 的))(NP (NN 网站)))(VP (ADVP (AD 未必))(VP (VC 是)(VP (ADVP (AD 最))(VP (VA 显着))))))(SP 的))(PU 。)) )'
    ts=CTB_main(psj=None, sen=sentence.decode('gbk'))
    print ts[0][0][0].show_tree()
    # for xt in t[0]:
    #     print xt[1],xt[0].show()+'\n###'
    # ####
    print time.asctime()
    print 'cost seconds:',time.time()-begin_time
    print 'done'

if __name__=='__main__':
    usage='''
    python CTB_main.py [-file/-string] [file/string] [1/2/3/4/5] [out_file/no]
    1 for sentence -> parser,like "Beijingtiananmen..."
    2 for seged sentence -> parser, like "Beijing tiananmen ..."
    3 for posed sentence - > parser,like "Beijing/NS  ..."
    4 for parsered sentence -> parser, like "((IP (NP ...)(VP ...)))"
    5 for show parsered sentence, like "((IP (NP ...)(VP ...)))",once for one sentence

    out_file for store tree
    no for directly show tree
    '''
    if len(sys.argv)==5 and\
        sys.argv[1] in ['-string','-file'] and\
        sys.argv[3] in ['1','2','3','4','5']:
        if sys.argv[1]=='-file':
            of=open(sys.argv[2],'r')
            string=of.read()
            of.close()
        else:
            string=sys.argv[2]
        try:
            string=string.decode('gbk')
        except:
            string=string.decode('utf8')
        string=string.replace('\t',' ')
        string=string.replace('  ',' ')
        tag=sys.argv[3]
        if tag=='5':
            draw_graph_main(string)
        else:
            if tag=='1':
                res=get_CTB_SEG_POS(string)
            elif tag=='2':
                res=get_CTB_POS(string)
            else:
                res=string
            CTB_parser_main(res,tag,sys.argv[4])
    else:
        print usage


