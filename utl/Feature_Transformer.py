import numpy as np
import random
from utl import Feature
class Feature_Transformer:

    def __init__(self):
        self.size = 0
        self.feature_space = set()
        self.feature_to_index = dict()
        self.index_to_feature = dict()
        self.feature = Feature.Feature()

    def load_data(self, lists,offset = 0):
        self.feature_space = self.load_feature_space(lists)
        self.feature_to_index,self.index_to_feature = self.load_feature_index(self.feature_space,offset)
        self.size=len(self.feature_space)

    def set_feature(self,feature):
        self. feature = feature


    def transform_to_vector(self,lists):
        return self.transform_into_vector(lists)

    def transform_to_index(self,lists):
        feature_to_index = self.feature.feature_to_index
        vector = []
        for _list in lists:
            if isinstance(_list, list):
                tmp_list = []
                for data in _list:
                    if data not in feature_to_index.keys():
                        tmp_list.append(0)
                    else:
                        tmp_list.append(feature_to_index[data])
                vector.append(tmp_list)
            else:
                if _list not in feature_to_index.keys():
                    vector.append(0)
                else:
                    vector.append(feature_to_index[_list])

        return vector



    def load_feature_space(self,lists):
        data_space = set()
        for _list in lists:
            if isinstance(_list, list):
                for data in _list:
                    data_space.add(data)
            else:
                data_space.add(_list)

        return data_space

    def load_feature_index(self, word_set,offset = 0):

        feature_to_index = dict()
        index_to_feature = dict()
        for i,word in enumerate(word_set):
            feature_to_index[word] = i+offset
            index_to_feature[i+offset] = word

        return feature_to_index,index_to_feature

    def transform_into_vector(self,lists):
        size = self.feature.size
        feature_to_index = self.feature.feature_to_index
        vector = np.zeros((len(lists),size))
        for i,_list in enumerate(lists):
            if isinstance(_list, list):
                for data in _list:
                    if data not in feature_to_index.keys():
                        continue
                    vector[i][feature_to_index[data]] = 1
            else:
                if _list not in feature_to_index.keys():
                    continue
                vector[i][feature_to_index[_list]] = 1

        return vector

    def save_feature(self,type_name=' ',dir='model/'):
        file_name = '_feature_index.txt'
        file = open(dir+type_name+file_name,'w')
        for key in self.feature_to_index.keys():
            file.write(key+'\t')
            file.write(str(self.feature_to_index[key])+'\n')

        file_name = '_index_feature.txt'
        file = open(dir+type_name+file_name,'w')
        for key in self.index_to_feature.keys():
            file.write(str(key)+'\t')
            file.write(self.index_to_feature[key]+'\n')

    def load_feature(self,type_name=' ',dir='model/'):
        file_name = '_feature_index.txt'
        file = open(dir + type_name + file_name, 'r')
        for data in file:
            feature_index = data.strip('\n').split('\t')
            self.feature_to_index[feature_index[0]] = int(feature_index[1])
            self.feature_space.add(feature_index[0])

        file_name = '_index_feature.txt'
        file = open(dir + type_name + file_name, 'r')
        for data in file:
            index_feature = data.strip('\n').split('\t')
            self.feature_to_index[index_feature[0]] = index_feature[1]

        self.size = len(self.feature_space)

    def concatenate(self,lists):

        _main_list = np.copy(lists[0])
        
        for i in range(1,len(lists)):
            copy_list = []
            for j, data in enumerate(_main_list):
                tmp = np.concatenate((_main_list[j], lists[i][j]), axis=0)
                copy_list.append(tmp)
            _main_list = np.array(copy_list,dtype=np.float32)

        return _main_list

    def to_nparray(self,list):
        return np.array(list,dtype=np.float32)

    def save_np(self,filename,nparray):
        np.save(filename, nparray)

    def load_np(self,filename):
        return np.load(filename)

    def data_separation(self,data,percent):
        size = len(data)
        pool = []
        for i in range(0,size):
            pool.append(i)
        data_size = int(size * percent)
        index = random.sample(pool,data_size)
        training = []
        validation = []
        for i in range(0,size):
            if i in index:
                training.append(data[i])
            else:
                validation.append(data[i])

        return np.array(training,dtype=np.float32),np.array(validation,dtype=np.float32),index

    def alignment(self,nparray,max_length = 0):

        alignment_array = []
        if max_length ==0:
            for array in nparray:
                if max_length < len(array):
                    max_length = len(array)
        for array in nparray:
            new_array = np.zeros(max_length)
            new_array[0:len(array)] = array
            alignment_array.append(new_array)
        return np.array(alignment_array)

    def alignment_2d(self,nparray,max_length = 0):
        alignment_array = []
        if max_length == 0:
            for array in nparray:
                if max_length < len(array):
                    max_length = len(array)
        for array in nparray:
            new_array = np.zeros((max_length,len(array[0])))
            new_array[0:len(array)] = array
            alignment_array.append(new_array)
        return np.array(alignment_array)

    def nparray_from_float_to_int(self,nparray):
        int_nparray=np.ndarray(nparray.shape,dtype=np.int32)
        for i,array in enumerate(nparray):
            if isinstance(array, np.ndarray):
                for j,data in enumerate(array):
                    int_nparray[i][j]=int(data)
            else:
                int_nparray[i]=int(data)
        return int_nparray

    def transform_from_index_to_label(self,index):
        return self.feature.index_to_feature[int(index)]