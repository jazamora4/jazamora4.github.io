string = "@negroactivo28 Lo felicito mijo Es cuestión d gusto y se respeta"
palabras = ['leninn moreno','leninmoreno','@lenin','moreno','fueramoreno','#fueramoreno','fuera moreno','corrupcion moreno','moreno es bucaram','#morenoesbucaram','gobiernocorrupto','#gobiernocorrupto','#elperogobierno','elpeorgobierno','apoyo moreno','adelante moreno','fuerza moreno','apoyo a lenin moreno']
for x in palabras:
    if(x in string.lower()):
        print("TRUE")
    else:
        print("FALSE")
print(string)