import DB_Connector

db_connector = DB_Connector.DB_Connector(user_name='postgres', db_name='semantic_parser', host='127.0.0.1',
                                         password='')


sql1='select sfms.id,sfms.semantic_frame_id,sfms.lu_id,lu.text from semantic_frame_model_sentence as sfms, lexicon_unit as lu where lu.lu_id = sfms.lu_id'
rows = db_connector.execute(sql1)
for i,row in enumerate(rows):
    if i % 50 ==0:
        print ('%s sentences' %(i))
    id = row[0]
    semantic_frame_id=row[1]
    lu_text = row[3]
    sql2 = 'select sfmf.index,sfmf.lexicon_text,sfmf.type,fd.text ' \
           'from semantic_frame_model_feature as sfmf, feature_dictionary as fd ' \
           'where sfmf.feature_dic_id = fd.id and sfmf.type = \'label\' and sfmf.lexicon_text = \'%s\' and fd.text=\'%s\''%(lu_text,row[1])
    rows2 = db_connector.execute(sql2)
    index = rows2[0][0]
    sql3 = 'update semantic_frame_model_sentence set label=%s where id=%s' %(index,id)
    db_connector.execute_update(sql3)