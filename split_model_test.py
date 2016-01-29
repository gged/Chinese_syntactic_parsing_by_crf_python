# -*- coding: cp936 -*-
import sys
import os
from CCG_tree import node
from configure import pwd_path, crfpath
is_test=False#True#False#False for train
is_test=True#

version='_BME'#_f2
#crfpath='/home/hdz/CRF/'
modelpath=pwd_path+'model/'

#model_name=modelpath+'CTB_piece_model_6_24_len_5'+version#'_BME_f2'# todo,old
model_name=modelpath+'CTB_piece_model_1_8'# todo, find what is it?
# version='7_BME'
# model_name=modelpath+'CTB_piece_model_7_3_len_'+version

crftest=crfpath+'crf_test'
crftrain=crfpath+'crf_learn'
# res_crf_file='files/ctb_8_test_right_split_res_crf.txt'
# test_file='files/split_sen_temp'#
train_file=pwd_path+'files/CTB_binary2_split_crf.txt_len_5'+version

test_file=pwd_path+'files/ctb_8_test_right_split_res_crf.txt_len_5'#+version
test_res_file=test_file+'.res'+version
#print test_res_file
tmp_file=pwd_path+'files/split_tmp.txt'
######
#print 'resf:',test_res_file
def write_file(fn,res):
    with open(fn,'w') as ff:
        ff.write('\n'.join(res).encode('utf8','ignore'))
    #print 'write done'
def test(testf,resf):
    #..\..\crf_test -m 2010_6tags_3f_model3 weibo3_3f.utf8 > weibo3_3f.tag.utf8
    #python crf_data_2_word.py weibo3_3f.tag.utf8 weibo3_3f.6tag2word.utf8
    print 'test:',testf
    cmd2='%s -m %s %s > %s' % (crftest,model_name,testf,resf)
    #print cmd2
    #os.system(cmd2+' & pause')#pause
    output=os.popen(cmd2)
    print output.read()
def train_model(trainf,modeln):
    #..\..\crf_learn -f 3 -c 4.0 template 2010_6tags3_3f.utf8 2010_6tags_3f_model3
    cmd2='%s -f 1 %spiece_template %s %s' % (crftrain,modelpath,trainf,model_name)
    #print cmd2
    #os.system(cmd2+' & pause')#pause
    #output=os.popen(cmd2)
    print cmd2
def get_res(text):#只适合一句话
    wl=text.split('\n')
    wl=[x.decode('utf8').split() for x in wl]#unicode
    res=[(x[0],x[1],x[-1]) for x in wl if len(x)>1]#word,pos,split tag
    return res
def split_model_test(testf):
    #print 'test:',testf
    cmd2='%s -m %s %s' % (crftest,model_name,testf)
    #cmd2='%s -v2 -m %s %s > %s' % (crftest,model_name,testf,temp_file)
    #print cmd2
    #os.system(cmd2+' & pause')#pause
    output=os.popen(cmd2)
    res_text=output.read()#读取终端的输出
    #print res_text
    #print res_text
    #time.sleep(0.1)
    #print res_text
    res=get_res(res_text)
    return res
def get_pieces(res):
    pieces=[]
    tmpl=[]
    for w in res:
        #####
        nnode=node(aleaf=True,aword=w[0],atag=w[1],apos=w[1])
        if w[-1] in ['B','S']:###
            if len(tmpl)!=0:
                pieces.append(tmpl)
                tmpl=[]
        if w[-1]=='E':
            tmpl.append(nnode)
            pieces.append(tmpl)
            tmpl=[]
        elif w[-1]=='S':
            tmpl.append(nnode)
            pieces.append(tmpl)
            tmpl=[]
        else:
            tmpl.append(nnode)
    if len(tmpl)!=0:
        pieces.append(tmpl)
    return pieces
def split_sen(wl):
    sen=[x[0]+'\t'+x[1] for x in wl]
    #print sen
    write_file(tmp_file,sen)
    res=split_model_test(tmp_file)
    #print res
    pieces=get_pieces(res)
    return pieces
####
def main():
    if is_test:
        test(test_file,test_res_file)
    else:
        print 'train:',train_file
        train_model(train_file,model_name)

if __name__=='__main__':
    pass
    print model_name
    main()
    #res=split_model_test(test_file)
    print 'done'

