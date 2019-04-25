import xml.etree.ElementTree as ET
import os
import logging
import json


logging.basicConfig(level=logging.INFO)
class FrameNet:
    def __init__(self,lu_dir='data/fndata-1.6/lu/',frame_dir='data/fndata-1.6/frame/', load_ori_lu = True ,load_ori_frame = True):
        self.lu_dir=lu_dir
        self.frame_dir=frame_dir
        self.lex_dic=dict()
        self.frame_dic=dict()
        self.set_sentence =''
        if load_ori_lu:
            self.lu_filenames = os.listdir(self.lu_dir)
            logging.info('Loading lu')
            self.__load_ori_lu()
            logging.info('Loading Finished')
        if load_ori_frame:
            self.frame_filenames = os.listdir(self.frame_dir)
            logging.info('Loading frame')
            self.__load_ori_frame()
            logging.info('Loading Finished')

    def __load_ori_lu(self):
        for i, file in enumerate(self.lu_filenames):
            if ('lu' in file):
                tree = ET.parse(self.lu_dir + file)
                root = tree.getroot()

                lexicon,pos,frame_id,frame_name,lu_id=self.get_lex_pos_frameID_frameName(root)
                if pos=='prep':
                    continue
                if lexicon in self.lex_dic.keys():
                    tmp_dict=dict()
                    tmp_dict['lu_id'] = lu_id
                    tmp_dict['frame_id'] = frame_id
                    tmp_dict['frame_name'] = frame_name
                    tmp_dict['pos'] = pos
                    self.lex_dic[lexicon].append(tmp_dict)
                else:
                    tmp_list = []
                    tmp_dict = dict()
                    tmp_dict['lu_id'] = lu_id
                    tmp_dict['frame_id'] = frame_id
                    tmp_dict['frame_name'] = frame_name
                    tmp_dict['pos'] = pos
                    tmp_list.append(tmp_dict)
                    self.lex_dic[lexicon] = tmp_list

    def __load_ori_frame(self):
        for i, file in enumerate(self.frame_filenames):
            if ('.xml' in file):
                tree = ET.parse(self.frame_dir+file)
                root = tree.getroot()
                name=file.split('.')[0]
                self.frame_dic[name]=self.get_lex_pos_luID_core_set(root)

    def __check_phrase_in_lu(self, words):
        is_contains = False
        is_equal = False
        for dic in self.lex_dic.keys():
            if words in dic:
                if words == dic:
                    is_equal = True
                    is_contains = True
                    break
                else:
                    is_contains = True
        return is_contains, is_equal

    def __find_longest_phrase(self, tokens, main_token_index):
        words = tokens[main_token_index].lemma_
        confidence_word = ''
        is_contains, is_equal = self.__check_phrase_in_lu(words)
        if is_contains:
            if is_equal:
                confidence_word = words
            if main_token_index != len(tokens) - 1:
                following_word = self.__find_following_word(tokens, words, confidence_word, main_token_index + 1)
                if following_word is not None:
                    confidence_word = following_word

        return confidence_word

    def __find_following_word(self, tokens, words, confidence_word, next_token_index):
        words += ' ' + tokens[next_token_index].lemma_
        is_contains, is_equal = self.__check_phrase_in_lu(words)
        if is_contains:
            if is_equal:
                confidence_word = words
            if next_token_index != len(tokens) - 1:
                following_word = self.__find_following_word(tokens, words, confidence_word, next_token_index + 1)
                if following_word is not None:
                    confidence_word = following_word
        return confidence_word

    def load_lu(self,dir):
        file = open(dir,'r')
        for datas in file:
            lu_frame = datas.strip('\n').rstrip('\t').split('\t')
            lex = lu_frame[0]
            tmp_list = []
            for i in range(1,len(lu_frame)):
                tmp_list.append(json.loads(lu_frame[i]))
            self.lex_dic[lex]=tmp_list

    def load_frame(self,dir):
        file = open(dir, 'r')
        for datas in file:
            frame_latent = datas.strip('\n').strip('\t').split('\t')
            frame_name = frame_latent[0]
            self.frame_dic[frame_name] = json.loads(str(frame_latent[1]))

    def write_lu(self,dir='../data/lu.txt'):
        file = open(dir,'w')
        for key in self.lex_dic.keys():
            file.write(key.encode('utf8').decode('cp950','ignore') +'\t')
            for frame in self.lex_dic[key]:
                file.write(json.dumps(frame)+'\t')
            file.write('\n')

    def write_frame(self,dir='../data/frame.txt'):
        file = open(dir, 'w')
        for key in self.frame_dic.keys():
            file.write(key.encode('utf8').decode('cp950', 'ignore') + '\t')
            file.write(json.dumps(self.frame_dic[key]) + '\t')
            file.write('\n')

    def get_lex_pos_luID_core_set(self, root):
        lu_cord_dic=dict()
        lu_set=[]
        core_set=[]
        for child in root:
            if '}' in child.tag:
                tag = child.tag.split('}')[1]
            if tag == 'lexUnit':
                tmp_dic=dict()
                frame_data = child.get('name').split('.')
                lex = frame_data[0]
                pos = frame_data[1]
                id = child.get('ID')
                tmp_dic['lexicon'] =lex
                tmp_dic['pos'] = pos
                tmp_dic['id'] = id
                lu_set.append(tmp_dic)
            if tag == 'FE':
                core_type = child.get('coreType')
                if core_type == 'Core':
                    tmp_dic = dict()
                    name = child.get('name')
                    abbrev = child.get('abbrev')
                    tmp_dic['coreType'] = core_type
                    tmp_dic['name'] = name
                    tmp_dic['abbrev'] = abbrev
                    core_set.append(tmp_dic)
        lu_cord_dic['lu']=lu_set
        lu_cord_dic['core']=core_set
        return lu_cord_dic

    def get_lex_pos_frameID_frameName(self, root):
        lexicon_pos = root.get("name").split('.')
        lexicon = lexicon_pos[0]
        pos = lexicon_pos[1]
        lu_id = root.get('ID')
        frame_id = root.get('frameID')
        frame_name = root.get('frame')
        return lexicon, pos, frame_id, frame_name,lu_id

    def get_lex_pos_frameID_by_frameName(self, root):
        lexicon_pos = root.get("name").split('.')
        lexicon = lexicon_pos[0]
        pos = lexicon_pos[1]
        frame_id = root.get('frameID')
        frame_name = root.get('frame')
        return lexicon,pos,frame_id,frame_name

    def set_sentence(self,sentence):
        self.set_sentence = sentence

    def get_latent_by_frameName(self,name):
        return self.frame_dic[name]

    def get_lu_candidate(self,tokens):
        candidate_set = []
        shift = 0
        for i in range (len(tokens)):
            candidate_dic = dict()
            if shift != 0:
                shift -= 1
                continue
            candidate_phrase = self.__find_longest_phrase(tokens, i)
            if candidate_phrase=='':
                continue
            candidate_dic['lexicon'] = candidate_phrase
            shift = len(candidate_phrase.split(' ')) - 1
            candidate_dic['high_index'] = i + shift
            candidate_dic['low_index'] = i
            candidate_set.append(candidate_dic)
        return candidate_set

    def get_frame_name_by_lu(self,lexicon_unit):
        return self.lex_dic[lexicon_unit]

    ###len(lexicon_text) < len(lu_id_list)
    """
    The lexicon_text only provide unique lexicon text and one lexicon_text should have at leaset one lu_id
    """
    def get_all_lu_id_semantic_frame_id_text(self):
        lu_id_list = []
        lexicon_text_list = self.lex_dic.keys()
        semantic_frame_id_list = []
        for lexicon_text in lexicon_text_list:
            for lexicon_unit in self.lex_dic[lexicon_text]:
                lu_id_list.append(lexicon_unit['lu_id'])
                semantic_frame_id_list.append(lexicon_unit['frame_id'])
        return lu_id_list,lexicon_text,semantic_frame_id_list

