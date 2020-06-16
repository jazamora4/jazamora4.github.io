import http.server
import socketserver
import pymongo
import json
import time
import os
import io


class coordinates_parsing():
    cadena_de_conexion = ""

    def __init__(self, cadena):
        self.cadena_de_conexion = cadena

    def parsing(self, database):
        # Apertura del archivo que va a contener las coordenadas
        print("Procesando Datos")
        if os.path.exists("coordenadas.tweets.txt"):
            os.remove("coordenadas.tweets.txt")
        coords_file = io.open('coordenadas.tweets.txt', 'a', encoding="utf-8")
        # Query de los datos desde la base de datos
        Query = database.find({'$and': [{'geoLocation.coordinates.0':{'$lte': -74.398689,'$gte': -81.788583}},{'geoLocation.coordinates.1':{'$lte':1.164222,'$gte':-4.522947}}]})
        
        # Separacion de las coordenadas de cada Tweet
        i=0
        coordinatesJSON = {}
        data_return = {}
        for tweet in Query:
            coordinates = tweet.get("geoLocation").get("coordinates")
            coordinatesJSON = {}
            coordinatesJSON['lat'] = coordinates[1]
            coordinatesJSON['long'] = coordinates[0]
            data_return['coordenadas'+str(i)] = coordinatesJSON
            i=i+1
            latitud = str(coordinates[1])
            longitud = str(coordinates[0])
            coordinate = latitud+" "+longitud
            coords_file.write(coordinate+"\n")
        coords_file.close()
        return data_return
    def parsing_Sentiment(self,database):
        Query = database.find()
        i=0
        coordinatesJSON = {}
        data_return = {}
        for tweet in Query:
            coordinates = tweet.get("sentiment")
            coordinatesJSON = {}
            coordinatesJSON['sent'] = coordinates
            data_return['sentiment'+str(i)] = coordinatesJSON
            i=i+1
        return data_return
    def data_base(self):
        gbd2020_Cluster=pymongo.MongoClient(self.cadena_de_conexion)
        DB_TweetsPrueba = gbd2020_Cluster.tweetsPrueba
        Coll_TweetsNew = DB_TweetsPrueba.tweetsNew
        return Coll_TweetsNew
    def data_base2(self):
        gbd2020_Cluster=pymongo.MongoClient(self.cadena_de_conexion)
        DB_TweetsPrueba = gbd2020_Cluster.tweetsPrueba
        Coll_TweetsNew = DB_TweetsPrueba.tweetsCorrupcion
        return Coll_TweetsNew


class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
 
    # Check the URI of the request to serve the proper content.
    def do_GET(self):
        if "URLToTriggerGetRequestHandler" in self.path:
        	# If URI contains URLToTriggerGetRequestHandler, execute the python script that corresponds to it and get that data
            # whatever we send to "respond" as an argument will be sent back to client
            coordinates_parse = coordinates_parsing("mongodb+srv://dbJoseZamora:balto1010@gbd2020-uzfjc.mongodb.net/gbd2020?retryWrites=true&w=majority")
            database = coordinates_parse.data_base()
            database2 = coordinates_parse.data_base2()
            content = coordinates_parse.parsing(database)
            content2 = coordinates_parse.parsing_Sentiment(database2)
            content3 = {}
            content3['coords'] =content
            content3['sentiment'] = content2
            self.respond(json.dumps(content3).encode()) # we can retrieve response within this scope and then pass info to self.respond
        else:
            super(MyHandler, self).do_GET() #serves the static src file by default
 
    def handle_http(self, data):
        self.send_response(200)
        # set the data type for the response header. In this case it will be json.
        # setting these headers is important for the browser to know what 	to do with
        # the response. Browsers can be very picky this way.
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        return data
 
     # store response for delivery back to client. This is good to do so
     # the user has a way of knowing what the server's response was.
    def respond(self, data):
        response = self.handle_http(data)
        self.wfile.write(response)
    
 
# This is the main method that will fire off the server. 
if __name__ == '__main__':
    HOST_NAME = ''
    PORT_NUMBER=8080
    server_class = http.server.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))
