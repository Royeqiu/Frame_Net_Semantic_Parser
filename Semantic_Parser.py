from utl import Feature_Transformer,Feature,Feature_Extractor
from NLP import NLP_Tool
from Frame_net import FrameNet_Data,Doc_Annotation
from semantic_role import Semantic_Role_Training
from numpy import argmax
import DB_Connector
import pickle
import os
import FrameNet_Loader


class feature_type:
    frame_feature_types = ['text', 'child_pos', 'child_dep', 'parent_pos', 'target_pos','child_tag','target_tag']
    semantic_role_feature_tpyes = ['text', 'dep','tag','parent_tag']

def calculate_vector_similarity(latents):
    latent_list = [latent['lexicon'] for latent in latents['lu']]
    all_vectors = []
    for latent in latent_list:
        vector = nlp.get_phrase_vector(latent)
        if vector is not None:
            all_vectors.append(vector)
    return all_vectors

def get_label_index(lexicon,index):
    file = open ('model/'+lexicon+'/label_index.txt')
    label_dict=dict()
    for data in file:
        label_index = data.strip('\n').split('\t')
        label_dict[label_index[1]]=label_index[0]
    file.close()
    return label_dict[str(index)]

def load_semantic_role_label_size_dict(filename):
    semantic_role_label_size_dic=dict()
    file = open(filename,'r')
    for data in file:
        semantic_role_label_size_dic[int(data.strip('\n').split('\t')[0])]=int(data.strip('\n').split('\t')[1])
    return semantic_role_label_size_dic

def load_alignment_size_dict(filename):
    return load_semantic_role_label_size_dict(filename)

def get_semantic_frame_vector_list(ft,fe,lexicon,tokens,target_lu,frame_features):
    function_list = [lambda x:x, fe.get_target_child_pos, fe.get_target_child_dependency, fe.get_target_parent_head_tag, fe.get_target_pos, fe.get_target_child_tag, fe.get_target_tag]
    arguments = tokens,target_lu
    function_parameter = [[lexicon],arguments,arguments,arguments,arguments,arguments,arguments]
    vector_list = []
    for i,frame_feature in enumerate(frame_features):
        ft.set_feature(frame_feature)
        vector_list.append(ft.transform_to_vector([function_list[i](*function_parameter[i])]))

    return vector_list

def load_created_model_name(path):
    filenames = os.listdir(path)
    created_model_id=set()
    for filename in filenames:
        created_model_id.add(filename.split('.')[0])
    return created_model_id

def get_semantic_role_vector_list(lu_id,ft,fe,tokens,semantic_role_features,alignment_size):
    function_list = [fe.get_tokens_text,fe.get_tokens_dep,fe.get_tokens_tag,fe.get_tokens_parent_tag]
    semantic_role_vector=[]
    for i, semantic_role_feature in enumerate(semantic_role_features):
        ft.set_feature(semantic_role_feature)
        semantic_role_vector.append(ft.alignment([ft.transform_to_index(function_list[i](tokens))],alignment_size))
    return semantic_role_vector


created_model_id = load_created_model_name('../semantic_role_model/created_model/')
semantic_role_model= Semantic_Role_Training.Semantic_Role_Trainer()
nlp=NLP_Tool.NLP_Tool()
frameNet= FrameNet_Data.FrameNet( load_ori_frame=False, load_ori_lu=False)
db_connector = DB_Connector.DB_Connector(user_name='postgres', db_name='semantic_parser', host='127.0.0.1', password='')
lex_dic,frame_dic=FrameNet_Loader.get_lexicon_unit_and_semantic_frame_infos(db_connector)
frameNet.lex_dic=lex_dic
frameNet.frame_dic=frame_dic
ft=Feature_Transformer.Feature_Transformer()
fe=Feature_Extractor.Feature_Extractor()
semantic_role_label_size_dic=load_semantic_role_label_size_dict('../semantic_role_model/label_size.txt')
alignment_size = load_alignment_size_dict('../semantic_role_model/alignment_size.txt')
annotation = Doc_Annotation.Doc_Annotation('../data/fndata-1.6/lu/')

