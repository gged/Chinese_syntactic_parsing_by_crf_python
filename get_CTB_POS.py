# -*- coding: cp936 -*-
import os,re
from configure import ctb_seg_pos_path
in_file=ctb_seg_pos_path+'in.txt'
out_file=ctb_seg_pos_path+'out.txt'
original =['.',',','!','?','(',')',':',';','/','%',\
           '0','1','2','3','4','5','6','7','8','9']
character=['。','，','！','？','（','）','：','；','／','％',\
           '０','１','２','３','４','５','６','７','８','９']
character=[cha.decode('gbk') for cha in character]
# original ='.,!?():;/%0123456789'
# character='。，！？（）：；／％０１２３４５６７８９'.decode('gbk')
# table = maketrans(original,character)
word_dict=dict(zip(original, character))
ptranslate = re.compile('|'.join(map(re.escape, word_dict)))
def replace_words(text): #translate some character
     def translate(mat):
         return word_dict[mat.group(0)]
     return ptranslate.sub(translate, text)
def get_CTB_POS(query):
    '''
    query: unicode,seged
    string: unicode
    '''
    query=replace_words(query)
    with open(in_file,'w') as ff: #write sen
        ff.write(query.encode('gbk'))
    cmd=ctb_seg_pos_path+'ctbparser_pos %s %s' %\
        (in_file,out_file)
    output=os.popen(cmd)
    output.close()
    of=open(out_file)
    string=of.read()
    of.close()
    string=string.decode('gbk')
    return string
def get_CTB_SEG_POS(query):
    '''
    query: unicode,seged
    string: unicode
    '''
    query=replace_words(query)
    with open(in_file,'w') as ff: #write sen
        ff.write(query.encode('gbk'))
    cmd=ctb_seg_pos_path+'ctbparser_seg_pos %s %s' %\
        (in_file,out_file)
    output=os.popen(cmd)
    output.close()
    of=open(out_file)
    string=of.read()
    of.close()
    string=string.decode('gbk')
    return string

if __name__=='__main__':
    get_CTB_POS('我是北京邮电大学学生.'.decode('gbk'))
    print 'done'