from keras.layers import Dense, Embedding,Dropout
from keras.layers import LSTM, Bidirectional
from keras.layers.wrappers import TimeDistributed
from keras.layers import Merge,Concatenate
from keras.utils import np_utils
from keras.models import Sequential

import numpy as np
from utl import Feature_Transformer
class Semantic_Role_Trainer:

    def __init__(self):
        self.features_size = None
        self.semantic_features = None
        self.vectors = []
        self.training_data = None
        self.label = None
        self.label_feature = None
        self.label_size = None
        self.ft = Feature_Transformer.Feature_Transformer()
        self.final_model=None

    def set_semantic_features(self, semantic_features):
        self.semantic_features = semantic_features
        self.set_feature_sizes(semantic_features)

    def set_label_feature(self,label_feature):
        self.label_feature = label_feature
        self.label_size = label_feature.size

    def set_training_data(self,filename):
        self.training_data = np.load(filename)

    def set_label(self,filename):
        self.label = np.load(filename)


    def set_feature_sizes(self, semantic_features):
        self.features_size=[]
        for feature in semantic_features:
            self.features_size.append(feature.size)

    def transform_index_to_vector(self,lists, label_size):
        labelarray = np.zeros((len(lists), len(lists[0]), int(label_size + 1)), dtype=np.int)

        for i, data in enumerate(lists):
            tmp = np.array(np_utils.to_categorical(data, int(label_size + 1)))
            labelarray[i, :tmp.shape[0], :tmp.shape[1]] = tmp
        return labelarray

    def construct_model(self):
        models = []
        for i in range(0, len(self.features_size)):
            models.append(Sequential())
            models[i].add(Embedding(self.features_size[i] + 1, 300, mask_zero=True))
        models.append(Sequential())
        models[len(self.features_size)].add(TimeDistributed(Dense(300, activation='softmax'),input_shape=(None,300,)))
        merged = Concatenate(models, mode='concat')
        self.final_model = Sequential()
        self.final_model.add(merged)
        self.final_model.add(Dropout(0.2))
        self.final_model.add(Bidirectional(LSTM(256, return_sequences=True)))
        self.final_model.add(TimeDistributed(Dense(self.label_size+1 , activation='softmax')))
        self.final_model.compile(loss='categorical_crossentropy',
                            optimizer='adam',
                            metrics=['categorical_accuracy'])

    def load_model_weight(self,model_name):
        self.final_model.load_weights(model_name)

    def load_training_data(self,lu_id):
        training_data = np.load('../semantic_role_model/training_data/' + lu_id+'.npy')
        label = np.load('../semantic_role_model/label/' + lu_id+'.npy')
        training_word_vector = np.load('../semantic_role_model/semantic_vector/' + lu_id + '_semantic_vector.npy')
        self.vectors = []
        text_vector = self.ft.nparray_from_float_to_int(training_data[0])
        dep_vector = self.ft.nparray_from_float_to_int(training_data[2])
        tag_vector = self.ft.nparray_from_float_to_int(training_data[4])
        parent_tag_vector = self.ft.nparray_from_float_to_int(training_data[5])
        self.vectors.append(text_vector)
        self.vectors.append(dep_vector)
        self.vectors.append(tag_vector)
        self.vectors.append(parent_tag_vector)
        self.vectors.append(training_word_vector)
        self.label = self.transform_index_to_vector(label,self.label_size)

    def save_model(self, filename):
        self.final_model.save(filename)

    def evaluate(self,datas,label):
        score, acc = self.final_model.evaluate(datas, label, batch_size=10)
        return score,acc

    def predict(self,datas):
        return self.final_model.predict(datas)

    def fit(self,lu_id,batch_size=10,validation_split=0.05,epochs = 30):

        self.final_model.fit(self.vectors, self.label, batch_size=batch_size, validation_split=validation_split, epochs=epochs)


    def transform_index_to_vector(self,lists, label_size):
        labelarray = np.zeros((len(lists), len(lists[0]), int(label_size + 1)), dtype=np.int)

        for i, data in enumerate(lists):
            tmp = np.array(np_utils.to_categorical(data, int(label_size + 1)))
            labelarray[i, :tmp.shape[0], :tmp.shape[1]] = tmp
        return labelarray
""" 
def transform_index_to_vector(lists, label_size):
    labelarray = np.zeros((len(lists), len(lists[0]), int(label_size + 1)), dtype=np.int)

    for i, data in enumerate(lists):
        tmp = np.array(np_utils.to_categorical(data, int(label_size + 1)))
        labelarray[i, :tmp.shape[0], :tmp.shape[1]] = tmp
    return labelarray

def get_max_label_size(self,lists):
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
"""
"""
ft = Feature_Transformer.Feature_Transformer()

training_data = np.load('semantic_role_model/training_data/10.npy')
label = np.load('semantic_role_model/label/10.npy')
max_label = get_max_label_size(label)
vectors=[]
text_vector = ft.nparray_from_float_to_int(training_data[0])
pos_vector = ft.nparray_from_float_to_int(training_data[1])
dep_vector = ft.nparray_from_float_to_int(training_data[2])
parent_pos_vector = ft.nparray_from_float_to_int(training_data[3])
vectors.append(text_vector)
vectors.append(pos_vector)
vectors.append(dep_vector)
vectors.append(parent_pos_vector)
text_max_feature_size = get_max_label_size(text_vector)
pos_max_feature_size = get_max_label_size(pos_vector)
dep_max_feature_size = get_max_label_size(dep_vector)
parent_pos_max_feature_size = get_max_label_size(parent_pos_vector) + 1
feature_size=[]
feature_size.append(text_max_feature_size)
feature_size.append(pos_max_feature_size)
feature_size.append(dep_max_feature_size)
feature_size.append(parent_pos_max_feature_size)

label_size = get_max_label_size(label)
t_y = transform_index_to_vector(label,label_size)

models = []
for i in range(0,4):
    models.append(Sequential())
    models[i].add(Embedding(int(feature_size[i]) + 1, 256, mask_zero=True))


merged=Merge(models,mode='concat')
final_model = Sequential()
final_model.add(merged)
final_model.add(Dropout(0.2))
final_model.add(LSTM(256, return_sequences=True))
final_model.add(TimeDistributed(Dense(max_label+1, activation='softmax')))
# final_model.add(Dense(27,activation='softmax'))
final_model.compile(loss='categorical_crossentropy',
                    optimizer='adam',
                    metrics=['categorical_accuracy'])
final_model.fit(vectors,t_y,batch_size=10,validation_split=0.1,epochs=100)
final_model.save('test_model.mod')

final_model.load_weights('test_model.mod')
score, acc = final_model.evaluate([text_vector,pos_vector,dep_vector, parent_pos_vector], t_y,batch_size=10)
test_text = [[176, 322, 335, 326, 142, 312, 361, 302, 356, 81]]

test_pos = [[5, 10, 5, 12, 7, 3, 11, 12, 11, 6]]
test_dep = [[33, 16, 4, 35, 3, 24, 27, 35, 27, 22]]
test_parent_pos =[[11, 8, 11, 10, 6, 3, 9, 10, 9, 4]]

test_text=ft.alignment_size.txt(test_text,37)
test_pos = ft.alignment_size.txt(test_pos,37)
test_dep = ft.alignment_size.txt(test_dep,37)
test_parent_pos = ft.alignment_size.txt(test_parent_pos,37)
print(test_text.shape)
print(test_pos.shape)
print('Test score:', score)
print('Test accuracy:', acc)
res=final_model.predict([test_text,test_pos,test_dep,test_parent_pos])
"""
