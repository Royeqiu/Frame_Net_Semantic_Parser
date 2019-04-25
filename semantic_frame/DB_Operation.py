from utl import Injection_sql,Query_sql
db_connector = None
semantic_frame_feature_types = ['tag', 'parent_tag', 'target_child_dep', 'child_tag', 'child_text', 'label']
semantic_role_feature_types = ['tag','dep','label']
frame_label_type_index = len(semantic_frame_feature_types) - 1
role_label_type_index = len(semantic_role_feature_types) - 1
def is_in_features_dic(feature):
    rows = db_connector.execute(Query_sql.get_contains_of_feature_dictionary(feature))
    if rows[0][0]==0:
        return False
    else:
        return True

def __is_in_frame_model_features(feature, type, lexicon):
    rows = db_connector.execute(Query_sql.get_contains_of_frame_model_feature(feature, type, lexicon))
    if rows[0][0]==0:
        return False
    else:
        return True

def get_max_index_of_frame_model_fature(lexicon_unit, type):
    rows = db_connector.execute(Query_sql.get_max_frame_model_feature_index(lexicon_unit, type))
    index = rows[0][0]
    return index

def get_feature_dic_id(feature_text):
    rows = db_connector.execute(Query_sql.get_feature_dic_id(feature_text))
    index = rows[0][0]
    return index

def add_feature_dictionary(data_lists):
    for data in data_lists:
        if isinstance(data,list):
            for single_data in data:
                insert_data = single_data.replace('\'','\'\'')
                if not is_in_features_dic(insert_data):
                    db_connector.execute_insert(Injection_sql.get_inject_feature_dic_sql(insert_data))
        else:
            insert_data = data.replace('\'', '\'\'')
            if not is_in_features_dic(insert_data):
                db_connector.execute_insert(Injection_sql.get_inject_feature_dic_sql(insert_data))

def add_frame_model_feature(data_lists, lexicon_unit):
    for i,data in enumerate(data_lists):
        if isinstance(data, list):
            for single_data in data:
                selected_data = single_data.replace('\'','\'\'')
                if not __is_in_frame_model_features(selected_data, semantic_frame_feature_types[i], lexicon_unit):
                    index = get_max_index_of_frame_model_fature(lexicon_unit, semantic_frame_feature_types[i])
                    feature_id = get_feature_dic_id(selected_data)
                    db_connector.execute_insert(
                        Injection_sql.get_inject_frame_model_feature_sql(lexicon_unit, semantic_frame_feature_types[i], feature_id, index))
        else:
            selected_data = data.replace('\'','\'\'')
            if not __is_in_frame_model_features(selected_data, semantic_frame_feature_types[i], lexicon_unit):
                index = get_max_index_of_frame_model_fature(lexicon_unit, semantic_frame_feature_types[i])
                feature_id = get_feature_dic_id(selected_data)
                db_connector.execute_insert(
                    Injection_sql.get_inject_frame_model_feature_sql(lexicon_unit, semantic_frame_feature_types[i], feature_id, index))

def get_frame_label_max_index(lexicon_text):
    rows = db_connector.execute(Query_sql.get_frame_label_max_index(lexicon_text.replace('\'', '\'\'')))
    index = rows[0][0]
    return index

def add_frame_model_label(label_list, lexicon_text):
    if isinstance(label_list,list):
        for i,label in enumerate(label_list):
            if not __is_in_frame_model_features(label, semantic_frame_feature_types[frame_label_type_index], lexicon_text):
                index = get_frame_label_max_index(lexicon_text)
                feature_id = get_feature_dic_id(label)
                db_connector.execute_insert(
                    Injection_sql.get_inject_frame_model_feature_sql(lexicon_text, semantic_frame_feature_types[frame_label_type_index], feature_id, index))
    else:
        if not __is_in_frame_model_features(label_list, semantic_frame_feature_types[frame_label_type_index], lexicon_text):
            index = get_frame_label_max_index(lexicon_text)
            feature_id = get_feature_dic_id(label_list)
            db_connector.execute_insert(
                Injection_sql.get_inject_frame_model_feature_sql(lexicon_text, semantic_frame_feature_types[frame_label_type_index], feature_id, index))

def get_frame_feature_index(feature_list, lexicon_text, type):
    index_list = []
    if isinstance(feature_list, list):
        for feature in feature_list:
            select_feature = feature.replace('\'','\'\'')
            if __is_in_frame_model_features(lexicon=lexicon_text, type=type, feature=select_feature):
                rows = db_connector.execute(Query_sql.get_frame_feature_index(lexicon_text=lexicon_text, type=type, feature=select_feature))
                index_list.append(rows[0][0])
    else:
        select_feature = feature_list.replace('\'', '\'\'')
        if __is_in_frame_model_features(lexicon=lexicon_text, type=type, feature=select_feature):
            rows = db_connector.execute(Query_sql.get_frame_feature_index(lexicon_text=lexicon_text, type=type, feature=select_feature))
            index_list.append(rows[0][0])
    return index_list

