import os
import sys

print ("Opciones seleccionadas: "+str(sys.argv))
if(len(sys.argv) == 1):
    nombre = "mapaDeCalor.png"
    nombre1 = "coordenadas.tweets.txt"
else:
    nombre = sys.argv[1]
    nombre1 = sys.argv[2]

os.system('py ../modules/heatmap.py --debug -o ../img/'+nombre+' -r 50 --width 1000 --osm -B 0.8 --osm_base http://b.tile.stamen.com/toner ../cord_files/'+nombre1)