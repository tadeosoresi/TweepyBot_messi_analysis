from keys import ApiKey, Token, MeaningCloud
from connection import MongoDB
from datetime import datetime
import requests
import tweepy
import sys
import demjson
import time

class Streaming(tweepy.StreamListener):
    ''' Clase streaming de tweepy (see doc)
    Comentarios: setear numero maximo de tweets,
    setear rango de fechas si es necesario (la docu de 
    tweepy no explica como automatizar esto,  ni tampoco
    hay argumentos en tweepy.Stream para definirlos '''
    def __init__(self):
        super(Streaming, self).__init__()
        self.num_tweets = 0
        self.database = MongoDB()
        self._created_at = time.strftime('%Y-%m-%d')

    def on_status(self, status):
        if not hasattr(status, 'retweeted_status'): # Ignoramos rt
            body = status.text
            #created = status.created_at
            #date = created.strftime("%Y-%m-%d")
            #start="2021-08-02"
            #end="2021-08-12"
            print(status.source.encode('utf-8'), '<>' , body)
            if self.num_tweets < 500:
                tweet = {
                        'Id': str(status.id),
                        'User': str(status.user.name),
                        'Followers': int(status.user.followers_count),
                        'FriendsCount': int(status.user.friends_count),
                        'Place': str(status.user.location),
                        'Tweet': body,
                        'RT': int(status.retweet_count),
                        'Favs': int(status.favorite_count),
                        'Geo': status.geo,
                        'Coordinates': status.coordinates,
                        'Date': status.created_at,
                        'Language': status.lang,
                        'Feeling': '',
                        'CreatedAt': self._created_at
                    }
                
                self.database.insert_one(tweet)
                self.num_tweets += 1
            else:
                print('--- SCRAPING FINALIZADO ---')
                return False

    def on_error(self, status_code):
        if status_code == 420:
            print('--- NUMERO DE INTENTOS SUPERADO (PROBAR DENTRO DE 15 MINUTOS) ---')
            sys.exit(0)
        elif status_code == 401:
            print('--- CREDENCIALES INCORRECTAS ---')
            sys.exit(0)
        else:
            print(f'--- OCURRIO UN ERROR AL CONECTARSE ({status_code}) ---')
            sys.exit(0) 
    
    def on_timeout(self):
        print('Timeout...')
        return False
    
class HashtagBot():
    ''' Bot que recibe via argumento los hashtags a buscar en tw
    instancia tweepy streaming (ver docu de tweepy) y luego
    instancia clases para limpiar la data '''
    def __init__(self):
        if len(sys.argv) <= 1:
            print('--- ESPECIFICAR HASHTAGS VIA CONSOLA ---')
            sys.exit(0)
        else:
            self.listener = Streaming()
            self.parse = Parse()
            self.consumer_key, self.consumer_secret = ApiKey.returnkeys()
            self.access_token, self.access_token_secret = Token.returnkeys()
            self.search()

    def tweepy_connection(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)

        return auth

    def search(self):
        print('--- SEARCHING FOR TWEETS :D ---\n')
        sys.argv.remove(sys.argv[0])
        hashtags = []
        for position in range(len(sys.argv)):
            hashtags.append('#'+str(sys.argv[position]))
        auth = self.tweepy_connection()
        tw_listener = tweepy.Stream(auth=auth, listener=self.listener)
        tw_listener.filter(track=hashtags)
        self.parse.clean_tweets(hashtags)
        self.parse.parse_data()

class Parse():
    ''' Clase que limpia la data eliminando tweets basura
    y luego haciendo un analisis de sentimiento conectandose 
    a la api de meaningcloud '''
    def __init__(self):
        self.collection = MongoDB().return_collection()

    def meaningcloud_request(self, tweet, language):
        url, headers, payload = MeaningCloud.returndata(tweet, language)
        try:
            response = requests.post(url, headers=headers, data=payload)
            return response
        except requests.exceptions.ConnectionError:
            print('--- ERROR DE CONEXIÓN A MEANINGCLOUD ---')
            return False
    
    def clean_tweets(self, hashtags):
        for tweet in self.collection.find({'CreatedAt': time.strftime('%Y-%m-%d')}):
            if all(hashtag not in tweet['Tweet'] for hashtag in hashtags):
                self.collection.delete_one(tweet)
                print('--- DELETED THRASH TWEET ---')

    def parse_data(self):
        print('\n--- PARSING DATA IN MONGODB ---\n')
        for tweet in self.collection.find({'Feeling': ''}):
            result = self.meaningcloud_request(tweet['Tweet'], tweet['Language'])
            if result:
                json = demjson.decode(result.text)
                status = json['status']['code']
                if status == '0':
                    _id = tweet['Id']
                    try:
                        feeling = json['score_tag']
                    except KeyError:
                        self.collection.delete_one({'Id': tweet['Id']})
                        continue
                    self.collection.update_one(
                            {
                                'Id': _id
                            }, 
                                {'$set': {'Feeling': feeling}
                            }
                        )
                    print(f'--- UPDATED FEELING: ID {_id} ---')
                elif status == '104':
                    print('--- ERROR 104 (LIMITE 2 SOLICITUDES/SEG EXCEDIDO) ---')
                    time.sleep(5)
                elif status == '205':
                    print('--- LENGUAGE DE TWEET NO ADMITIDO POR MEANING CLOUD ---')
                    self.collection.delete_one(
                            {
                                'Id': tweet['Id']
                            }
                        )
                else:
                    print(f'--- ERROR DESCONOCIDO {status}, SKIPPING ---')
                    continue
            else:     
                continue
        print('\n--- DONE ---')


if __name__ =='__main__':
    HashtagBot()
    #MongoDB().delete_all()