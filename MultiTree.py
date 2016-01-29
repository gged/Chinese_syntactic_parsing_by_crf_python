'''
author:hdz
time:2015-3-14 23:05:53
'''
class Node():
    '''
    node will be used in MultiTree
    '''
    def __init__(self,elem):
        self.elem = elem
        self.nsons = []
    def __str__(self):
        return self.elem

class MultiTree():
    def __init__(self, root = None):
        self.root = root
    
    def createTree(self, sen = None):
        '''create a MultiTree'''
        def get_root_elem(parse_str):
            parse_str=parse_str.strip()
            while parse_str[0]=='(':
                if parse_str[-1]==')':
                    parse_str=parse_str[1:-1].strip()
                else:
                    return None,''
            if parse_str.strip()=='':
                return None,''
            pss=parse_str.split(' ')
            if len(pss)==1:
                return pss[0],''
            return pss[0],' '.join(pss[1:])
        def get_elems(son_str):
            stk=[]
            count=0
            tmp=''
            for x in son_str:
                tmp+=x
                if x=='(':
                    count+=1
                elif x==')':
                    count-=1
                    if count==0:
                        stk.append(tmp)
                        tmp=''
                if x==' ' and count==0:
                    tmp=''
            if tmp!='':
                stk.append(tmp)
            return stk
        def get_son_elems(son_str):
            son_str=son_str.strip()
            if son_str=='':
                return []##end
            stk=get_elems(son_str)#get sons
            return stk
        def createTreeHelp(parse_str):
            elem,son_str = get_root_elem(parse_str)
            if elem==None:
                return None
            #print 'node',elem
            root = Node(elem)
            root.nsons=[]#
            sons=get_son_elems(son_str)
            #print sons
            for son in sons:
                root.nsons.append(createTreeHelp(son))
            return root
        #######
        #print sen
        elem,son_str = get_root_elem(sen)
        self.root = Node(elem)
        #print 'root',elem
        sons=get_son_elems(son_str)
        #print sons
        for son in sons:
            leaf=createTreeHelp(son)
            if leaf:
                self.root.nsons.append(leaf)
        
    def preorderTravel(self):
        def preorderTravelHelp(root):
            if not root:
                return 
            print(root.elem)
            for son in root.nsons:
                preorderTravelHelp(son)      
        preorderTravelHelp(self.root)
if __name__ == '__main__':
    tree = MultiTree()
    tree.createTree('(np (dd xx) (nn pp))'.decode('gbk'))
    print '###'
    tree.preorderTravel()
