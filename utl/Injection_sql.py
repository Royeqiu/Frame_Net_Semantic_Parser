import pickle as pickle
def __turn_list_to_postgresListStr(list):
    PLStr='{'
    for i,value in enumerate(list):
        if isinstance(value,str):
            PLStr+='\''+value+'\''
        else:
            PLStr+=str(value)
        if i != len(list)-1:
            PLStr+=','
    PLStr+='}'
    return PLStr

def get_inject_semantic_frame_sql(frame_info):
    plstr = __turn_list_to_postgresListStr(frame_info.latent_id)
    sql='insert into semantic_frame(semantic_frame_id,semantic_frame_name,latent_lexicon_unit_id) values(%s,\'%s\',\'%s\')' %(frame_info.semantic_frame_id,frame_info.semantic_frame_name,plstr)
    return sql

def get_inject_lexicon_unit_sql(lexicon_unit_info):
    sql='insert into lexicon_unit(lu_id,semantic_frame_id,text,pos) values(%s,%s,\'%s\',\'%s\')' %(lexicon_unit_info.lu_id,lexicon_unit_info.semantic_frame_id,lexicon_unit_info.text,lexicon_unit_info.pos)
    return sql

def get_inject_annotation_data_sql(annotation_info):
    sql = 'insert into annotation_data(lu_id,text) values(%s,\'%s\')' % (annotation_info.lu_id,annotation_info.text)
    return sql

def get_inject_annotation_label_sql(annotation_label):
    sql = 'insert into annotation_label(annotation_data_id,start_offset,end_offset,semantic_role) values(%s,%s,%s,\'%s\')' % (annotation_label.text_id,annotation_label.start_offset,annotation_label.end_offset,annotation_label.semantic_role)
    return sql

def get_inject_feature_dic_sql(text):
    sql = 'insert into feature_dictionary(text) values(\'%s\')' %(text)
    return sql

def get_inject_frame_model_feature_sql(lexicon_text, type, feature_dic_id, index):
    sql = 'insert into semantic_frame_model_feature (feature_dic_id,lexicon_text,index,type) values(%s,\'%s\',%s,\'%s\')' %(feature_dic_id,lexicon_text,index,type)
    return sql


def get_inject_frame_model_sentence_sql(lu_id,semantic_frame_id,text):
    sql = 'insert into semantic_frame_model_sentence (lu_id,semantic_frame_id,text) values(%s,%s,\'%s\')' %(lu_id,semantic_frame_id,text)
    return sql

def get_inject_frame_model_sentence_feature_label_sql(sentence_id,feature_vector,label):
    sql = 'update semantic_frame_model_sentence set feature_vector =\'%s\', label = %s where id = %s '\
          %(__turn_list_to_postgresListStr(feature_vector),label,sentence_id)
    return sql

def get_inject_semantic_latent_vector_sql(semantic_frame_id,latent_vector):
    plstr = __turn_list_to_postgresListStr(latent_vector)
    sql = 'update semantic_frame set latent_vector = \'%s\' where semantic_frame_id = %s'%(plstr,semantic_frame_id)
    return sql

def get_inject_semantic_frame_model_sql(lexicon_text,binary_model,prob,sentences_count):
    sql = 'insert into semantic_frame_model (lexicon_text,model,precision,sample_count) values(\'%s\',%s,%s,%s)'%(lexicon_text,binary_model,prob,sentences_count)
    return sql

def get_inject_role_model_feature_sql(lu_id,type,feature_dic_id,index):
    sql = 'insert into semantic_role_model_feature (lu_id,feature_dic_id,type,index) values(%s,%s,\'%s\',%s)' %(lu_id,feature_dic_id,type,index)
    return sql

def get_inject_role_model_window_size(lu_id,window_size):
    sql = 'update semantic_role_model set window_size=%s where lu_id = %s' %(window_size,lu_id)
    return sql

def get_inject_role_model_lu_id(lu_id):
    sql = 'insert into semantic_role_model (lu_id) values(%s)'%(lu_id)
    return sql

def get_injext_role_model_sentences(lu_id,text,feature_vector,label_vector):
    sql ='insert into semantic_role_model_sentence (lu_id,text,feature_vector,label_vector) values(%s,\'%s\',%s,%s)' %(lu_id,text,feature_vector,label_vector)
    return sql