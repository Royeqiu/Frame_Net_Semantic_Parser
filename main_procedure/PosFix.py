from semantic_frame import DB_Operation as dbo, Semantic_Frame_Model_Feature as sfmf
import DB_Connector
from NLP import NLP_Tool
from Frame_net import FrameNet_Data
import FrameNet_Loader
import Feature_Transformer_db as ftd

def get_latent_similarity(lexicon_text, text):
    rows = dbo.get_lexicon_unit_by_text(lexicon_text)
    latent_vector_list = []
    for row in rows:
        latent_vector =dbo.get_latent_vector(row[2])
        latent_vector_list.append(latent_vector)
    text_vector = nlp.get_phrase_vector(text)
    latent_similarity = sfmf.get_latent_similarity(latent_vector_list, text_vector)
    return latent_similarity

db_connector = DB_Connector.DB_Connector(user_name='postgres', db_name='semantic_parser', host='127.0.0.1',
                                         password='')
dbo.db_connector = db_connector

frameNet = FrameNet_Data.FrameNet(load_ori_frame=False, load_ori_lu=False)
lex_dic, frame_dic = FrameNet_Loader.get_lexicon_unit_and_semantic_frame_infos(db_connector)
frameNet.lex_dic = lex_dic
frameNet.frame_dic = frame_dic
nlp = NLP_Tool.NLP_Tool()
dbo.db_connector = db_connector
sfmf.nlp = nlp
def fix(lexicon_text):
    ids=dbo.get_lexicon_unit_by_text(lexicon_text)
    for id in ids:
        print(id)
        for sentence in dbo.get_semantic_frame_mode_sentence_by_id(id[1]):
            sentence_id = sentence[0]
            lu_id = sentence[1]
            semantic_frame_id = sentence[2]
            text = sentence[3]
            lexicon_text = dbo.get_lexicon_unit_name_by_id(lu_id)

            feature_lists = sfmf.get_frame_feature_lists(frameNet, lexicon_text, nlp.get_tokens(text))
            if feature_lists is None:
                continue
            child_text_features = feature_lists[len(feature_lists) - 1]
            child_vector_list = []
            for child_text in child_text_features:
                if nlp.get_phrase_vector(child_text) is not None:
                    child_vector_list.append(nlp.get_phrase_vector(child_text))
            child_text_avg_vec = nlp.get_avg_vector(child_vector_list).tolist()
            del (feature_lists[len(feature_lists) - 1])
            vector_list = []
            for i, feature_index_list in enumerate(dbo.get_feature_index_lists(lexicon_text, feature_lists)):
                vector_list.append(ftd.transform_to_vector(feature_index_list,
                                                           dbo.get_max_index_of_frame_model_fature
                                                           (lexicon_text, dbo.semantic_frame_feature_types[i])))
            vector_list.append(child_text_avg_vec)
            latent_similarity = get_latent_similarity(lexicon_text, text)
            vector_list.append(latent_similarity)
            feature_vector = ftd.concatenate(vector_list).tolist()
            label_index = dbo.get_label_index(lexicon_text, semantic_frame_id)
            dbo.add_semantic_frame_model_sentence_feature(sentence_id, feature_vector, label_index)
    print('fix finished')