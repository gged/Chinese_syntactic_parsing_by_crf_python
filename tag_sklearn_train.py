from sklearn import svm
from sklearn.datasets import load_svmlight_file
from sklearn import metrics
##from sklearn.naive_bayes import GaussianNB
##from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
##from sklearn.linear_model import LogisticRegression
import cPickle
##import pickle
from tag_sklearn import model_name,feature_file,calculate_result,use_model
import sys,os,time
##################
print '******************************************'
#feature_file="./files/CTB_binary2_split_tag_joint_svm.txt"

TRAIN=True
# TRAIN=False

if __name__=='__main__':
    X_, Y_ = load_svmlight_file(feature_file)
    print X_.shape

    if not TRAIN:
        model_name=model_name+'_all'
        #model_name='./model/tag_joint_model_linux_dt.pickle'
        X_test,Y_test=X_[-2000:], Y_ [-2000:]
        X_test=X_test.toarray()

        clf=cPickle.load(file(model_name,'rb'))

        pred = clf.predict(X_test)
        calculate_result(Y_test,pred)
        ##############
    else:
        X_train,Y_train=X_, Y_
        X_train=X_train.toarray()
        print 'start train'
        clf = use_model()
        if len(sys.argv)==3:
            clf=use_model(int(sys.argv[1]))
            model_name=sys.argv[2]
        print repr(clf)
        clf.fit(X_train,Y_train)
        cPickle.dump(clf,file(model_name+'_all','wb'),True)
        print 'model name',model_name+'_all'



