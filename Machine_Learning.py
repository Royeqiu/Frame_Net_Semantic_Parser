import numpy as np
import pickle
from sklearn import svm
from sklearn import linear_model
from utl import Feature_Transformer

lexicon='give'
ft = Feature_Transformer.Feature_Transformer()
training_data = np.load('data/ML_data/'+lexicon+'_training_data.npy')
label = np.load('data/ML_data/'+lexicon+'_training_label.npy')
print(training_data.shape)
t_x,v_x,index = ft.data_separation(training_data,1)
t_y = []
v_y = []
for i in range(0,len(label)):
    if i in index:
        t_y.append(label[i])
    else:
        v_y.append(label[i])

t_y = ft.to_nparray(t_y)
v_y = ft.to_nparray(v_y)
clf = svm.LinearSVC()
#clf = linear_model.LogisticRegression()
clf.C=1.0
print(clf)
clf.fit(t_x, t_y)
correct = 0
#prediction= clf.decision_function(v_x)

#print(hinge_loss(v_y,prediction))
print(clf.predict(t_x))
print(t_y)
""""""
for i,predict in enumerate(clf.predict(t_x)):

    if predict == t_y[i]:
        correct += 1
print (correct)
print (len(t_y))

filename = 'frame_model/'+lexicon+'_model.sav'
pickle.dump(clf, open(filename, 'wb'))
