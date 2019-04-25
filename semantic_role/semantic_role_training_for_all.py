from keras.layers import Dense, Embedding,Dropout
from keras.layers import LSTM, Bidirectional
from keras.layers.wrappers import TimeDistributed
from keras.layers import Merge
from keras.utils import np_utils
from keras.models import Sequential
from utl import Feature
import numpy as np
import os
import logging

logging.basicConfig(level=logging.INFO,filename ='../semantic_role_model/training.log', filemode='a')

from utl import Feature_Transformer

def transform_index_to_vector(lists, label_size):
    labelarray = np.zeros((len(lists), len(lists[0]), int(label_size + 1)), dtype=np.int)

    for i, data in enumerate(lists):
        tmp = np.array(np_utils.to_categorical(data, int(label_size + 1)))
        labelarray[i, :tmp.shape[0], :tmp.shape[1]] = tmp
    return labelarray

def get_max_label_size(lists):
    max_label = 0
    for _list in lists:
        if isinstance(_list, np.ndarray):
            for data in _list:
                if data > max_label:
                    max_label = data
        else:
            if _list > max_label:
                max_label = data
    return int(max_label)

def load_created_model_name(path):
    filenames = os.listdir(path)
    created_model_id=set()
    for filename in filenames:
        created_model_id.add(filename.split('.')[0])
    return created_model_id

training_path = '../semantic_role_model/training_data/'
label_path= '../semantic_role_model/label/'
training_filename= os.listdir(training_path)
ft = Feature_Transformer.Feature_Transformer()
total_acc = 0
total_sentence = 0
count = 0
created_model_id = load_created_model_name('../semantic_role_model/created_model_copy/')
#
for file_count,name in enumerate(training_filename):
#for file_count,name in enumerate(created_model_id):
    #name=name+'.npy'
    id = '4344'
    name=id+'.npy'

    print(name)
    #if name.split('.')[0] in created_model_id:
    #    continue
    training_data = np.load('../semantic_role_model/training_data/'+name)
    label = np.load('../semantic_role_model/label/'+name)
    training_word_vector = np.load('../semantic_role_model/semantic_vector/' + id + '_semantic_vector.npy')
    print(training_word_vector.shape)
    #break
    if len(training_data[0])<3:
        continue
    if len(training_data[0])<20:
        epochs = 30
    elif len(training_data[0])<50:
        epochs = 30
    else:
        epochs = 40
    count+=1
    max_label = get_max_label_size(label)
    vectors=[]
    text_vector = ft.nparray_from_float_to_int(training_data[0])
    dep_vector = ft.nparray_from_float_to_int(training_data[2])
    tag_vector = ft.nparray_from_float_to_int(training_data[4])
    parent_tag_vector = ft.nparray_from_float_to_int(training_data[5])
    vectors.append(text_vector)
    vectors.append(dep_vector)
    vectors.append(tag_vector)
    vectors.append(parent_tag_vector)
    vectors.append(training_word_vector)
    text_max_feature_size = get_max_label_size(text_vector)
    dep_max_feature_size = get_max_label_size(dep_vector)
    tag_max_feature_size = get_max_label_size(tag_vector)
    parent_tag_max_feature_size = get_max_label_size(parent_tag_vector)

    feature_size=[]
    feature_size.append(text_max_feature_size)
    #feature_size.append(pos_max_feature_size)
    feature_size.append(dep_max_feature_size)
    #feature_size.append(parent_pos_max_feature_size)

    feature_size.append(tag_max_feature_size)
    feature_size.append(parent_tag_max_feature_size)


    label_size = get_max_label_size(label)
    t_y = transform_index_to_vector(label,label_size)
    print(feature_size)
    for vector in vectors:
        print(vector.shape)

    models = []
    for i in range(0,4):
        models.append(Sequential())
        models[i].add(Embedding(int(feature_size[i]) + 1, 300, mask_zero=True))
    models.append(Sequential())
    models[4].add(TimeDistributed(Dense(300, activation='softmax'),input_shape=(None,300,)))

    merged=Merge(models,mode='concat')
    final_model = Sequential()
    final_model.add(merged)
    final_model.add(Dropout(0.2))
    final_model.add(Bidirectional(LSTM(256, return_sequences=True)))
    final_model.add(TimeDistributed(Dense(max_label+1, activation='softmax')))
    # final_model.add(Dense(27,activation='softmax'))
    final_model.compile(loss='categorical_crossentropy',
                        optimizer='adam',
                        metrics=['categorical_accuracy'])

    final_model.fit(vectors,t_y,batch_size=10,validation_split=0.05,epochs=epochs)
    #final_model.save('../semantic_role_model/created_model/'+name.split('.')[0]+'.mod')
    break
    #final_model.load_weights('test_model.mod')
    #score, acc = final_model.evaluate([text_vector,pos_vector,dep_vector, parent_pos_vector,tag_vector], t_y,batch_size=10)
    score, acc = final_model.evaluate([text_vector, dep_vector, tag_vector, parent_tag_vector, training_word_vector], t_y, batch_size=10)
    logging.info('-------------------------------------------------------------')
    logging.info('lu count:'+str(count))
    logging.info('cost:'+str(score))
    logging.info('acc:'+str(acc))
    total_acc+=acc
    total_sentence += len(training_data[0])

    logging.info('avg_acc:'+str(total_acc/count))
    logging.info('total_sentence_count:'+str(total_sentence))
    break