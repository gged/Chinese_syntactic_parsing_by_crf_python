__author__ = 'hdz'
from CCG_tree import read_tree
file_name='files/ctb_8_test_right_split_res_crf_res.txt'
# file_name='files/ctb_8_test_right_split_res_crf.txt_len_5.res_BME'
# file_name='files/ctb_8_test_right_split_res_crf.txt_len_5.res_BME_f2'
# file_name='files/ctb_8_test_right_split_res_crf.txt_len_5.res'
# file_name='files/ctb_8_test_right_split_res_crf.txt_len_5.res5_BM'

old_file='files/ctb_8_test_right.txt'
word_ind=0
def old_eval():
    lines=[x.rstrip() for x in file(file_name)]
    res1=[]
    res2=[]
    start=0
    start2=0
    i=0
    for line in lines:
        i+=1
        if line=='':
            continue
        fls=line.split('\t')
        tag1=fls[-2]
        tag2=fls[-1]
        if tag1 in ["B"]:
            start=i
        if tag2 in ["B"]:
            start2=i
        if tag1 == "E":
            res1.append((start,i))
        if tag1 == "S":
            res1.append((i))
        if tag2 == "E":
            res2.append((start2,i))
        if tag2 == "S":
            res2.append((i))
    total_len=len(res1)
    sys_len=len(res2)
    print len(res1),len(res2)
    right=set(res1).intersection(set(res2))
    right_len=len(right)
    print len(right)
    P=right_len*1.0/sys_len
    R=right_len*1.0/total_len
    F=2*P*R/(P+R)
    print 'pre:',P
    print 'rec:',R
    print 'F1:',F
def read_res_data():
    lines=[x.rstrip() for x in file(file_name)]
    res1=[]
    start=-1
    line_num=0
    i=0
    tree_num=0
    size_list=[]
    for line in lines:
        line_num+=1
        if line=='':
            size_list.append(i)
            tree_num+=1
            i=0
            start=-1
            continue
        fls=line.split('\t')
        tag1=fls[-1]
        if tag1 in ["B"]:
            if start!=-1:
                if i-start==1:
                    res1.append((tree_num,start))
                else:
                    res1.append((tree_num,start,i-1))
            start=i
        if tag1 == "E":
            if start==-1:
                print 'E',line_num
            res1.append((tree_num,start,i))
            start=-1
        if tag1 == "S":
            if start!=-1:
                if i-start==1:
                    res1.append((tree_num,start))
                else:
                    res1.append((tree_num,start,i-1))
            res1.append((tree_num,i))
            start=-1
        i+=1
    if i!=0:
        size_list.append(i)
    if start!=-1:
        if i-start==1:
            res1.append((tree_num,start))
        else:
            res1.append((tree_num,start,i-1))
    return res1,size_list
def number_tree(t):
    global word_ind
    if t.isleaf:
        t.word=word_ind
        word_ind+=1
    else:
        nson=[]
        for son in t.son:
            nson.append(number_tree(son))
        t.son=nson
    return t
def get_t_ind(t,tnum):
    if t.isleaf:
        return (tnum,t.word)
    ls=t.son[0]
    while not ls.isleaf:
        ls=ls.son[0]
    start=ls.word
    rs=t.son[-1]
    while not rs.isleaf:
        rs=rs.son[-1]
    end=rs.word
    if start!=end:#binary
        return (tnum,start,end)
    else:#unary
        return (tnum,start)
def get_pieces_ind(t,tnum):
    temp=[]
    temp.append(get_t_ind(t,tnum))
    for son in t.son:
        temp.extend(get_pieces_ind(son,tnum))
    return temp
def get_pieces(t,tnum,size):
    global word_ind
    words=t.get_words()
    lenth=len(words)
    if lenth!=size:
        print tnum,lenth,size
        return []
    word_ind=0
    t=number_tree(t)
    return get_pieces_ind(t,tnum)

def read_right_data(size_list):
    lines=[x.rstrip().decode('utf8') for x in file(old_file)]
    tree_num=0
    res2=[]
    for line in lines:
        t=read_tree(line)
        pieces=get_pieces(t,tree_num,size_list[tree_num])
        res2.extend(pieces)
        tree_num+=1
    return res2
def analyse_pieces(res,hit):
    short_res=[x for x in res if len(x)==2]
    long_res=[x for x in res if len(x)!=2]
    print 'short num:%d\nlong num:%d' % (len(short_res),len(long_res))
    short_hit=hit.intersection(set(short_res))
    long_hit=hit.intersection(set(long_res))
    print 'short pre:',len(short_hit)*1.0/len(short_res)
    print 'long pre:',len(long_hit)*1.0/len(long_res)
    lenth_l=[x[-1]-x[-2] for x in long_res]
    average_len=sum(lenth_l)*1.0/len(long_res)
    print 'long averge len:',average_len
    for i in xrange(2,20):
        _res=[x for x in long_res if x[-1]-x[-2]==i]
        _hit=hit.intersection(set(_res))
        try:
            print 'long, size=%d number:%d\tprecise:%f' % (i,len(_res),len(_hit)*1.0/len(_res))
        except:
            print 'long, size=%d number:%d\tprecise:%f' % (i,0,0)
    _res=[x for x in long_res if x[-1]-x[-2]>9]
    _hit=hit.intersection(set(_res))
    print 'long, size>%d number:%d\tprecise:%f' % (9,len(_res),len(_hit)*1.0/len(_res))
    sum_long_lenth=sum([x[2]-x[1] for x in long_res])
    sum_short_lenth=len(short_res)
    sum_error_lenth=sum_long_lenth-sum([x[2]-x[1] for x in long_hit])
    print 'error_lenth_rate:%f' % (sum_error_lenth*1.0/(sum_long_lenth+sum_short_lenth))

def new_eval():
    res,sl=read_res_data()
    right=read_right_data(sl)
    res=set(res)
    right=set(right)
    hit=right.intersection(res)
    analyse_pieces(res,hit)
    total=len(res)
    precise=len(hit)*1.0/total
    print 'pieces total Precise:',precise
if __name__=='__main__':
    old_eval()
    print '######'
    new_eval()
    print 'done'

