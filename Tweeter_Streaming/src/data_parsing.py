import json
import io

#Apertura del archivo que contiene los datos de geolocalizacion
json_file = io.open('Export1.json',"r",encoding="utf-8")
json_data = json.load(json_file,strict=False)
json_file.close()
#Apertura del archivo que va a contener las coordenadas
coords_file = io.open('coordenadas.tweets.txt','a',encoding="utf-8")
#Separacion de las coordenadas de cada Tweet
for tweet in json_data:
    coordinates = tweet.get("geoLocation").get("coordinates")
    latitud = str(coordinates[1])
    longitud = str(coordinates[0])
    coordinate = latitud+" "+longitud
    coords_file.write(coordinate+"\n")
    print(coordinate)
coords_file.close()