from keras.layers import Dense, Embedding,Dropout
from keras.layers import LSTM, Bidirectional
from keras.layers.wrappers import TimeDistributed
from keras.layers import Merge
from keras.utils import np_utils
from keras.models import Sequential

import pickle
import DB_Connector
from semantic_frame import DB_Operation as dbo
from semantic_role.Semantic_Role_Training import Semantic_Role_Trainer as smt
import numpy as np
from NLP.NLP_Tool import NLP_Tool
def alignment_word_vector(word_vector_list,window_size):
    ori_len = len(word_vector_list)
    for i in range(ori_len,window_size):
        word_vector_list.append(np.zeros((300), dtype='f'))

def transform_index_to_vector(lists, label_size):
    labelarray = np.zeros((len(lists), len(lists[0]), int(label_size)), dtype=np.int)
    for i, data in enumerate(lists):
        tmp = np.array(np_utils.to_categorical(data, int(label_size)))
        labelarray[i, :tmp.shape[0], :tmp.shape[1]] = tmp
    return labelarray

def __prepare_input(rows, window_size):
    word_vector_list = []
    tag_list = []
    dep_list = []
    label_list = []
    for i, row in enumerate(rows):
        word_vector = []
        text = row[0]
        words = text.strip().split(' ')
        for word in words:
            vector = nlp.get_phrase_vector(word)
            if vector is not None:
                word_vector.append(vector)
            else:
                word_vector.append(np.zeros((300),dtype='f'))
        feature_vector = pickle.loads(row[1])
        tag_list.append(feature_vector[0])
        dep_list.append(feature_vector[1])
        label_vector = pickle.loads(row[2])
        alignment_word_vector(word_vector, window_size=window_size)
        word_vector_list.append(word_vector)
        label_list.append(label_vector)
    return [tag_list,dep_list,word_vector_list],label_list

db = DB_Connector.DB_Connector(user_name='postgres', db_name='semantic_parser', host='127.0.0.1', password='')
dbo.db_connector = db
nlp = NLP_Tool()
lu_id = 4344
rows = dbo.get_role_model_sentences(lu_id)
window_size = dbo.get_window_size(lu_id)
input_feature,output_feature = __prepare_input(rows,window_size)
input = []
for feature in input_feature:
    input.append(np.asarray(feature))

srt=smt()
models = []
label_size = dbo.get_role_label_max_index(lu_id)

output = transform_index_to_vector(output_feature, label_size + 2)
print(transform_index_to_vector(output_feature,label_size+2).shape)

output= np.asarray(output,dtype='f')
for i in range(0, len(input_feature)-1):
    models.append(Sequential())
    feature_size=dbo.get_role_feature_max_index(lu_id, dbo.semantic_role_feature_types[i])
    models[i].add(Embedding(feature_size + 2, 300, mask_zero=True))
models.append(Sequential())
models[len(models)-1].add(TimeDistributed(Dense(300, activation='softmax'),input_shape=(None,300,)))

merged = Merge(models, mode='concat')
final_model = Sequential()
final_model.add(merged)
final_model.add(Dropout(0.2))
final_model.add(Bidirectional(LSTM(256, return_sequences=True)))
final_model.add(TimeDistributed(Dense(label_size + 2, activation='softmax')))
final_model.compile(loss='categorical_crossentropy',
                         optimizer='adam',
                         metrics=['categorical_accuracy'])
batch_size= 40
validation_split = 0.1
epochs = 70

print(input[len(input)-1].shape)
final_model.fit(input, output, batch_size=batch_size, validation_split=validation_split, epochs=epochs)
