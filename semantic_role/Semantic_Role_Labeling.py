from Frame_net import Doc_Annotation
import numpy as np
import json
import re

def add_feature(feature_list,feature):
    feature_list[feature] = len(feature_list)+1

def is_in_feature(feature_list,feature):
    return feature in feature_list.keys()

def split_sent(sentence):
    """
    tmp=sentence.replace('--','@')
    tmp=tmp.replace(' -',' *')
    tmp=tmp.replace('- ','~ ')
    if tmp[0] == '-':
        tmp=tmp.replace('-','*',2)

    text = tmp.replace('-',' - ').split(' ')
    copy_text = []
    for i,data in enumerate(text):
        str = data.replace('@', '--')
        str = str.replace('*','-')
        str = str.replace('~','-')
        copy_text.append(str)
"""
    return sentence.split(' ')

def get_word_leng(sentence):
    """
    print('@@'+sentence)
    tmp = sentence.replace('--', '@')
    tmp = tmp.replace(' -',' *')
    tmp = tmp.replace('- ','~ ')
    if '-' == tmp[0] or '-' == tmp[len(tmp)-1]:
        tmp=tmp.replace('-','*',1)

    text = tmp.replace('-', ' - ').split(' ')
    print('$$'+str(text))
    """
    return len(sentence.split(' '))

def get_feature_label(feature_list, feature):
    if is_in_feature(feature_list, feature):
        return feature_list[feature]
    else:
        add_feature(feature_list, feature)
        return feature_list[feature]

def save_feature(filename,feature_index):
    file = open(filename,'w')
    for key in feature_index.keys():
        file.write(key+'\t'+str(feature_index[key])+'\n')

def load_feature(filename,feature_index):
    file = open(filename,'r')
    for line in file:
        data = line.strip('\n')
        fi=data.strip('\t')
        feature_index[fi[0]]= int(fi[1])

def alignment(nparray):
    max_length = 0
    alignment_array = []
    for array in nparray:
        if max_length< len(array):
            max_length= len(array)
    for array in nparray:
        new_array= np.zeros(max_length)
        new_array[0:len(array)] = array
        alignment_array.append(new_array)
    return np.array(alignment_array)

def save_label(filename,label):
    np.save()
annotation = Doc_Annotation.Doc_Annotation()
annotation.load_annotation()
for i,key in enumerate(annotation.lu_annotation.keys()):
    key=str(2378)
    #print(key)
    feature_list = dict()

    if i%50==0:

        print(str(i)+'s lu have been processed!')
    label_list=[]
    i = 0

    for annotation_set in annotation.lu_annotation[key]['annotation']:
        i+=1
        text = annotation_set['text'].strip(' ').lower()
        while '  ' in text:
            text = text.replace('  ', ' ')
        annotation_labels = annotation_set['annotation']
        sentence_leng = get_word_leng(text)
        sentence_label = np.zeros(sentence_leng)
        print('!!'+text)
        print(sentence_leng)
        for annotation_label in annotation_labels:
            for label in annotation_label:
                print(label)
                if(text[int(label['start']):int(label['end']) + 1])=='':
                    continue
                word_leng = get_word_leng(text[int(label['start']):int(label['end']) + 1])
                sentence_index = 0
                words = split_sent(text)
                for word_index,word in enumerate(words):
                    if sentence_index == int(label['start']):
                        tmp = ''
                        for count in range(0,word_leng):
                            tmp += words[word_index+count]+' '
                            sentence_label[word_index+count] = get_feature_label(feature_list, label['name'])
                        found = True
                        break
                    sentence_index += len(word)
                    #print(word)
                    if word!='-':
                        sentence_index += 1
                    else:
                        sentence_index -=1
        print(sentence_label)
        label_list.append(sentence_label)
    nplablel_list = alignment(label_list)
    print(nplablel_list)
    #np.save('../semantic_role_model/label/'+key,nplablel_list)
    #save_feature('../semantic_role_model/feature/'+key,feature_list)
    break