def get_feature_index_lists(lexicon_text,feature_lists):
    index_lists = []
    for i,feature_list in enumerate(feature_lists):
        index_lists.append(get_frame_feature_index(feature_list, lexicon_text, semantic_frame_feature_types[i]))
    return index_lists

def get_semantic_frame_id(lu_id):
    rows = db_connector.execute(Query_sql.get_semantic_frame_id(lu_id))
    semantic_frame_id = rows[0][0]
    return semantic_frame_id

def add_semantic_frame_model_sentence(lu_id,text):
    text = text.replace('\'','\'\'')
    semantic_frame_id = get_semantic_frame_id(lu_id)
    db_connector.execute_insert(Injection_sql.get_inject_frame_model_sentence_sql(lu_id,semantic_frame_id,text))

def get_semantic_frame_model_sentence(is_filled = False):
    rows = db_connector.execute(Query_sql.get_semantic_frame_model_sentence(is_filled))
    return rows
def get_semantic_frame_mode_sentence_by_id(lu_id):
    rows = db_connector.execute(Query_sql.get_semantic_frame_model_sentence_by_id(lu_id))
    return rows
def get_lexicon_unit_name_by_id(lu_id):
    rows = db_connector.execute(Query_sql.get_lexicon_unit_by_id(lu_id))
    return  rows[0][2]

def get_lexicon_unit_by_text(lu_text):
    rows = db_connector.execute(Query_sql.get_lexicon_unit_by_text(lu_text.replace('\'','\'\'')))
    return rows

def get_latents(semantic_frame_id):
    rows = db_connector.execute(Query_sql.get_semantic_frame_by_id(semantic_frame_id))
    latent_id_list = rows[0][2]
    latent_lexicon_unit=[]
    for latent_id in latent_id_list:
        rows=db_connector.execute(Query_sql.get_lexicon_unit_by_id(latent_id))
        if len(rows)!=0:
            latent_lexicon_unit.append(rows[0])
    return latent_lexicon_unit


def get_label_index(lexicon_text,label):
    rows = db_connector.execute(Query_sql.get_frame_feature_index(lexicon_text, semantic_frame_feature_types[frame_label_type_index], label))
    return rows[0][0]

def add_semantic_frame_model_sentence_feature(sentence_id, feature_vecotr, label_index):
    db_connector.execute_update(Injection_sql.get_inject_frame_model_sentence_feature_label_sql(sentence_id, feature_vecotr, label_index))


def get_latent_lists(lexicon_text):
    related_lu_list = get_lexicon_unit_by_text(lexicon_text)
    latent_lists = []
    for related_lu in related_lu_list:
        semantic_frame_id = related_lu[2]
        latent_list = get_latents(semantic_frame_id)
        latent_lists.append(latent_list)
    return latent_lists

def get_lu_ids():
    lu_id_list = []
    rows = db_connector.execute(Query_sql.get_all_lu_id())
    for row in rows:
        lu_id_list.append(row[0])
    return lu_id_list

def get_semantic_frame_ids(lu_id = -1):
    semantic_frame_id_list = []
    if lu_id == -1:
        rows = db_connector.execute(Query_sql.get_all_semantic_frame_id())
    else:
        rows = db_connector.execute(Query_sql.get_semantic_frame_id(lu_id))
    for row in rows:
        semantic_frame_id_list.append(row[0])
    return semantic_frame_id_list

def get_annotation_datas(lu_id):
    text_list = []
    rows = db_connector.execute(Query_sql.get_select_annotation_text_sql(lu_id))
    for row in rows:
        text_list.append(row)
    return text_list

def get_annotation_texts(lu_id):
    text_list = []
    rows = db_connector.execute(Query_sql.get_select_annotation_text_sql(lu_id))
    for row in rows:
        text_list.append(row[1])
    return text_list
def get_annotation_label(annotation_text):
    rows = db_connector.execute(Query_sql.get_annotation_label(annotation_text))
    return rows
def get_semantic_frame_training_data(lu_id):
    training_data_rows = db_connector.execute(Query_sql.get_semantic_frame_training_data_sql(lu_id))
    input_list = []
    output_list = []
    for row in training_data_rows:
        input_list.append(row[0])
        output_list.append(row[1])
    return input_list,output_list

def get_latent_vector(semantic_frame_id):
    latent_vector_row = db_connector.execute(Query_sql.get_latent_vector(semantic_frame_id))
    return latent_vector_row[0][0]

def get_semantic_frame(semantic_frame_id):
    semantic_frame_row = db_connector.execute(Query_sql.get_semantic_frame(semantic_frame_id))
    return semantic_frame_row

def get_lexicon_unit_id(lexicon_text,semantic_frame_name):
    rows =db_connector.execute(Query_sql.get_lu_id_by_lexicon_text_and_frame_name(lexicon_text,semantic_frame_name))
    return rows

def __is_in_role_model_features(lu_id, feature, type):
    rows = db_connector.execute(Query_sql.get_contains_role_model_feature(lu_id=lu_id,feature=feature,type=type))
    if rows[0][0]==0:
        return False
    else:
        return True
