from utl import Feature_Extractor
import numpy as np
from utl import DB_Connector
db_connector= None

fe = Feature_Extractor.Feature_Extractor()
extract_functions = [fe.get_target_tag, fe.get_target_parent_head_tag, fe.get_target_child_dependency, fe.get_target_child_tag, fe.get_target_child_text]
function_len = len(extract_functions)
nlp = None
def get_frame_feature_lists(frameNet, lexicon_text, tokens):
    lus = frameNet.get_lu_candidate(tokens)
    target_lu = __find_target_lu(lus, lexicon_text)
    if target_lu is None:
        return None
    data_lists = []
    for function in extract_functions:
        data_lists.append(function(tokens, target_lu))

    return data_lists

def __find_target_lu(lus, lexicon_text):
    for lu in lus:
        if lu['lexicon']==lexicon_text:
            return lu
    return None

def get_latent_similarity(latent_vector_list,text_vector):
    similarity_list = []
    for latent_vector in latent_vector_list:
        similarity_list.append(nlp.get_cos_similarity(latent_vector,text_vector))
    return similarity_list

def get_latent_vector_lists(latent_lists, lexicon_text):
    latent_vector_list = []

    for latent_list in latent_lists:

        vector_list = []
        for latent in latent_list:
            if nlp.get_phrase_vector(latent[2]) is not None:
                vector_list.append(nlp.get_phrase_vector(latent[2]))
        latent_vector_list.append(nlp.get_avg_vector(vector_list))
    return latent_vector_list