import tweepy
import json
import io
import pymongo
#Conexion con la base de datos

cadena_de_conexion = "mongodb+srv://dbJoseZamora:balto1010@gbd2020-uzfjc.mongodb.net/gbd2020?retryWrites=true&w=majority"

gbd2020_Cluster=pymongo.MongoClient(cadena_de_conexion)

DB_TweetsPrueba = gbd2020_Cluster.tweetsPrueba
Coll_TweetsNew = DB_TweetsPrueba.tweetsNew

#-----------------------------------------------------------------------------
#Listener de Tweets
#Crear un StreamListener
#El stream listener tiene dos casos
#on data
#on error
class MiPrimerListener(tweepy.StreamListener):

    def on_data(self, raw_data):
        self.process_data(raw_data)
        return True
    def process_data(self,raw_data):
        try:
            data = json.loads(raw_data)
        except Exception as e:
            log = io.open("../log/logFile.txt","a",encoding="utf-8")
            try:
                log.write("Error en el parseo de datos \n"+str(e))
            except Exception as e1:
                log.write("Error de escritura en la linea 33\n")
                return True
            log.close()
            print(e)
            return True
        if data.get('geo') is not None:
            location = data.get('geo').get('coordinates')
        else:
            location = [0,0]
        text = data.get('text').replace('\n',' ')
        fulltext = data.get('extended_tweet')
        if(isinstance(fulltext,dict)):
            full = fulltext['full_text']
        else:
            full=text
        full = full.replace('"','')
        user = '@' + data.get('user').get('screen_name')
        created = data.get('created_at')
        #Formateo de la cadena JSON
        json_string = '{'+'"user":"'+user+'","geoLocation":{"type":"Point","coordinates":['+str(location[1])+','+str(location[0])+']},"created":"'+created+'","text":"'+full+'"}'
        try:
            json_obj = json.loads(json_string,strict=False)
        except Exception as e:
            log = io.open("../log/logFile.txt","a",encoding="utf-8")
            log.write(json_string+","+"\n")
            log.close()
            print(e)
            print(json_string)
            return True
        Coll_TweetsNew.insert_one(json_obj)#Incersion en la base de datos
        if(location[0]!=0):
            print("Tweet del usuario "+user+" ha sido guardo con geolocacion en la base de datos")
        else:
            print("Tweet del usuario "+user+" ha sido guardado en la base de datos")        
        return True
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return False
class MaxStream():
    def __init__(self, auth, listener):
        self.stream = tweepy.Stream(auth=auth, listener=listener)
    def start(self):
        self.stream.filter(locations=[-81.788583,-4.522947,-74.398689,1.164222])
if __name__ == "__main__":
    print("Iniciando....")
    listener = MiPrimerListener()
    
    auth = tweepy.OAuthHandler("claves de aplicacion","claves de aplicacion")
    auth.set_access_token("tokens de aplicacion","tokens de aplicacion")
    stream = MaxStream(auth,listener)
    print("Capturando Tweets")
    stream.start()
#py heatmap.py --debug -o photos.png -r 50 --width 1000 --osm -B 0.8 --osm_base http://b.tile.stamen.com/toner coordenadas.tweets.txt