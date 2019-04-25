import xml.etree.ElementTree as ET
import os
import logging
import json

logging.basicConfig(level=logging.INFO)

class Doc_Annotation:
    def __init__(self,lu_dir='../data/fndata-1.6/lu/',load_ori = False):
        self.lu_dir=lu_dir
        self.lu_filenames = None

        if load_ori:
            self.lu_filenames = os.listdir(self.lu_dir)
        self.lu_annotation = dict()
        self.count = 0

    def load_ori_annotation(self):
        for i, file in enumerate(self.lu_filenames):
            if ('lu' in file):
                tree = ET.parse(self.lu_dir + file)
                root = tree.getroot()
                id = root.get('ID')
                lu_dic = dict()
                lu_dic['frame'] = self.get_frame(root)
                lu_dic['annotation'] = self.get_sentence(root,lu_dic['frame'])
                lu_dic['lexicon_unit'] = root.get('name').split('.')[0]
                lu_dic['pos'] = root.get('name').split('.')[1]
                self.lu_annotation[id] = lu_dic

    def write_annotation(self, file_name='data/annotation.txt'):
        file=open(file_name, 'w')
        for key in self.lu_annotation.keys():
            file.write(key+'\t')
            file.write(json.dumps(self.lu_annotation[key])+'\n')

    def load_annotation(self,dir='../data/annotation.txt'):
        file=open(dir,'r')
        for data in file:
            annotations = data.strip('\n').split('\t')
            self.lu_annotation[annotations[0]] = json.loads(annotations[1])

    def get_sentence(self,root,core):
        sentence_label_list=[]

        for child in root:
            tag = self.remove_meta_url(child.tag)
            if tag == 'subCorpus':
                for sentence_node in child:
                    sentence_dict=dict()
                    text = self.load_text(sentence_node)
                    annotation_set = self.load_annotation_set(sentence_node,core)
                    sentence_dict['text'] = text
                    sentence_dict['annotation'] = annotation_set
                    sentence_label_list.append(sentence_dict)
        return sentence_label_list

    def load_text(self,sentence_node):

        return sentence_node[0].text

    def load_annotation_set(self,sentence_node,core):
        nodes_range = range(2,len(sentence_node))
        annotation_set_list=[]
        for i in nodes_range:
            for layer_node in sentence_node[i]:
                type = layer_node.get('name')
                if type == 'Target' or type == 'FE':
                    annotation_set_list.append(self.get_label(layer_node,core))
        return annotation_set_list

    def remove_meta_url(self,tag):
        true_tag = tag.split('}')[1]
        return true_tag

    def get_label(self,layer_node,core):
        annotation_set=[]
        for label_node in layer_node:

            if label_node.get('start') is None:
                continue
            if label_node.get('name') not in core and label_node.get('name') != 'Target':
                continue
            frame_element = dict()
            frame_element['name'] = label_node.get('name')
            frame_element['start'] = label_node.get('start')
            frame_element['end'] = label_node.get('end')
            annotation_set.append(frame_element)
        return annotation_set

    def get_frame(self,root):
        header = root[0]
        core_list = []
        for mata_data in header:
            if self.remove_meta_url(mata_data.tag) =='frame':
                frame = mata_data
                for element in frame:
                    if element.get('type')=='Core':
                        core_list.append(element.get('name'))
        return  core_list

    def add_lu_annotation(self,lu_id,doc_annotation):
        self.lu_annotation[lu_id]=doc_annotation

    def get_all_annotation_text(self,lu_id):
        text_list = []
        if lu_id in self.lu_annotation.keys():
            for annotation_set in self.lu_annotation[lu_id]['annotation']:
                text_list.append(annotation_set['text'])
        return text_list