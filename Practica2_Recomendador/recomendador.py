import pandas
import re
found = False
anterior = ""

def leerfichero():  # leer el fichero csv
    pelis=pandas.read_csv('imdb.csv',sep=',')
    pelis.columns=['Name','Date','Rate','Votes','Genre','Duration','Type','Certificate','Episodes','Nudity','Violence','Profanity','Alcohol','Frightening']
    pelis=pelis[['Name','Date','Rate','Genre','Certificate','Nudity','Violence','Profanity','Frightening']]
    return pelis # devuelve el dataframe eliminando algunas columnas que no vamos a utilizar

def distance(str1, str2): # calcula el parecido entre el string introducido y cada string introducido
  d=dict()
  for i in range(len(str1)+1):
     d[i]=dict()
     d[i][0]=i
  for i in range(len(str2)+1):
     d[0][i] = i
  for i in range(1, len(str1)+1):
     for j in range(1, len(str2)+1):
        d[i][j] = min(d[i][j-1]+1, d[i-1][j]+1, d[i-1][j-1]+(not str1[i-1] == str2[j-1]))
  return d[len(str1)][len(str2)]

def Search_names(Name):
    global found, anterior
    # Search for opening bracket in the name followed by
    # any characters repeated any number of times
    if re.search(str(anterior), Name):
        global found 
        found = True
    return Name

def moviename():
    global anterior, found
    top=[[20,20],[20,20],[20,20]] # top falso inicial que se irá modificandos
    anterior = input("Nombre de la película: ") # nombre de la película
    pelis['Name'] = pelis['Name'].apply(Search_names)
    if not found:
        for i in range(len(pelis)):
            intento = pelis['Name'][i]
            valor = distance(anterior,intento)
            new = [valor,intento]
            if new[0] < top[0][0]:
                top=[new,top[0],top[1]]
            elif new[0] < top[1][0]:
                top[2],top[1]=top[1],new
            elif new[0] < top[2][0]:
                top[2]=new 
        for i in range(0,3):
            print(f'- {i+1} {top[i][1]}')
        eleccion = int(input(f' No tenemos {anterior} en el dataset, estas son algunas posibilidades alternativas, elija introduciendo el número asociado: '))
        anterior = top[eleccion-1][1]
    return anterior

def recomendar(anterior,pelis):
    top=[[0,0],[0,0],[0,0]] # las tres mejores recomendaciones, inciadas a 0
    statsr = [] # las estadísticas de la pelicula solicitada
    for i in range(0,6176):# dentro del dataset
        if (pelis['Name'][i]==anterior): # si la pelicula es la correcta
            for category in ['Name','Date','Rate','Genre','Certificate','Nudity','Violence','Profanity','Frightening']:
                a = pelis[category][i]
                statsr.append(a) # lista con las características, para ir sumando
    statsr[3] = str(statsr[3]).split(",")
    # en caso de que haya varios generos, se deben recorrer todos para ver si es parecido en alguno
    for i in range(len(pelis)): # para cada película del dataset
        genref = str(pelis["Genre"][i]).split(",") 
        rating = 0
        for j in range(len(genref)): # se mira cuantos géneros tiene en común con la inicial, si no es ninguno ni se considera
            for k in range(len(statsr[3])):
                if genref[j]== statsr[3][k]:
                    rating +=6

        if rating > 0: # solo la considera si tiene algún genero en común
            try:# suma del rating, para tener películas de calidad parecida
                if abs(float(pelis["Rate"][i]) -float(statsr[2])) <= 1:
                    rating += 3
                elif abs(float(pelis["Rate"][i]) -float(statsr[2])) >= 2.5:
                    rating -= 3
            except:
                error=1 
            
            contadour=5
            for matices in ['Nudity','Violence','Profanity','Frightening']:
                try: 
                    if statsr[contadour] == pelis[matices][i]:# se calcula si tiene las mismas especificaciones en 4 areas diferentes
                        rating += 1.5
                except:
                    error=1
                contadour +=1
            
            try:
                if int(pelis["Certificate"][i]) == statsr[4]: # suma tambien si tiene el mismo rating de edad
                    rating += 8 # esto posee bastante peso para no ver una pelicula para una audiencia adulta tras una película infantil, ni viceversa
            except:
                a=0
            if pelis["Name"][i]==statsr[0]:
                rating=0.1
            else:
                rating = rating/0.27 - 8.35
            new =[rating,pelis["Name"][i]]
            if new[1] in [top[0][1],top[1][1],top[2][1]]:
                doubled=0
            else:
                if new[0] > top[0][0]:
                    top=[new,top[0],top[1]]
                elif new[0] > top[1][0]:
                    top[2],top[1]=top[1],new
                elif new[0] > top[2][0]:
                    top[2]=new
            
    # GENRE Para empezar ha de ser del mismo genero, hay varias palabras clave, si encaja más de una suma 6
    # RATE se suma 5 si (abs(rateR-rateN))<1 se resta 5 si (abs(rateR-rateN))>2.5
    # CERTIFICATE si es igual suma 5 pts
    # NUDITY, VIOLENCE, PROFANITY, FRIGHTENINGsuma 3 por cada parámetro igual
    for w in range(0,3):
        statsr=[]
        for j in range(0,6176):
            if (pelis['Name'][j]==top[w][1]):
                for category in ['Name','Date','Rate','Genre','Certificate','Nudity','Violence','Profanity','Frightening']:
                    a = pelis[category][j]
                    statsr.append(a)
    return top

def show(anterior,top):
    print(f'Habiendo visto {anterior}, el recomendador piensa que te gustará:') # 3 recomendaciones
    for rank in top: # imprime las 3 peliculas que más se aproximan a la que acabas de ver
        print(f'- {rank[1]}')
    x=int(input("Quieres buscar otra película?: (1=Sí , 0 = No) ")) # ver si quieren otra pelicula o no
    if x == 0:                                                      # si no quiere se acaba el bucle
        print('Gracias por usar el recomendador, hasta la próxima')
        return True
    return False

if __name__ == "__main__": 
    pelis=leerfichero() #importamos las películas
    ex = False # no sale del bucle hasta que lo digas dentro de la terminal
    while ex == False:
        anterior = moviename() #se recoje nombre y comprueba que esté en el dataset
        top = recomendar(anterior,pelis) # recomendador, ponderando las diferentes categorías
        ex = show (anterior,top) # muestra los resultados y permite salir del programa o repetir
    