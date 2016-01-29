__author__ = 'hdz'

from piece_feature import res_file as res_file_parse
from piece_joint_feature import res_file as res_file_joint
res_file_parse=res_file_parse+'_res'
res_file_joint=res_file_joint+'_res'

def count_tag(lines,ind):
    res={'S':set([]),'B':set([]),
         'E':set([]),'O':set([]),
         'tag':set([])}
    flag=0
    i=0
    for line in lines:
        i+=1
        if line=='':
            continue
        fls=line.split('\t')
        tag=fls[ind]
        item='%d%s' % (i,tag)
        res['tag'].add(item)
        if flag!=0:
            if flag==1 and tag!='BI':
                print i
            elif flag==-1 and tag!='E':
                print i
        elif tag=='BI' or tag=='E':
            print i
        flag=0
        if tag=='O':
            res['O'].add(item)
        elif tag=='S':
            res['S'].add(item)
        elif tag=='B':
            res['B'].add(item)
            flag=1
        elif tag=='EI':
            res['E'].add(item)
            flag=-1
        elif tag not in ['BI','E']:
            print tag
    #print len(res['O'])
    return res

def count_PRF_main(rd,sd):
    def count_PRF(rs,ss):
        total=len(rs)
        sys=len(ss)
        right=len(rs.intersection(ss))
        P=right*1.0/max(sys,0.001)
        R=right*1.0/max(total,0.001)
        F=2*P*R/max(P+R,0.001)
        #print total,sys,right
        return [P,R,F,total,sys,right]
    actions=['S','B','E','O','tag']
    prf={}
    for key in actions:
        prf[key]=count_PRF(rd[key],sd[key])
    real_action=rd['S'].union(rd['B']).union(rd['E'])
    sys_action=sd['S'].union(sd['B']).union(sd['E'])
    prf['action']=count_PRF(real_action,sys_action)
    return prf
def main(file_name):
    lines=[x.rstrip() for x in file(file_name)]
    real_d=count_tag(lines,-2)
    sys_d=count_tag(lines,-1)
    F_d=count_PRF_main(real_d,sys_d)
    for key in F_d.keys():
        print key+':'
        print 'total:%d\tsys:%d\tright:%d' % \
              (F_d[key][3],F_d[key][4],F_d[key][5])
        print 'Precise:%f\tRecall:%f\tF1:%f' %\
              (F_d[key][0],F_d[key][1],F_d[key][2])
if __name__=='__main__':
    pass
    print res_file_parse,res_file_joint
    print 'parse:'
    main(res_file_parse)
    print 'joint:'
    main(res_file_joint)
    print 'done'

