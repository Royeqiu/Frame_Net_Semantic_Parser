import Feature
from NLP import NLP_Tool
from Frame_net import FrameNet_Data,Doc_Annotation
import Feature_Extractor
import Feature_Transformer
import os
trained_model=os.listdir('copy/')
print(trained_model)
def calculate_vector_similarity(latents):
    latent_list = [latent['lexicon'] for latent in latents['lu']]
    all_vectors = []

    for latent in latent_list:
        vector = nlp.get_phrase_vector(latent)
        if vector is not None:
            all_vectors.append(vector)

    return all_vectors

def save_all_feature(lexicon, features):
    for i,_list in enumerate(features):
        if i == 0:
            features[i].save_feature('text','model/'+lexicon+'/')
        if i == 1:
            features[i].save_feature('child_pos','model/'+lexicon+'/')
        if i == 2:
            features[i].save_feature('child_dep','model/'+lexicon+'/')
        if i == 3:
            features[i].save_feature('parent_pos','model/'+lexicon+'/')
        if i == 4:
            features[i].save_feature('target_pos','model/'+lexicon+'/')
        if i == 5:
            features[i].save_feature('child_tag','model/'+lexicon+'/')
        if i == 6:
            features[i].save_feature('target_tag', 'model/' + lexicon + '/')
def save_label(lexicon,label_dict):
    file=open('model/'+lexicon+'/label_index.txt','w')
    for key in label_dict.keys():
        file.write(str(key)+'\t'+str(label_dict[key])+'\n')

nlp = NLP_Tool.NLP_Tool()
fe = Feature_Extractor.Feature_Extractor()
frameNet= FrameNet_Data.FrameNet( load_ori_frame=False, load_ori_lu=False)
frameNet.load_lu('data/lu.txt')
frameNet.load_frame('data/frame.txt')
annotation = Doc_Annotation.Doc_Annotation()
annotation.load_annotation()
ft = Feature_Transformer.Feature_Transformer()
count = 0

for lexicon_count,key in enumerate(frameNet.lex_dic.keys()):
    key = 'give'
    lexicon = key
    text_list = []
    child_pos_list = []
    child_dep_list = []
    child_text_list = []
    parent_pos = []
    current_pos = []
    current_tag = []
    child_tag_list = []
    all_similarity = []
    label = []
    label_dict=dict()
    label_count = 0
    if len(frameNet.lex_dic[key])==1:
        continue
    for lu in frameNet.lex_dic[key]:
        annotation_id = lu['lu_id']
        if len(annotation.lu_annotation[annotation_id]['annotation']) == 0:
            continue

        for annotation_text in annotation.lu_annotation[annotation_id]['annotation']:
            text = annotation_text['text']
            tokens = nlp.get_tokens(text)
            lus = frameNet.get_lu_candidate(tokens)
            lu_similarity = []
            for target_lu in lus:
                if target_lu['lexicon'] == key:
                    print('lu:',end='\t')
                    print(target_lu)
                    text_list.append(lexicon)
                    current_pos.append(fe.get_target_pos(tokens,target_lu))
                    parent_pos.append(fe.get_target_parent_head_tag(tokens, target_lu))
                    child_dep_list.append(fe.get_target_child_dependency(tokens, target_lu))
                    child_pos_list.append(fe.get_target_child_pos(tokens, target_lu))
                    child_text_list.append(fe.get_target_child_text(tokens, target_lu))
                    child_tag_list.append(fe.get_target_child_tag(tokens,target_lu))
                    current_tag.append(fe.get_target_tag(tokens,target_lu))
                    all_frame = frameNet.get_frame_name_by_lu(target_lu['lexicon'])
                    if len(lu_similarity) == 0:
                        for frame in all_frame:
                            latents = frameNet.get_latent_by_frameName(frame['frame_name'])
                            lu_vector = nlp.get_phrase_vector(target_lu['lexicon'])
                            all_vectors = calculate_vector_similarity(latents)
                            if lu_vector is not None:
                                lu_similarity.append(nlp.get_cos_similarity(lu_vector, list(nlp.get_avg_vector(all_vectors))))
                            else:
                                lu_similarity.append(0.0)
                    all_similarity.append(lu_similarity)
                    print(lu_similarity)
                    label.append(label_count)
        label_dict[annotation_id]=label_count
        label_count += 1
    features = []
    data_list = []
    data_list.append(text_list)
    data_list.append(child_pos_list)
    data_list.append(child_dep_list)
    data_list.append(parent_pos)
    data_list.append(current_pos)
    data_list.append(child_tag_list)
    data_list.append(current_tag)
    for i in range(0,7):
        features.append(Feature.Feature())
        features[i].load_data(data_list[i])
    save_label(lexicon,label_dict)
    save_all_feature(lexicon,features)
    vector_list = []
    for i in range(0,7):
        ft.set_feature(features[i])
        vector_list.append(ft.transform_to_vector(data_list[i]))
    vector_list.append(ft.to_nparray(all_similarity))
    label = ft.to_nparray(label)
    training_data = ft.concatenate(vector_list)


    ft.save_np('data/ML_data/'+lexicon+'_training_data', training_data)
    ft.save_np('data/ML_data/'+lexicon+'_training_label', label)
    break