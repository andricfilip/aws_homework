
import uuid
import psycopg2
import os
import conf  

from model.ann_model import ANNModel

class Database():
    __instance = None
    conn = None

    def __init__(self):
        self.conn = psycopg2.connect(
            host = "localhost",
            database= "ml_db",
            user = "postgres",
            password = "postgres",
            port=5432
            )
        # print(conf.db_host)
        # print(conf.db_name)
        # print(conf.user)
        # print(conf.password)
        # print(conf.db_name)
        # print(conf.db_port)
        # self.conn = psycopg2.connect(
        #     host = conf.db_host,
        #     database= conf.db_name,
        #     user = conf.user,
        #     password = conf.password,
        #     port= conf.db_port)

        
        self._create_table()
        Database.__instance = self



    @staticmethod
    def getInstance():
        if(Database.__instance == None):
            Database()
            
        return Database.__instance

    def get_all_models(self):
        query = "select * from model"
        dbh = self.conn.cursor()
        dbh.execute(query)
        records = dbh.fetchall()

        models = []
        for row in records:
            path = row[5]
            model_name = path.split('/')[1]
            # print(model_name)
            models.append(ANNModel(id = row[0], model_name = row[1], mse = row[2], auc = row[3], acc = row[4],path=row[5]))
        return models

    
    def _create_table(self):
        query = "create table if not exists model(id uuid primary key, model_name varchar(100) not null, mse float not null, auc_score float not null, accuracy float not null, model_path varchar(100) not null)"
        dbh = self.conn.cursor()
        dbh.execute(query)
        self.conn.commit()


    def add_model(self, model_name, mse, auc_score, accuracy, model_path):
        query = "insert into model(id, model_name, mse, auc_score, accuracy, model_path) values('"+ str(uuid.uuid1())+ "', '"+model_name +"', " +str(mse) +", " +str(auc_score) +", " +str(accuracy) +", '" +model_path +"')"
        print(query)
        dbh = self.conn.cursor()
        dbh.execute(query)
        self.conn.commit()

    def get_model_path_by_id(self, id):
        query = "select model_path from model where id = '"+str(id)+"'"
        dbh = self.conn.cursor()
        dbh.execute(query)
        record = dbh.fetchall()

        return record[0][0]








