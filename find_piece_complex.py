# -*- coding: cp936 -*-
'''
target:CTB find split sen
author:hdz
time:2015-1-5 23:03:12
'''
import re
import cPickle
import copy
from CCG_tree import node,read_tree
max_len=5#5,6,7
version='_len_'+str(max_len)+'_BME'
test_file='files/ctb_8_test_right.txt'
res_file='files/ctb_8_test_right_split_res.txt'+version
piece_joint_file='files/ctb_8_test_right_split_joint.pickle'+version
res_crf_file='files/ctb_8_test_right_split_res_crf.txt'+version

_test_file='files/CTB_binary2.txt'
_res_file='files/CTB_binary2_split.txt'+version
_piece_joint_file='files/CTB_binary2_piece_joint.pickle'+version#for piece joint crf src file
_res_crf_file='files/CTB_binary2_split_crf.txt'+version
##
is_test=True
##is_test=False
split_pos=['PU']#
split_punc='， 。 ？ ！ ： '.decode('gbk').split(' ')
# crf_tag_list=[['S'],['B','E'],['B','B2','E'],\
#               ['B','B2','E2','E']]
crf_tag_list=[['S'],['B','E']]###MMEEEE
#特殊p:把被用将
##nosplit_p='把 被 用 将'.decode('gbk').split(' ')
##nosplit_c='和 或 及 以及 与 或者 同'.decode('gbk').split(' ')
##split_verb='使 是'.decode('gbk').split(' ')
#分割标记,一些主观的动词v+j
def write_file(fn,res):
    with open(fn,'w') as ff:
        ff.write('\n'.join(res).encode('utf8','ignore'))
    #print 'write done'
def piece_to_crf_data(src_file,res_file):
    '''已分块的文本,进行crf标记
    (vp)\n(np)   
    '''
    def crf_str_add(aw,tag):
        return (aw[0],aw[1],tag)
    def tag_wl(wll):
        #B,B2,M,E2,E,S
        crf_str=[]
        lenth=len(wll)
        '''
        if lenth<=4:
            i=0
            for x in crf_tag_list[lenth-1]:
                crf_str.append(crf_str_add(wll[i],x))
                i+=1
        else:
            crf_str.append(crf_str_add(wll[0],'B'))
            crf_str.append(crf_str_add(wll[1],'B2'))
            for x in wll[2:-2]:
                crf_str.append(crf_str_add(x,'M'))
            crf_str.append(crf_str_add(wll[-2],'E2'))
            crf_str.append(crf_str_add(wll[-1],'E'))
        '''
        if lenth<=2:
            i=0
            for x in crf_tag_list[lenth-1]:
                crf_str.append(crf_str_add(wll[i],x))
                i+=1
        else:
            crf_str.append(crf_str_add(wll[0],'B'))
            for x in wll[1:-1]:
                crf_str.append(crf_str_add(x,'M'))
            crf_str.append(crf_str_add(wll[-1],'E'))#######MMMEEEE
        #'''
        crf_str=['\t'.join(x) for x in crf_str]
        return '\n'.join(crf_str)
    lines=[x.strip().decode('utf8') for x in file(src_file)]#[:10]
    res=[]
    i=0
    for line in lines:
        if len(line.strip())>0:
            t=read_tree(line)
            wl=t.get_words()
            #print wl
            tag_piece=tag_wl(wl)
            res.append(tag_piece)
        else:#end of sentence
            res.append('')
        i+=1
        if i%1000==0:
            print i
    write_file(res_file,res)
def check_is_single_leaf(t):
    if t.isleaf:
        return True
    elif len(t.son)==1:
        return check_is_single_leaf(t.son[0])
    return False
def tag_split(t):
    if check_is_single_leaf(t):
        #print 'root',t.word
        t.level=False
        return t
    for son in t.son:       #a not splitpunc son is leaf,return it
        if check_is_single_leaf(son):
            if son.tag in split_pos and\
                son.word in split_punc:
                continue
            else:           #no complex son
                #print son.word
                t.level=False
                return t
    t.son=[tag_split(son) for son in t.son]
    t.level=True
    return t
def check_lenth(nt):
    def check_tag_not_equal(t1,t2):
        tag1=t1.tag
        tag2=t2.tag
        tag1=tag1.split('-')[0].rstrip('*')
        tag2=tag2.split('-')[0].rstrip('*')
        return tag1!=tag2
    if len(nt.get_words())<=max_len:
        return [nt]
    ntl=[]
    if len(nt.son)==2:
        if check_tag_not_equal(nt.son[0],nt.son[1]) or len(nt.get_words())>=10:
            ntl.extend(check_lenth(nt.son[0]))
            ntl.extend(check_lenth(nt.son[1]))
        else:
            ntl.append(nt)
    elif len(nt.son)==1:
        ntl.extend(check_lenth(nt.son[0]))
    else:
        print '3 sons'
        for son in nt.son:
            ntl.extend(check_lenth(son))
    return ntl
