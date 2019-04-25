import os
import numpy as np
from utl import Feature
training_path = 'semantic_role_model/training_data/'
label_path= 'semantic_role_model/label/'
alignment_file = open('semantic_role_model/alignment_size.txt','w')
label_file = open('semantic_role_model/label_size.txt','w')

training_filename= os.listdir(training_path)
for file_count,name in enumerate(training_filename):
    print(name)
    training_data = np.load('semantic_role_model/training_data/'+name)
    id = name.split('.')[0]
    #print(training_data[0].shape == label.shape)
    feature = Feature.Feature()
    feature.load_feature('semantic_role_model/feature/'+id)
    label_size = len(feature.index_to_feature)
    alignment_size = training_data[0].shape[1]
    alignment_file.write(str(id)+'\t'+str(alignment_size)+'\n')
    label_file.write(str(id)+'\t'+str(label_size)+'\n')
