import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import pandas as pd

class MongoDB():
    ''' Clase que inicializa MongoDB y provee de distintos metodos '''
    def __init__(self):
        try:
            self.host_mongo  = 'mongodb://localhost:27017/'
            self.cursor= MongoClient(self.host_mongo)
            self.db = self.cursor.twitter_bot
        except ConnectionFailure:
            print('--- ERROR AL CONECTARSE A LOCALHOST, POR FAVOR VERIFICAR SI MONGODB ESTA CORRIENDO ---')
            return False
    
    def insert_one(self, query, collection='tweets'):
        self.db[collection].insert_one(query)
        print('--- TWEET INSERTADO EN BD ---')
    
    def delete_all(self, collection='tweets'):
        self.db[collection].remove({})
        print('--- ELIMINADOS TODOS LOS REGISTROS DB ---')
    
    def return_db(self):
        return self.db

    def return_collection(self, collection='tweets'):
        return self.db[collection]

class Dataframe():
    ''' Clase para usar en jupyter notebook
     que trae la data de mongo en formato dataframe '''
    def __init__(self):
        self.db = MongoDB().return_db()
        self.collection_names = self.db.collection_names(include_system_collections=False)

    def tweets_to_df(self, collection='tweets'):
        if not collection in self.collection_names:
            print('--- COLECCIÓN "TWEETS" NO EXISTE EN MONGODB, POR FAVOR EJECUTAR SCRAPPER PRIMERO ---')
            return False
        else:
            data = self.db[collection]
            df = pd.DataFrame(list(data.find({})))
            print('--- COLECCIÓN ---> TWEETS ---> TO DATAFRAME ---> DONE ---')

            return df
    
