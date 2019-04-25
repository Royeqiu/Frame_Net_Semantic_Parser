import DB_Connector
from NLP import NLP_Tool
from semantic_frame import DB_Operation as dbo
db_connector = DB_Connector.DB_Connector(user_name='postgres', db_name='semantic_parser', host='127.0.0.1', password='')
dbo.db_connector = db_connector
nlp = NLP_Tool.NLP_Tool()
semantic_frame_ids = dbo.get_semantic_frame_ids()
for i,semantic_frame_id in enumerate(semantic_frame_ids):
    semantic_frame_id = 64
    if i% 50 == 0:
        print ('%s semantic_frame_has been transformed! '%(str(i)))
    print(semantic_frame_id)
    vectors = []
    for latent in dbo.get_latents(semantic_frame_id):
        print(latent[2])
        vector = nlp.get_phrase_vector(latent[2])
        if vector is not None:
            vectors.append(vector)
    latent_vector = nlp.get_avg_vector(vectors)
    print(latent_vector)
    #db_connector.execute_update(Injection_sql.get_inject_semantic_latent_vector_sql(semantic_frame_id,latent_vector))
    break