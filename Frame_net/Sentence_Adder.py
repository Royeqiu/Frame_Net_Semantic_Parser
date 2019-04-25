from Frame_net import Doc_Annotation
import os

class Sentence_Adder:
    def __init__(self, doc_annotation):
        self.doc_annotation = doc_annotation

    def load_new_sentences(self,lu_id, file_name):
        file = open(file_name, 'r')
        for data in file:
            label = data.strip('\n').split('\t')
            sentence_annotation = dict()
            text = label[0].lower()
            sentence_annotation['text'] = text
            loaded_annotation_list = label[1:]
            created_annotation_list = []
            for annotation in loaded_annotation_list:
                tmp_dic = dict()
                created_annotation_list.append(tmp_dic)
                each_column = annotation.split(' ')
                tmp_dic['name'] = each_column[0]
                tmp_dic['start'] = each_column[1]
                tmp_dic['end'] = each_column[2]
            sentence_annotation['annotation'] = [created_annotation_list]
            self.doc_annotation.lu_annotation[lu_id]['annotation'].append(sentence_annotation)

    def save_annotation(self,file_name):
        self.doc_annotation.write_annotation(file_name)