def get_split_nodel(nt):
    nodel=[]
    if nt.level==False:
        nodel.append(nt)
    else:
        for son in nt.son:
            if son.level==False:
                # nodel.append(son)
                nodel.append(son)
            else:
                nodel.extend(get_split_nodel(son))
    return nodel
    # if nt.level==True or nt.isleaf:
    #     # nodel.append(nt)
    #     nodel.extend(check_lenth(nt))
    # else:
    #     for son in nt.son:
    #         if son.level==True or son.isleaf:
    #             # nodel.append(son)
    #             nodel.extend(check_lenth(son))
    #         else:
    #             nodel.extend(get_split_nodel(son))
    # return nodel
def split_main(t):#####主函数
    #nodel=[]
    nt=tag_split(t)
    nodel=get_split_nodel(nt)
    #print len(nodel)
    return nodel
def split_sen(fn,resf):
    lines=[x.strip().decode('utf8') for x in file(fn)]#[:1]
    res=[]
    i=0
    for line in lines:
        if len(line.strip())>0:
            t=read_tree(line)
            tl=split_main(t)
            for node in tl:
##                while not node.isleaf and len(node.son)==1:
##                    node=node.son[0]
                res.append(node.show())
            res.append('')
        i+=1
        if i%1000==0:
            print i
    write_file(resf,res)
########
def split_for_piece_joint_file(fn,resf):
    lines=[x.strip().decode('utf8') for x in file(fn)]
    res=[]
    i=0
    for line in lines:
        if len(line.strip())>0:
            t=read_tree(line)
            nt=tag_split(t)
            res.append(nt)
        i+=1
        if i%1000==0:
            print i
    cPickle.dump(res,file(resf,'wb'),True)
if __name__=='__main__':
    pass
    # split_sen(test_file,res_file)
    # split_for_piece_joint_file(test_file,piece_joint_file)
    # piece_to_crf_data(res_file,res_crf_file)
    #
    # split_sen(_test_file,_res_file)
    # split_for_piece_joint_file(_test_file,_piece_joint_file)
    # piece_to_crf_data(_res_file,_res_crf_file)
    # print 'done'
    sen=read_tree('( (IP (IP (NP-PN (NR 澳洲))(VP (VV 面对)(NP (CP (IP (VP (ADVP (AD 有史以来))(ADVP (AD 最))(VP (VA 严酷))))(DEC 的))(NP (NN 干旱)))))(PU ，)(IP (NP (NP-PN (NR 澳洲))(NP (NN 宗教)(NN 团体)))(VP (NP (NT 今天))(VP (VV 举行)(NP (ADJP (JJ 全国性))(NP (NN 祈雨)(NN 活动))))))(PU 。)) )'.decode('gbk'))
    sen=read_tree('(IP (IP (IP (AD 例如)(IP (VP (LCP (P 在)(LCP (NP (NN 工作))(LC 上)))(FRAG (VV 遭到)(FRAG (NN 惩戒)(NP (CC 或)(NN 开除)))))))(IP (IP (PU ，)(IP (CC 或是)(IP (IP (NP (NP (PN 他们))(DEG 的))(IP (NN 妻子)(NP (CC 或)(NN 丈夫))))(VP (VRD (VV 扬言)(VV 要))(IP (VV 离开)(NP (PN 他们)))))))(IP (PU ，)(IP (IP (VP (NP (PN 他们))(VP (ADVP (AD 才))(NP (NP (VV 了解)(NP (IP (LCP (DP (DT 这))(NP (NN 表面)))(LC 上))(NP (IP (ADVP (AD 看来))(VP (VA 无害)))(DEC 的))))(NP (NN 行为))))))(IP (PU ，)(VP (ADVP (AD 已))(VP (NP (P 为)(NP (PN 他们)))(NP (VV 带来)(NP (NP (CD 一)(NP (ADJP (JJ 大))(CLP (M 堆))))(NP (NN 问题)))))))))))(PU 。))'.decode('gbk'))
    sen=read_tree('''
    ( (IP (NP-PN (NR 劳瑞))(VP (VV 表示)(PU ，)(IP (NP (PN 他))(VP (VV 认为)(IP (NP (DP (DT 这)(CLP (M 场)))(NP (NN 全国))(NP (NN 祈雨)(NN 活动)))(PU ，)(VP (VV 显示)(IP (NP (NN 城市)(NN 居民))(VP (ADVP (AD 正))(VP (VV 开始)(VP (VV 了解)(PU ，)(NP (CP (IP (NP (NN 干旱))(VP (PP (P 对)(NP (NN 乡下)(NN 地区)))(VP (MSP 所)(VP (VV 造成)))))(DEC 的))(NP (NN 冲击))))))))))))(PU 。)) )
                  '''.decode('gbk'))
    ntl=split_main(sen)
    for st in ntl:
        print st.show()














    





