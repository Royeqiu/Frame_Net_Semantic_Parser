import Feature
from NLP import NLP_Tool
from Frame_net import Doc_Annotation
import Feature_Extractor
import Feature_Transformer
import numpy as np
from spacy.tokens import Doc

class WhitespaceTokenizer(object):
    def __init__(self, vocab):
        self.vocab = vocab

    def __call__(self, text):
        words = text.split(' ')
        # All tokens 'own' a subsequent space character in this tokenizer
        spaces = [True] * len(words)
        return Doc(self.vocab, words=words, spaces=spaces)

fe = Feature_Extractor.Feature_Extractor()
ft = Feature_Transformer.Feature_Transformer()
feature_list=[]
for i in range(0,6):
    feature_list.append(Feature.Feature())
nlp = NLP_Tool.NLP_Tool()
nlp.nlp.tokenizer = WhitespaceTokenizer(nlp.nlp.vocab)

annotation = Doc_Annotation.Doc_Annotation()
annotation.load_annotation()


for i,key in enumerate(annotation.lu_annotation.keys()):
    print(key)
    key='4344'

    data_list = []
    text_list = []
    pos_list = []
    tag_list = []
    dep_list = []
    parent_pos_list = []
    parent_tag_list = []
    semantic_vector = []
    data_list.append(text_list)
    data_list.append(pos_list)
    data_list.append(dep_list)
    data_list.append(parent_pos_list)
    data_list.append(tag_list)
    data_list.append(parent_tag_list)
    data_list.append(semantic_vector)
    annotation_set = annotation.lu_annotation[key]['annotation']
    if i%50:
        print(str(i)+'s lu has been processed.')
    if len(annotation_set)==0:
        continue
    i=0
    print(len(annotation_set))
    for single_annotation in annotation_set:
        i+=1
        text = single_annotation['text'].strip(' ').lower()
        while '  ' in text:
            text = text.replace('  ', ' ')
        tokens = nlp.get_tokens(text)
        text_list.append(fe.get_tokens_text(tokens))
        pos_list.append(fe.get_tokens_pos(tokens))
        dep_list.append(fe.get_tokens_dep(tokens))
        parent_pos_list.append(fe.get_tokens_parent_pos(tokens))
        tag_list.append(fe.get_tokens_tag(tokens))
        parent_tag_list.append(fe.get_tokens_parent_tag(tokens))
        semantic_vector.append(fe.get_tokens_semantic_vector(tokens,nlp))
    #print(np.array(semantic_vector).shape)
    feature_list[0].load_data(text_list,1)
    feature_list[0].save_feature('text','../semantic_role_model/training_data_feature/'+key+'/')
    feature_list[1].load_data(pos_list,1)
    feature_list[1].save_feature('pos','../semantic_role_model/training_data_feature/'+key+'/')
    feature_list[2].load_data(dep_list,1)
    feature_list[2].save_feature('dep','../semantic_role_model/training_data_feature/'+key+'/')
    feature_list[3].load_data(parent_pos_list,1)
    feature_list[3].save_feature('parent_pos','../semantic_role_model/training_data_feature/'+key+'/')
    feature_list[4].load_data(tag_list,1)
    feature_list[4].save_feature('tag','../semantic_role_model/training_data_feature/'+key+'/')
    feature_list[5].load_data(parent_tag_list,1)
    feature_list[5].save_feature('parent_tag', '../semantic_role_model/training_data_feature/' + key + '/')
    vector_list = []

    for i in range(0,6):
        ft.set_feature(feature_list[i])
        vector_list.append(ft.alignment(ft.transform_to_index(data_list[i])))


    semantic_vector=ft.alignment_2d(semantic_vector)
    #ft.save_np('../semantic_role_model/training_data/'+key,vector_list)
    for vector in vector_list:
        print(vector)
    #print(np.asarray(vector_list).shape)
    #ft.save_np('../semantic_role_model/semantic_vector/'+key+'_semantic_vector',np.asarray(semantic_vector))
    break