from sklearn import svm
from sklearn.datasets import load_svmlight_file
from sklearn import metrics
##from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from sklearn.linear_model import LogisticRegression
import cPickle
##import pickle

version='_0408_50_svm'
# feature_file="./files/CTB_binary2_split_tag_joint_svm.txt"
feature_file="./files/CTB_binary2_union_tag_svm"+version

# model_name='./model/tag_joint_model_linux_rfc_01.pickle'
model_name='./model/tag_model_linux_dt_01.pickle'+version

def use_model(ind=0):
    model_list=[tree.DecisionTreeClassifier(criterion='entropy'),svm.LinearSVC(),
                svm.SVC(kernel = 'linear'),LogisticRegression(),
                RandomForestClassifier(n_estimators=100)]
    return model_list[ind]


def calculate_result(actual,pred):  
    right=[1 for x,y in actual,pred if x==y]
    right=sum(right)*1.0

    print 'f1-score:{0:.3f}'.format(right/len(pred))
##################
print '******************************************'
if __name__=='__main__':

    X_, Y_ = load_svmlight_file(feature_file)
    print X_.shape

    X_train,Y_train=X_[:10000], Y_ [:10000]

    X_train=X_train.toarray()
    print 'start train'

    clf = use_model()
    print repr(clf)

    clf.fit(X_train,Y_train)
    X_test,Y_test=X_[-1000:], Y_ [-1000:]
    X_test=X_test.toarray()
    #f1-score:0.892#f1-score:0.942#f1-score:0.955#all_97.4
    pred = clf.predict(X_test)
    calculate_result(Y_test,pred)
    cPickle.dump(clf,file(model_name,'wb'),True)