def get_result(text):
    lexicon_list = []
    lexicon_unit_id_list = []
    semantic_frame_result_list = []
    semantic_role_result_list = []

    tokens = nlp.get_tokens(text)
    lus = frameNet.get_lu_candidate(tokens)

    for lu in lus:
        lexicon = lu['lexicon']
        frames = frameNet.get_frame_name_by_lu(lexicon)
        no_annotation = False
        model_exist=os.path.exists('frame_model/'+lexicon+'_model.sav')

        if len(frames)==1:
            predict_index=0
            frame_index = 0
            semantic_role_id = int(frames[predict_index]['lu_id'])
        elif not model_exist:
            for i,frame in enumerate(frames):
                predict_index = -1
                if FrameNet_Loader.get_annotation_number_by_lu_id(db_connector,frame['lu_id'])!=0:
                    predict_index = i
                    frame_index = i
                    break
            if predict_index == -1:
                continue
            semantic_role_id = int(frames[predict_index]['lu_id'])
        else:
            frame_features=[]
            for i in range(0,len(feature_type.frame_feature_types)):
                frame_features.append(Feature.Feature())
            for i, feature in enumerate(feature_type.frame_feature_types):
                frame_features[i].load_feature('model/' + lexicon + '/'+feature+'_feature_index.txt')

            vector_list = get_semantic_frame_vector_list(ft,fe,lexicon,tokens,lu,frame_features)
            lu_vector = nlp.get_phrase_vector(lu['lexicon'])
            lu_similarity = []
            for frame in frames:
                latents = frameNet.get_latent_by_frameName(frame['frame_name'])
                all_vectors = calculate_vector_similarity(latents)
                lu_similarity.append(nlp.get_cos_similarity(lu_vector, list (nlp.get_avg_vector(all_vectors))))
            vector_list.append([ft.to_nparray(lu_similarity)])
            training_data = ft.concatenate(vector_list)
            model_file = open('frame_model/'+lexicon+'_model.sav', 'rb')
            clf = pickle.load(model_file)
            model_file.close()
            predict_index=int(clf.predict(training_data)[0])
            semantic_role_id = int(get_label_index(lexicon, predict_index))
            for index,frame in enumerate(frames):
                if int(frame['lu_id'])==semantic_role_id:
                    frame_index = index
                    break
        lexicon_list.append(lu['lexicon'])
        if FrameNet_Loader.get_annotation_number_by_lu_id(db_connector,semantic_role_id) ==0 :
            no_annotation = True
        semantic_frame_result_list.append(frames[frame_index]['frame_name'])
        lexicon_unit_id_list.append(frames[frame_index]['lu_id'])
        if no_annotation:
            st=''
            for word_count in range(0,len(text.split(' '))):
                if word_count >= lu['low_index'] and word_count<lu['high_index']+1:
                    st+='Target\t'
                else:
                    st+='0\t'
        else:
            semantic_role_features = []
            for i in range(0, len(feature_type.semantic_role_feature_tpyes)):
                semantic_role_features.append(Feature.Feature())
            for i, feature in enumerate(feature_type.semantic_role_feature_tpyes):
                semantic_role_features[i].load_feature('../semantic_role_model/training_data_feature/' + str(semantic_role_id) + '/' + feature + '_feature_index.txt')
            label_feature = Feature.Feature()
            label_feature.load_feature('../semantic_role_model/feature/' + str(semantic_role_id))
            semantic_role_model.set_semantic_features(semantic_role_features)
            semantic_role_model.set_label_feature(label_feature)
            semantic_role_model.construct_model()
            if str(semantic_role_id) not in created_model_id:
                semantic_role_model.load_training_data(str(semantic_role_id))
                semantic_role_model.fit(str(semantic_role_id))
                semantic_role_model.save_model('../semantic_role_model/created_model/' + str(semantic_role_id) + '.mod')
                created_model_id.add(str(semantic_role_id))
            predicted_semantic_role_vector = get_semantic_role_vector_list(str(semantic_role_id), ft, fe, tokens, semantic_role_features, alignment_size[semantic_role_id])
            predicted_word_vector=[]
            predicted_word_vector.append(fe.get_tokens_semantic_vector(tokens, nlp))
            predicted_word_vector=ft.alignment_2d(predicted_word_vector, alignment_size[semantic_role_id])
            predicted_word_vector=ft.to_nparray(predicted_word_vector)
            semantic_role_model.load_model_weight('../semantic_role_model/created_model/'+str(semantic_role_id)+'.mod')
            res=semantic_role_model.predict([predicted_semantic_role_vector[0], predicted_semantic_role_vector[1], predicted_semantic_role_vector[2], predicted_semantic_role_vector[3], predicted_word_vector])
            print(res.shape)
            ft.set_feature(label_feature)
            for single_res in res:
                st = ''
                for i,re in enumerate(single_res):
                    result = argmax(re)
                    if result == 0:
                        result = 0
                    else:
                        result = ft.transform_from_index_to_label(result)
                        if i >= lu['low_index'] and i < lu['high_index'] + 1:
                            result = 'Target'
                        elif result == 'Target':
                            result = frames[frame_index]['frame_name']
                    st += str(result) + '\t'
                    if i+1 == len(text.split(' ')):
                        break
        semantic_role_result_list.append(st)

    return lexicon_list,lexicon_unit_id_list,semantic_frame_result_list,semantic_role_result_list