import Feature_Extractor
from semantic_frame import DB_Operation as dbo
from Frame_net import Annotation_Info,Annotation_Label
from semantic_role import Semantic_Role_Model_Feature as srmf
from NLP import NLP_Tool
from utl import DB_Connector
import numpy as np
import pickle
import psycopg2

def __contains_label(labels):
    if len(labels)==0:
        return False
    else:
        return True

def __load_annotation_data(lu_id):
    annotation_datas = dbo.get_annotation_datas(lu_id)
    annotation_info_list = []
    for row in annotation_datas:
        id = row[0]
        text,right_space = __remove_duplicate_space(row[1])
        if right_space:
            right_space_offset =1
        else:
            right_space_offset = 0
        annotation_info = Annotation_Info.Annotation_Info_DB(id=id, lu_id=lu_id, text=text)
        annotation_label_rows = dbo.get_annotation_label(id)
        if __contains_label(annotation_label_rows):
            for annotation_label_row in annotation_label_rows:
                start_offset = annotation_label_row[2] - right_space_offset
                end_offset = annotation_label_row[3] - right_space_offset
                semantic_role = annotation_label_row[4]
                annotation_info.add_annotation_label(
                    Annotation_Label.Annotation_Label(text_id=id, start_offset=start_offset, end_offset=end_offset,
                                                      semantic_role=semantic_role))
            annotation_info_list.append(annotation_info)

    return annotation_info_list

def __extract_feature(lu_id,annotation):
    tokens=nlp.get_tokens(annotation.text.strip())
    feature_lists = srmf.get_frame_feature_lists(tokens)
    dbo.add_feature_dictionary(feature_lists)
    dbo.add_semantic_role_model_feature(feature_lists,lu_id)
    feature_vector = []
    for i,feature_list in enumerate(feature_lists):
        feature_vector.append(__alignment(lu_id,dbo.get_role_feature_index(feature_list=feature_list,lu_id=lu_id,type=dbo.semantic_role_feature_types[i])))
    return feature_vector

def __alignment(lu_id,vector):
    window_size = dbo.get_window_size(lu_id)
    text_leng = len(vector)
    for i in range(text_leng,window_size):
        vector.append(0)
    return vector
def __add_window_size(lu_id):
    annotaion_list = __load_annotation_data(lu_id)
    window_size = 0
    dbo.add_role_model_lu_id(lu_id)
    for annotation in annotaion_list:
        text = annotation.get_text().strip()
        tokens = nlp.get_tokens(text)
        if len(tokens) > window_size:
            window_size = len(tokens)
    dbo.add_role_model_window_size(lu_id, window_size)

def __remove_duplicate_space(text):
    right_space = False
    if text[0]==' ':
        right_space = True
    copied_text = text.strip()
    while '  ' in copied_text:
        copied_text = copied_text.replace('  ',' ')
    return copied_text,right_space

def __is_vaild_offset(label, text):
    label_part_text = text[label.start_offset:label.end_offset]
    if label_part_text =='':
        return False
    elif label.semantic_role=='':
        return False
    else:
        return True

def __extract_label_vector(lu_id,annotation):
    text=annotation.text.strip()
    tokens = nlp.get_tokens(text)
    labels = annotation.get_annotation_labels()
    text_len = len(tokens)
    label_array = np.ones(window_size, np.int8)
    for label in labels:
        if __is_vaild_offset(label, text):
            dbo.add_feature_dictionary([label.semantic_role])
            dbo.add_semantic_role_model_label([label.semantic_role], lu_id)
            label_part_text = text[label.start_offset:label.end_offset + 1]
            label_tokens = nlp.get_tokens(label_part_text)
            equal_count = 0
            tmp = -1
            found_index = False
            for i, token in enumerate(tokens):
                if equal_count == len(label_tokens):
                    found_index = True
                    break
                if token.text == label_tokens[equal_count].text:
                    if equal_count == 0:
                        tmp = i
                    equal_count += 1
                else:
                    equal_count = 0
            if found_index:
                for i in range(0, window_size):
                    if tmp <= i and i < tmp + len(label_tokens):
                        feature_index = dbo.get_role_feature_index(label.semantic_role, lu_id, 'label')[0]
                        label_array[i] = feature_index
                    elif i >= text_len:
                        label_array[i] = 0
    return label_array

fe = Feature_Extractor.Feature_Extractor()
nlp = NLP_Tool.NLP_Tool()
nlp.set_tokenizer(NLP_Tool.WhitespaceTokenizer,nlp.nlp.vocab)
db_connector = DB_Connector.DB_Connector(user_name='postgres', db_name='semantic_parser', host='127.0.0.1',password='')
dbo.db_connector = db_connector
#sentence='give me a cup of tea?'
lu_id_list = dbo.get_lu_ids()
log_file=open('log.txt','w')
loaded_lu_id = [int(x.strip()) for x in open('loaded_lu_id.txt', 'r')]
for i,lu_id in enumerate(lu_id_list):
    if i%100 ==0:
        print('%s lu_id have been processed' %i)
    if lu_id in loaded_lu_id:
        continue
    annotaion_list = __load_annotation_data(lu_id)
    window_size= dbo.get_window_size(lu_id)
    if window_size==0:
        continue
    for annotation in annotaion_list:
        if annotation.text =='':
            continue
        try:
            feature_list = __extract_feature(lu_id,annotation)
            label_vector = __extract_label_vector(lu_id,annotation)
            dbo.add_role_model_sentences(lu_id=lu_id,text=annotation.text.strip().replace('\'','\'\''),feature_vector=psycopg2.Binary(pickle.dumps(feature_list,-1)),label_vector=psycopg2.Binary(pickle.dumps(label_vector,-1)))
        except:
            log_file.write(str(lu_id)+'\t')
            log_file.write(str(annotation.id)+'\t')
