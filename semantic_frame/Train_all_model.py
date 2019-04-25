from os import listdir
from utl import Feature_Transformer
import numpy as np
from sklearn import linear_model
import pickle

def is_label_invaild(labels):
    check_set = set()
    for label in labels:
        check_set.add(label)
    if len(check_set) <=1:
        return True
    else:
        return False
count = 0
no_annotation = 0
only_one_annotation = 0
file_name = listdir('data/ML_data/')
lexicon_set = set()
worst_case_prob = 1.0
worst_case_lu = '@@'
total_prob = 0.0
sentence_count = 0
for file in file_name:
    names = file.split('_')
    lexicon_set.add(names[0])

ft = Feature_Transformer.Feature_Transformer()
for file_count,lexicon in enumerate(lexicon_set):
    if file_count% 100 == 0:
        print(str(file_count)+'s lu have been processed!')
    print(lexicon,end='\t')

    training_data = np.load('data/ML_data/'+lexicon+'_training_data.npy')
    label = np.load('data/ML_data/'+lexicon+'_training_label.npy')
    if len(training_data)==0:
        no_annotation += 1
        continue
    if is_label_invaild(label):
        only_one_annotation += 1
        continue
    count += 1
    sentence_count += len(training_data)
    t_x, v_x, index = ft.data_separation(training_data, 0.7)
    t_y = []
    v_y = []
    for i in range(0, len(label)):
        if i in index:
            t_y.append(label[i])
        else:
            v_y.append(label[i])
    t_y = ft.to_nparray(t_y)
    v_y = ft.to_nparray(v_y)
    clf = linear_model.LogisticRegression()
    clf.fit(t_x, t_y)
    filename = 'frame_model/'+lexicon+'_model.sav'
    pickle.dump(clf, open(filename, 'wb'))
    correct = 0
    for i, predict in enumerate(clf.predict(t_x)):
        if predict == t_y[i]:
            correct += 1
    prob = float(correct/len(t_y))
    if prob < worst_case_prob:
        worst_case_prob = prob
        worst_case_lu = lexicon
    total_prob += prob
    print(prob)
total_number = only_one_annotation+no_annotation+count
print ('total number of lu:')
print (count)
print ('the overall performance:')
print (float(total_prob/count))
print (worst_case_lu)
print (worst_case_prob)
print (sentence_count)