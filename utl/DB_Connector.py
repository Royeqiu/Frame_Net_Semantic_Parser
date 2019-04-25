import psycopg2
import psycopg2.extras

class DB_Connector:

    def     __init__(self,host,db_name,user_name,password):
        try:
            self.conn = psycopg2.connect(dbname=db_name,user=user_name,host=host,password=password)
            self.conn.set_client_encoding('utf-8')
            self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except:
            print("I am unable to connect to the database")

    def execute(self, sql):
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        return rows

    def get_sentences(self):
        sql = 'select intent_code, sample_sentence from nlp_intent_training;'
        sentences_list = []
        rows = self.execute(sql)
        for row in rows:
            sentence_dict = dict()
            sentence = row['sample_sentence']
            intent = row['intent_code']
            sentence_dict['sample_sentence'] = sentence
            sentence_dict['intent_code'] = intent
            sentences_list.append(sentence_dict)

        return sentences_list

    def execute_update(self,sql):
        self.cur.execute(sql)
        self.conn.commit()

    def execute_insert(self,sql):
        self.execute_update(sql)