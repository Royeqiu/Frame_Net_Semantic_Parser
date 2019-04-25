import psycopg2
import numpy as np
import pickle
from sklearn import linear_model
import DB_Connector
from semantic_frame import DB_Operation
import random
from main_procedure import PosFix as pos
from utl import Injection_sql

db = DB_Connector.DB_Connector(user_name='postgres', db_name='semantic_parser', host='127.0.0.1', password='')
DB_Operation.db_connector = db
def concat_lexicon_input(lexicon_inputs):
    input_vector=[]
    for lexicon_input in lexicon_inputs:
        for vector in lexicon_input:
            input_vector.append(vector)
    return input_vector

def data_separation(data, percent):
    size = len(data)
    pool = []
    for i in range(0, size):
        pool.append(i)
    data_size = int(size * percent)
    index = random.sample(pool, data_size)
    training = []
    validation = []
    for i in range(0, size):
        if i in index:
            training.append(data[i])
        else:
            validation.append(data[i])

    return np.array(training, dtype=np.float32), np.array(validation, dtype=np.float32), index


def __get_lu_training_data(lu_id):
    input_list,output_list = DB_Operation.get_semantic_frame_training_data(lu_id)
    return input_list,output_list

def __get_training_data(lexicon_text):
    rows= DB_Operation.get_lexicon_unit_by_text(lexicon_text)
    input_training_data_list = []
    output_training_data_list = []
    for row in rows:
        input_list,output_list=__get_lu_training_data(row[1])
        input_training_data_list.append(input_list)
        output_training_data_list.append(output_list)
    return input_training_data_list,output_training_data_list

def __vaildate_leng(list):
    default_len = len(list[0])
    for vector in list:
        if default_len != len(vector):
            print(default_len)
            print(len(vector))

            return False

    return True
lexicon_text_set =set()
lus = DB_Operation.get_lu_ids()

for lu_id in lus:
    lexicon_text_set.add(DB_Operation.get_lexicon_unit_name_by_id(lu_id))

for lexicon_text in lexicon_text_set:

    print(lexicon_text)
    vaild_classification = DB_Operation.get_frame_label_max_index(lexicon_text)
    if vaild_classification < 2:
        continue
    lexicon_training_input, lexicon_training_output = __get_training_data(lexicon_text)
    training_input_list = concat_lexicon_input(lexicon_training_input)
    training_output_list = concat_lexicon_input(lexicon_training_output)
    if len(training_input_list) < 5:
        continue
    input_np_array = np.array(training_input_list)
    output_np_array = np.array(training_output_list)

    clf = linear_model.LogisticRegression()
    vaild_leng = False
    while(not vaild_leng):

        try:
            clf.fit(input_np_array,output_np_array)
            vaild_leng = True
        except ValueError:
            pos.fix(lexicon_text)
            lexicon_training_input, lexicon_training_output = __get_training_data(lexicon_text)
            training_input_list = concat_lexicon_input(lexicon_training_input)
            training_output_list = concat_lexicon_input(lexicon_training_output)
            input_np_array = np.array(training_input_list)
            output_np_array = np.array(training_output_list)
            __vaildate_leng(input_np_array)
    binary_model = pickle.dumps(clf,-1)
    correct = 0
    for i, predict in enumerate(clf.predict(input_np_array)):
        if predict == output_np_array[i]:
            correct += 1
    prob = float(correct / len(output_np_array))
    sql = Injection_sql.get_inject_semantic_frame_model_sql(lexicon_text,psycopg2.Binary(binary_model),prob,len(input_np_array))
    db.execute_insert(sql)
