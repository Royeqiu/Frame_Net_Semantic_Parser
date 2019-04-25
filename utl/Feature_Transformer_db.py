import numpy as np

def __find_max_feature(_list):
    max_feature = -1
    if isinstance(_list,list):
        for value in _list:
            if value> max_feature:
                max_feature=value
    else:
        max_feature = _list
    return max_feature

def transform_to_vector(feature, max_feature = -1):
    if max_feature ==-1:
        max_feature=__find_max_feature(feature)
    vector = np.zeros(max_feature)
    if isinstance(feature,list):
        for single_feature in feature:
            vector[single_feature-1] = 1
    else:
        vector[feature-1] = 1
    return vector
def __get_sum_of_lists_leng(lists):
    leng = 0
    for list in lists:
        leng +=len(list)
    return leng

def concatenate(lists):
    result_vector = []
    for i,list in enumerate(lists):
        result_vector = np.concatenate((result_vector, list), axis=0)

    return result_vector
