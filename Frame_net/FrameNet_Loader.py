import Query_sql
from Frame_net import Lexicon_Unit_Info,Frame_Info,Annotation_Info,Annotation_Label
def __transform_Lexicon_Unit_Info_into_obj(db, lexicon_unit_info, lex_dic):
    tmp_lexicon_unit_dict = dict()
    tmp_lexicon_unit_dict['lu_id'] = lexicon_unit_info.lu_id
    tmp_lexicon_unit_dict['frame_id'] = lexicon_unit_info.semantic_frame_id
    semantic_rows = db.execute(Query_sql.get_semantic_frame_by_id(lexicon_unit_info.semantic_frame_id))
    tmp_lexicon_unit_dict['frame_name'] = semantic_rows[0][1]
    tmp_lexicon_unit_dict['pos'] = lexicon_unit_info.pos

    if lexicon_unit_info.text not in lex_dic.keys():
        tmp_lexicon_unit_list = []
        tmp_lexicon_unit_list.append(tmp_lexicon_unit_dict)
        lex_dic[lexicon_unit_info.text] = tmp_lexicon_unit_list
    else:
        lex_dic[lexicon_unit_info.text].append(tmp_lexicon_unit_dict)

def __transform_Semantic_Frame_Info_into_obj(db, frame_info, frame_dic):

    if frame_info.semantic_frame_name not in frame_dic.keys():
        tmp_frame_dict = dict()
        tmp_latent_list = []
        for latent_id in frame_info.latent_id:
            latent_rows = db.execute(Query_sql.get_lexicon_unit_by_id(latent_id))
            for latent_row in latent_rows:
                tmp_latent_dict = dict()
                tmp_latent_dict['lexicon'] = latent_row[2]
                tmp_latent_dict['pos'] = latent_row[3]
                tmp_latent_dict['id'] = latent_row[0]
                tmp_latent_list.append(tmp_latent_dict)
        tmp_frame_dict['lu'] = tmp_latent_list
        frame_dic[frame_info.semantic_frame_name] = tmp_frame_dict



def get_lexicon_unit_and_semantic_frame_infos(db_connector):
    rows = db_connector.execute(Query_sql.get_all_lexicon_unit())
    lex_dic=dict()
    frame_dic=dict()
    for row in rows:
        tmp_lu_info = Lexicon_Unit_Info.Lexicon_Unit_Info(lu_id=row[0],semantic_frame_id=row[1],text=row[2],pos=row[3])
        tmp_frame_info = Frame_Info.Frame_Info(lu_id=row[0],semantic_frame_id=row[1],semantic_frame_name=row[4],pos=row[3],latent_id=row[5])
        __transform_Lexicon_Unit_Info_into_obj(db_connector, tmp_lu_info, lex_dic)
        __transform_Semantic_Frame_Info_into_obj(db_connector, tmp_frame_info, frame_dic)
    return lex_dic,frame_dic

def get_annotation_number_by_lu_id(db_connector,lu_id):
    rows = db_connector.execute(Query_sql.get_annotation_number_by_lu_id(lu_id))
    for row in rows:
        number = row[0]
    return number

def get_annotation_data_by_lu_id(db_connector, lexicon_unit_id):
    doc_annotation=dict()
    sentence_dic = dict()
    rows = db_connector.execute(Query_sql.get_annotation_data(lexicon_unit_id))
    for row in rows:
        if row[0] not in sentence_dic.keys():
            sentence_dic[row[0]] = Annotation_Info.Annotation_Info(lu_id=lexicon_unit_id,text=row[2])
            annotation_info = sentence_dic[row[0]]
            annotation_info.add_annotation_label(
                Annotation_Label.Annotation_Label(text_id=row[0], start_offset=row[6], end_offset=row[7],
                                                  semantic_role=row[8]))
        else:
            annotation_info = sentence_dic[row[0]]
            annotation_info.add_annotation_label(Annotation_Label.Annotation_Label(text_id=row[0],start_offset=row[6],
                                                                                   end_offset=row[7],semantic_role=row[8]))
    doc_annotation['annotation']=[__transform_annotation_into_obj(sentence_dic[x]) for x in sentence_dic.keys()]
    return doc_annotation

def __transform_annotation_into_obj(annotation_info):
    annotation_dict=dict()
    annotation_dict['text'] = annotation_info.text
    annotation_dict['annotation'] = [[annotation_label.get_annotation_label_obj() for annotation_label in annotation_info.annotations_labels]]
    return annotation_dict
