# -*- coding: cp936 -*-
__author__ = 'hdz'
'''
set the system parameters
'''

beam_size=8 #beam search kbest
pwd_path='./'.decode('gbk').encode('utf8')
ctb_seg_pos_path=pwd_path+'ctbparser-master/'
crfpath='./CRF/'
if __name__=='__main__':
    print 'done'
