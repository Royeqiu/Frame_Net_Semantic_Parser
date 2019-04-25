import numpy as np
import os

class Feature:
    def __init__(self):
        self.feature_to_index = dict()
        self.index_to_feature = dict()
        self.size = 0
        self.feature_space = set()

    def load_data(self, lists,offset = 0):
        self.feature_space = self.load_feature_space(lists)
        self.feature_to_index,self.index_to_feature = self.load_feature_index(self.feature_space,offset)
        self.size=len(self.feature_space)

    def load_feature_space(self,lists):
        data_space = set()
        for _list in lists:
            if isinstance(_list, list):
                for data in _list:
                    data_space.add(data)
            else:
                data_space.add(_list)

        return data_space

    def load_feature_index(self, word_set,offset):

        feature_to_index = dict()
        index_to_feature = dict()
        for i,word in enumerate(word_set):
            feature_to_index[word] = i+offset
            index_to_feature[i+offset] = word

        return feature_to_index,index_to_feature

    def save_feature(self,type_name=' ',dir='model/'):
        file_name = '_feature_index.txt'
        if not os.path.exists(dir):
            os.makedirs(dir)
        file = open(dir+type_name+file_name,'w')
        for key in self.feature_to_index.keys():
            file.write(key.encode('utf8').decode('cp950','ignore') +'\t')
            file.write(str(self.feature_to_index[key])+'\n')

        file_name = '_index_feature.txt'
        file = open(dir+type_name+file_name,'w')
        for key in self.index_to_feature.keys():
            file.write(str(key)+'\t')
            file.write(self.index_to_feature[key].encode('utf8').decode('cp950','ignore') +'\n')

    def load_feature(self,filename):
        file = open(filename,'r')
        size_file = open(filename,'r')
        self.size = len(size_file.readlines())
        size_file.close()
        for data in file:
            feature_index = data.strip('\n').split('\t')
            self.feature_to_index[feature_index[0]]=int(feature_index[1])
            self.index_to_feature[int(feature_index[1])] = feature_index[0]
            self.feature_space.add(feature_index[0])
        file.close()

    def save_np(self,filename,nparray):
        np.save(filename, nparray)

    def load_np(self,filename):
        np.load(filename)
