import DB_Connector
from semantic_frame import DB_Operation as dbo,Semantic_Frame_Model_Feature as sfmf
from Frame_net import FrameNet_Loader,FrameNet_Data,Doc_Annotation
from NLP import NLP_Tool

db_connector = DB_Connector.DB_Connector(user_name='postgres', db_name='semantic_parser', host='127.0.0.1', password='')
frameNet= FrameNet_Data.FrameNet(load_ori_frame=False, load_ori_lu=False)
lex_dic,frame_dic=FrameNet_Loader.get_lexicon_unit_and_semantic_frame_infos(db_connector)
frameNet.lex_dic=lex_dic
frameNet.frame_dic=frame_dic
nlp = NLP_Tool.NLP_Tool()
sfmf.nlp = nlp
lu_id_list,semantic_frame_id_list,lexicon_text_list=frameNet.get_all_lu_id_semantic_frame_id_text()
doc_annotation=Doc_Annotation.Doc_Annotation()
for i,lu_id in enumerate(lu_id_list):
    lu_id = 4344

    print('%s lu has been extracted!' %(i))
    doc_annotation.add_lu_annotation(lu_id,FrameNet_Loader.get_annotation_data_by_lu_id(db_connector,lu_id))
    dbo.db_connector=db_connector
    semantic_frame_id = dbo.get_semantic_frame_id(lu_id)
    text_list = dbo.get_annotation_texts(lu_id)
    lexicon_text = dbo.get_lexicon_unit_name_by_id(lu_id)
    for text in text_list:
        print(text)
        print(lexicon_text)
        feature_lists = sfmf.get_frame_feature_lists(frameNet, lexicon_text, nlp.get_tokens(text))
        if feature_lists is None:
            continue
        dbo.add_semantic_frame_model_sentence(lu_id,text)
    break