def get_role_feature_max_index(lu_id, type):
    rows = db_connector.execute(Query_sql.get_role_model_max_index(lu_id=lu_id,type=type))
    return rows[0][0]

def add_semantic_role_model_feature(feature_lists, lu_id):
    for i,feature_list in enumerate(feature_lists):
        if isinstance(feature_list, list):
            for feature in feature_list:
                selected_feature = feature.replace('\'', '\'\'')
                if not __is_in_role_model_features(lu_id, selected_feature, semantic_role_feature_types[i]):
                    dic_id = get_feature_dic_id(selected_feature)
                    feature_index = get_role_feature_max_index(lu_id, semantic_role_feature_types[i]) + 2 # 0 for panding 1 for unknown word
                    db_connector.execute_insert(Injection_sql.get_inject_role_model_feature_sql
                                                (lu_id=lu_id,type=semantic_role_feature_types[i],feature_dic_id=dic_id,index=feature_index))

        else:
            selected_feature = feature_list.replace('\'','\'\'')
            if not __is_in_role_model_features(lu_id=lu_id, feature=selected_feature, type=semantic_role_feature_types[i]):
                dic_id = get_feature_dic_id(selected_feature)
                feature_index = get_role_feature_max_index(lu_id, semantic_role_feature_types[i]) + 2
                db_connector.execute_inset(Injection_sql.get_inject_role_model_feature_sql
                                           (lu_id=lu_id,type=semantic_role_feature_types[i],feature_dic_id=dic_id,index=feature_index))

def get_role_feature_index(feature_list,lu_id,type):
    index_list = []
    if isinstance(feature_list, list):
        for feature in feature_list:
            select_feature = feature.replace('\'', '\'\'')
            if __is_in_role_model_features(lu_id=lu_id, type=type, feature=select_feature):
                rows = db_connector.execute(
                    Query_sql.get_role_feature_index(lu_id=lu_id, type=type, feature=select_feature))
                index_list.append(rows[0][0])
            else:
                index_list.append(1)
    else:
        select_feature = feature_list.replace('\'', '\'\'')
        if __is_in_role_model_features(lu_id=lu_id, type=type, feature=select_feature):
            rows = db_connector.execute(
                Query_sql.get_role_feature_index(lu_id=lu_id, type=type, feature=select_feature))
            index_list.append(rows[0][0])
        else:
            index_list.append(1)
    return index_list

def get_role_label_max_index(lu_id):
    rows = db_connector.execute(Query_sql.get_role_label_max_index(lu_id=lu_id))
    return rows[0][0]

def add_semantic_role_model_label(label_list,lu_id):
    if isinstance(label_list, list):
        for i, label in enumerate(label_list):
            selected_label = label.replace('\'','\'\'')
            if not __is_in_role_model_features(lu_id=lu_id , feature=selected_label, type=semantic_role_feature_types[role_label_type_index]):
                index = get_role_label_max_index(lu_id) + 2 #original = 1 pading = 0
                feature_dic_id = get_feature_dic_id(selected_label)
                db_connector.execute_insert(
                    Injection_sql.get_inject_role_model_feature_sql(
                        lu_id=lu_id, type=semantic_role_feature_types[role_label_type_index], feature_dic_id=feature_dic_id, index=index))
    else:
        selected_label = label_list.replace('\'', '\'\'')
        if not __is_in_role_model_features(lu_id=lu_id, feature=selected_label,
                                           type=semantic_role_feature_types[role_label_type_index]):
            index = get_role_label_max_index(lu_id) + 2
            feature_dic_id = get_feature_dic_id(selected_label)
            db_connector.execute_insert(
                Injection_sql.get_inject_role_model_feature_sql(
                    lu_id=lu_id, type=semantic_role_feature_types[role_label_type_index], feature_dic_id=feature_dic_id,
                    index=index))
def __is_in_role_model_lu_id(lu_id):
    rows = db_connector.execute(Query_sql.role_model_contains_lu_id(lu_id))
    if rows[0][0]==0:
        return False
    else:
        return True

def add_role_model_lu_id(lu_id):
    if not __is_in_role_model_lu_id(lu_id):
        db_connector.execute_insert(Injection_sql.get_inject_role_model_lu_id(lu_id))

def add_role_model_window_size(lu_id,window_size):
    db_connector.execute_update(Injection_sql.get_inject_role_model_window_size(lu_id,window_size))

def get_window_size(lu_id):
    sql=Query_sql.get_window_size(lu_id)
    rows = db_connector.execute(sql)
    return rows[0][0]

def add_role_model_sentences(lu_id,text,feature_vector,label_vector):
    sql = Injection_sql.get_injext_role_model_sentences(lu_id=lu_id,text=text,feature_vector=feature_vector,label_vector=label_vector)
    db_connector.execute_insert(sql)

def get_role_model_sentences(lu_id):
    sql = 'select text,feature_vector,label_vector from semantic_role_model_sentence where lu_id = %s' %lu_id
    return db_connector.execute(sql)