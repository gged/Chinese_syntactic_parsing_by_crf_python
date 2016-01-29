from CCG_tree import read_tree

file_name='files/CTB_binary2.txt'

result_file='files/CTB_binary_no_xing'

test_file='files/ctb_8_test_right.txt'
test_pos_file='files/ctb_8_test_right_pos.txt'

def delete_xing(t):
    if t.isleaf:
        return t
    t.tag=t.tag.rstrip('*')
    nson=[]
    for son in t.son:
        son=delete_xing(son)
        nson.append(son)
    t.son=nson
    return t
def get_stanford_train():
    lines=[x.rstrip().decode('utf8') for x in file(file_name)]
    res=[]
    for line in lines[:]:
        if len(lines)==0:
            continue
        t=read_tree(line)
        t=delete_xing(t)
        res.append(t.show())
    with open(result_file,'w') as ff:
        ff.write('\n'.join(res).encode('utf8'))
def get_stanford_test():
    lines=[x.rstrip().decode('utf8') for x in file(test_file)]
    res=[]
    maxlen=0
    for line in lines[:]:
        t=read_tree(line)
        ws=t.get_words()
        sen=[x[0]+'/'+x[1] for x in ws]
        lenth=len(sen)
        if lenth>100:
            print ' '.join(sen).encode('utf8')
        if lenth>maxlen:
            maxlen=lenth
        res.append(' '.join(sen))
    print maxlen
    with open(test_pos_file,'w') as ff:
        ff.write('\n'.join(res).encode('utf8'))
if __name__=='__main__':
    #get_stanford_train()
    get_stanford_test()
