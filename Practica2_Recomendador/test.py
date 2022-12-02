import pandas
import re
trai = False

def leerfichero():  # leer el fichero csv
    pelis=pandas.read_csv('imdb.csv',sep=',')
    pelis.columns=['Name','Date','Rate','Votes','Genre','Duration','Type','Certificate','Episodes','Nudity','Violence','Profanity','Alcohol','Frightening']
    pelis=pelis[['Name','Date','Rate','Genre','Certificate','Nudity','Violence','Profanity','Frightening']]
    return pelis # devuelve el dataframe eliminando algunas columnas que no vamos a utilizar


def Search_names(Name):
    global trai
    # Search for opening bracket in the name followed by
    # any characters repeated any number of times
    if re.search(str(find), Name):
        trai = True
    return Name
  

if __name__ == "__main__":
    pelis = leerfichero()
    print(pelis.head())
    find = input('Nombre de la película: ')
    pelis['Name'] = pelis['Name'].apply(Search_names)
        