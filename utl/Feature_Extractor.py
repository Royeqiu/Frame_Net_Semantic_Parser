from NLP import NLP_Tool
import numpy as np
class Feature_Extractor:

    def get_target_pos(self,tokens,target):
        target_pos = ''
        for i in range(target['low_index'],target['high_index']+1):
            if target_pos != 'VERB':
                target_pos = tokens[i].pos_
        return target_pos

    def get_target_tag(self,tokens,target):
        target_tag = ''
        for i in range(target['low_index'],target['high_index']+1):
            if 'VB' not in target_tag:
                target_tag = tokens[i].tag_
        return target_tag

    def get_target_parent_head_tag(self, tokens, target):

        parent_head_tag=''
        for i in range(target['low_index'],target['high_index']+1):
            if  tokens[i].head.text == tokens[i].text:
                parent_head_tag=tokens[i].head.tag_
            elif not self.is_in_phrase(tokens[i].head,target):
                parent_head_tag=tokens[i].head.tag_

        return parent_head_tag

    def is_in_phrase(self,word,target):
        if word.text in target['lexicon'].split(' '):
            return True
        else:
            return False

    def get_target_child_dependency(self, tokens, target):

        child_dep=[]
        for i in range(target['low_index'],target['high_index']+1):
            for child in tokens[i].children:
                child_dep.append(child.dep_)
        return child_dep

    def get_target_child_tag(self,tokens,target):
        child_tag = []
        for i in range(target['low_index'], target['high_index'] + 1):
            for child in tokens[i].children:
                child_tag.append(child.tag_)
        return child_tag

    def get_target_child_pos(self, tokens, target):
        child_pos=[]
        for i in range(target['low_index'],target['high_index']+1):
            for child in tokens[i].children:
                child_pos.append(child.pos_)
        return child_pos

    def get_target_child_text(self, tokens, target):
        child_text = []
        for i in range(target['low_index'], target['high_index'] + 1):
            for child in tokens[i].children:
                child_text.append(child.text)
        return child_text

    def get_target_child_vector(self,tokens,target):
        child_vector =np.zeros((300), dtype='f')
        child_num = 0
        for i in range(target['low_index'], target['high_index'] + 1):
            for child in tokens[i].children:
                if child.has_vector:
                    child_num += 1
                    child_vector += child.vector
        if child_num == 0:
            return child_vector
        else:
            return child_vector/len(child_num)

    def get_tokens_text(self,tokens):

        return  [token.text.lower() for token in tokens]

    def get_tokens_pos(self,tokens):

        return [token.pos_ for token in tokens]
    """
    def get_tokens_child(self,tokens):
        for token in tokens:
            for child in token.children:
                
        return
    """
    def get_tokens_dep(self,tokens):

        return [token.dep_ for token in tokens]

    def get_tokens_lemma(self,tokens):
        return [tokens.lemma_ for token in tokens]

    def get_tokens_parent_pos(self,tokens):
        return [token.head.pos_ for token in tokens]

    def get_tokens_parent_text(self,tokens):
        return [token.head.text for token in tokens]

    def get_tokens_parent_tag(self,tokens):
        return [token.head.tag_ for token in tokens]

    def get_tokens_tag(self,tokens):
        return [token.tag_ for token in tokens]

    def get_tokens_semantic_vector(self,tokens,nlp_tool):
        result_vector=[]
        for token in tokens:
            vector = nlp_tool.get_phrase_vector(token.text)
            if vector is not None:
                result_vector.append(vector)
            else:
                vector = np.zeros((300), dtype='f')
                result_vector.append(vector)
        return result_vector

