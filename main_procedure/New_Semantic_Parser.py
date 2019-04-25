from semantic_frame import DB_Operation as dbo, Semantic_Frame_Model_Feature as sfmf
import DB_Connector
from NLP import NLP_Tool
from Frame_net import FrameNet_Data, FrameNet_Loader
import Feature_Transformer_db as ftd
import pickle
from main_procedure import Semantic_Parser_Consist_Field as cf
from utl import Query_sql

db_connector= DB_Connector.DB_Connector(user_name='postgres', db_name='semantic_parser', host='127.0.0.1', password='')
lex_dic, frame_dic = FrameNet_Loader.get_lexicon_unit_and_semantic_frame_infos(db_connector)
frameNet = FrameNet_Data.FrameNet(load_ori_frame=False, load_ori_lu=False)
frameNet.lex_dic = lex_dic
frameNet.frame_dic = frame_dic
dbo.db_connector = db_connector
nlp = NLP_Tool.NLP_Tool()
sfmf.nlp = nlp

def __get_lu_candidate(tokens):
    lus = frameNet.get_lu_candidate(tokens)
    return lus

def __turn_features_to_vec(lexicon_text,feature_lists):
    vector_list = []
    for i, feature_index_list in enumerate(dbo.get_feature_index_lists(lexicon_text, feature_lists)):
        vector_list.append(ftd.transform_to_vector(feature_index_list,
                                                   dbo.get_max_index_of_frame_model_fature
                                                   (lexicon_text, dbo.semantic_frame_feature_types[i])))
    return vector_list

def __get_child_vector(feature_lists):
    child_text_features = feature_lists[len(feature_lists) - 1]
    child_vector_list = []
    for child_text in child_text_features:
        if nlp.get_phrase_vector(child_text) is not None:
            child_vector_list.append(nlp.get_phrase_vector(child_text))
    child_text_avg_vec = nlp.get_avg_vector(child_vector_list).tolist()
    del (feature_lists[len(feature_lists) - 1])
    return child_text_avg_vec

def __get_semantic_frame_model_label_index(lexicon_text):
    rows = db_connector.execute(Query_sql.get_semantic_frame_model_label_index(lexicon_text))
    return [row[0] for row in rows]

def __is_contains_model(lexicon_text):
    rows = db_connector.execute(Query_sql.is_contains_semantic_frame_model(lexicon_text))
    if rows[0][0] ==0:
        return False
    else:
        return True
def __is_contains_label_index(lexicon_text):
    rows = Query_sql.is_contains_semantic_frame_model_label(lexicon_text)
    db_connector.execute(rows)
    if rows[0][0] == 0:
        return False
    else:
        return True
def __load_semantic_model(lexicon_text):

    sql = Query_sql.get_semantic_frame_model(lexicon_text)
    rows = db_connector.execute(sql)
    model = pickle.loads(rows[0][0])
    return model

def get_latent_similarity(lexicon_text, text):
    rows = dbo.get_lexicon_unit_by_text(lexicon_text)
    latent_vector_list = []
    for row in rows:
        latent_vector_list.append(dbo.get_latent_vector(row[2]))
    text_vector = nlp.get_phrase_vector(text)
    latent_similarity = sfmf.get_latent_similarity(latent_vector_list, text_vector)
    return latent_similarity

def predict_semantic_frame(lu,tokens,sentence):
    lexicon_text = lu[cf.LEXICON_TEXT].replace('\'', '\'\'')
    print('The lexicon text is :%s' %lexicon_text)
    feature_lists = sfmf.get_frame_feature_lists(frameNet, lexicon_text, tokens)
    child_text_avg_vec = __get_child_vector(feature_lists)
    vector_list = __turn_features_to_vec(lexicon_text, feature_lists)
    vector_list.append(child_text_avg_vec)
    latent_similarity = get_latent_similarity(lexicon_text, sentence)
    vector_list.append(latent_similarity)
    feature_vector = ftd.concatenate(vector_list)
    if __is_contains_model(lexicon_text):
        model = __load_semantic_model(lexicon_text)
        index = model.predict([feature_vector])
    elif __is_contains_label_index(lexicon_text):
        #print('case2')
        index = __get_semantic_frame_model_label_index(lexicon_text)
    else:
        print('this lu totally doesn\'t have record.')
        return None
    return index

def __predict_semantic_frame(lexicon_text, semantic_frame_index):
    sql = 'select fd.text from semantic_frame_model_feature as sfmf, feature_dictionary as fd where sfmf.lexicon_text=\'%s\' and sfmf.index = %s and sfmf.type=\'label\' and fd.id = sfmf.feature_dic_id' %(lexicon_text,semantic_frame_index)
    rows = db_connector.execute(sql)
    return rows[0][0]

def parse(sentence):
    tokens = nlp.get_tokens(sentence)
    lus = __get_lu_candidate(tokens)
    for lu in lus:
        lexicon_text=lu[cf.LEXICON_TEXT]
        semantic_frame_indexs= predict_semantic_frame(lu,tokens,sentence)
        for semantic_frame_index in semantic_frame_indexs:
            semantic_frame_id =__predict_semantic_frame(lexicon_text, semantic_frame_index)
            semantic_frame_name = dbo.get_semantic_frame(semantic_frame_id)[0][2]
            print('The semantic meaning is :%s' %semantic_frame_name)
            lu_id = dbo.get_lexicon_unit_id(lexicon_text,semantic_frame_name)[0][0]
            print(lu_id)

parse('boxed up your stuff')