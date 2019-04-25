def get_all_lexicon_unit():
    sql = 'select lu.lu_id,lu.semantic_frame_id,lu.text,lu.pos,sf.semantic_frame_name,sf.latent_lexicon_unit_id ' \
          'from semantic_frame as sf, lexicon_unit as lu ' \
          'where sf.semantic_frame_id = lu.semantic_frame_id'
    return sql

def get_lexicon_unit_by_id(lexicon_unit_id):
    sql = 'select lu_id,semantic_frame_id,text,pos from lexicon_unit where lu_id = %s' %(lexicon_unit_id)
    return sql

def get_lexicon_unit_by_text(lexicon_text):
    sql = 'select * from lexicon_unit where text = \'%s\'' %(lexicon_text)
    return sql

def get_semantic_frame_by_id(semantic_frame_id):
    sql = 'select semantic_frame_id,semantic_frame_name,latent_lexicon_unit_id from semantic_frame where semantic_frame_id = %s' % (semantic_frame_id)
    return sql

def get_annotation_number_by_lu_id(lexicon_unit_id):
    sql = 'select count(*) from annotation_data where lu_id = %s' %(lexicon_unit_id)
    return sql

def get_select_annotation_data_id_sql(lu_id,text):
    sql = 'select * from annotation_data where lu_id = %s and text = \'%s\'' % (lu_id,text)
    return sql



def get_annotation_data(lexicon_unit_id):
    sql = 'select * from annotation_data as ad, annotation_label as al  where ad.id=al.annotation_data_id and ad.lu_id = %s' %(lexicon_unit_id)
    return sql

def get_select_annotation_text_sql(lu_id):
    sql = 'select id,text from annotation_data where lu_id = %s' %(lu_id)
    return sql

def get_lu_id_by_lexicon_text_and_frame_name(lexicon_text, frame_name):
    sql = 'select lu.lu_id  from lexicon_unit as lu, semantic_frame as sf where lu.text=\'%s\' and sf.semantic_frame_name=\'%s\' and lu.semantic_frame_id=sf.semantic_frame_id' %(lexicon_text,frame_name)
    return sql

def get_contains_of_feature_dictionary(feature_text):
    sql = 'select count(*) from  feature_dictionary as fd where  fd.text=\'%s\'' %(feature_text)
    return sql

def get_contains_of_frame_model_feature(feature_text, type, lexicon_unit):
    sql = 'select count(*) from semantic_frame_model_feature as sf, feature_dictionary as fd where sf.feature_dic_id = fd.id and sf.lexicon_text=\'%s\' and sf.type=\'%s\'  and fd.text = \'%s\'' %(lexicon_unit,type,feature_text)
    return sql

def get_max_frame_model_feature_index(lexicon_text, type):
    sql = 'select count(*) from semantic_frame_model_feature as sf where  sf.lexicon_text=\'%s\' and sf.type=\'%s\'  ' %(lexicon_text, type)
    return sql

def get_feature_dic_id(lexicon_text):
    sql = 'select id from feature_dictionary where text = \'%s\'' %(lexicon_text)
    return sql

def get_frame_label_max_index(lexicon_text):
    sql = 'select count(*) from semantic_frame_model_feature where lexicon_text =\'%s\' and type =\'label\' ' %(lexicon_text)
    return sql

def get_role_label_max_index(lu_id):
    sql = 'select count(*) from semantic_role_model_feature where lu_id =%s and type =\'label\''%(lu_id)
    return sql

def get_frame_feature_index(lexicon_text, type, feature):
    sql = 'select sfmf.index from semantic_frame_model_feature as sfmf, feature_dictionary as fd ' \
          'where sfmf.lexicon_text = \'%s\' and sfmf.type = \'%s\' and sfmf.feature_dic_id =  fd.id and fd.text = \'%s\'' \
          %(lexicon_text,type,feature)
    return sql

def get_semantic_frame_id(lu_id):
    sql = 'select sf.semantic_frame_id from semantic_frame as sf, lexicon_unit as lu where sf.semantic_frame_id = lu.semantic_frame_id and lu.lu_id = %s' %(lu_id)
    return sql

def get_semantic_frame_model_sentence(is_filled = False):
    if is_filled:
        is_filled = 'not Null'
    else:
        is_filled = 'Null'
    sql = 'select id,lu_id,semantic_frame_id,text from semantic_frame_model_sentence as sfmf where sfmf.feature_vector is %s' %(is_filled)
    return sql

def get_all_lu_id():
    sql = 'select lu_id from lexicon_unit'
    return sql

def get_semantic_frame_id(lu_id):
    sql = 'select semantic_frame_id from lexicon_unit where lu_id=%s' %(lu_id)
    return sql

def get_all_semantic_frame_id():
    sql = 'select semantic_frame_id from semantic_frame'
    return sql

def get_semantic_frame_training_data_sql(lu_id):
    sql = 'select feature_vector,label from semantic_frame_model_sentence where lu_id = %s' %(lu_id)
    return sql

def get_latent_vector(semantic_frame_id):
    sql = 'select latent_vector from semantic_frame where semantic_frame_id = %s' %(semantic_frame_id)
    return sql

def get_semantic_frame_model_sentence_by_id(lu_id):
    sql = 'select id,lu_id,semantic_frame_id,text from semantic_frame_model_sentence where lu_id = %s'%(lu_id)
    return sql

def get_semantic_frame_model(lexicon_text):
    sql = 'select model from semantic_frame_model where lexicon_text = \'%s\''%(lexicon_text)
    return sql

def is_contains_semantic_frame_model(lexicon_text):
    sql = 'select count(model) from semantic_frame_model where lexicon_text = \'%s\''%(lexicon_text)
    return sql

def is_contains_semantic_frame_model_label(lexicon_text):
    sql = 'select count(index) from semantic_frame_model_feature where lexicon_text=\'%s\' and type = \'label\'' %(lexicon_text)
    return sql

def get_semantic_frame_model_label_index(lexicon_text):
    sql = 'select index from semantic_frame_model_feature where lexicon_text = \'%s\' and type = \'label\'' %(lexicon_text)
    return sql

def get_semantic_frame(semantic_frame_id):
    sql = 'select * from semantic_frame where semantic_frame_id = %s' %(semantic_frame_id)
    return sql

def get_contains_role_model_feature(lu_id,feature,type):
    sql = 'select count(*) from semantic_role_model_feature as srmf, feature_dictionary as fd ' \
          'where srmf.lu_id =%s and srmf.type=\'%s\' and srmf.feature_dic_id=fd.id and fd.text=\'%s\' '%(lu_id,type,feature)
    return sql

def get_role_model_max_index(lu_id, type):
    sql = 'select count(*) from semantic_role_model_feature where type = \'%s\' and lu_id = %s' %(type,lu_id)
    return sql

def get_annotation_label(annotation_id):
    sql = 'select * from annotation_label as al where al.annotation_data_id = %s' %(annotation_id)
    return sql

def get_role_feature_index(lu_id, feature, type):
    sql = 'select index from semantic_role_model_feature as srmf, feature_dictionary as fd ' \
          'where srmf.type =\'%s\' and srmf.lu_id =%s and fd.text = \'%s\' and fd.id = srmf.feature_dic_id' %(type,lu_id,feature)
    return sql

def role_model_contains_lu_id(lu_id):
    sql='select count(*) from semantic_role_model where lu_id =%s' %(lu_id)
    return sql

def get_window_size(lu_id):
    sql='select window_size from semantic_role_model where lu_id=%s' %(lu_id)
    return sql