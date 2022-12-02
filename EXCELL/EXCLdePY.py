from openpyxl import Workbook
import asposecells
import xlsxwriter
import pandas as pd
import matplotlib.pyplot as plt
import csv

npizzas={"bbq_ckn":0,"cali_ckn":0,"ckn_alfredo":0,"ckn_pesto":0,"southw_ckn":0,"thai_ckn":0,"big_meat":0,"classic_dlx":0,"hawaiian":0,"ital_cpcllo":0,"napolitana":0,"pep_msh_pep":0,"pepperoni":0,"the_greek":0,"brie_carre":0,"calabrese":0,"ital_supr":0,"peppr_salami":0,"prsc_argla":0,"sicilian":0,"soppressata":0,"spicy_ital":0,"spinach_supr":0,"five_cheese":0,"four_cheese":0,"green_garden":0,"ital_veggie":0,"mediterraneo":0,"mexicana":0,"spin_pesto":0,"spinach_fet":0,"veggie_veg":0}
sizetorations={"s":0.6,"m":1.0,"l":1.4,"xl":1.8,"xxl":2.1}



def cells(menu,diccionarios):
    wb = xlsxwriter.Workbook('Pizza_report.xlsx')
    bold = wb.add_format({'bold': True})
    pizzas=[]
    for p_and_i in menu:
        pizzas.append(p_and_i[0])
    letras = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','AA', 'AB', 'AC', 'AD', 'AE', 'AF']
    pizza_to_column ={}   
    for i in range(len(menu)):
        pizza_to_column[pizzas[i]]=letras[i]
    data = pd.read_csv('Shoppinglist(week)2016.csv')
    ingredientes = list(data['Ingredient'])
    quantity = list(data['Quantity_for_n_pizzas'])
    
    # Página 1 
    worksheet = wb.add_worksheet('Daily_orders')
    worksheet.write('B1','Quantity of pizzas of each flavour per day (decimals depend on the size of the pizza)')
    for i in range(3,len(diccionarios)+3): # eje y
        worksheet.write('A'+str(i), 'Day '+str(i-2),bold)
    for column in pizza_to_column.keys():     # eje x
        worksheet.write(pizza_to_column[column]+'2', column,bold)
    


    # Iterate over the data and write it out row by row.
    row = 2
    for day in (diccionarios):
        column = 1
        for pizza in day.keys():
            worksheet.write(row,column, day[pizza])
            column += 1
        row += 1

    # Página 2, 
    worksheet = wb.add_worksheet('Ingredients_per_pizza')
    
    
    # insert value in the cells
    
    ingrvalues={}

    # introducción al contenido de la tabla
    worksheet.write('A1', 'Ingredient report')
    worksheet.write('F1', 'Table with the ingredients of each pizza')

    # se hace la tabla haciendo los ejes y luego añadiendo x's donde coincidan los ingrendientes en la pizza
    for i in range(3,len(ingredientes)+3):
        ingrvalues[ingredientes[i-3]]=i
    ingrvalues['�Nduja Salami']=48 # corrección en caso de error por caracter especial
    
    for line in range(3,len(ingredientes)+3): # eje y
        worksheet.write('A'+str(line), ingredientes[line-3],bold)

    for column in pizza_to_column.keys():     # eje x
        worksheet.write(pizza_to_column[column]+'2', column,bold)

    for complete in menu:
        column = pizza_to_column[complete[0]]
        for single_ingredient in complete[1][0].split(','):
            worksheet.write(column+str(ingrvalues[single_ingredient]), 'X')

    # página 3
    worksheet = wb.add_worksheet('Prediction_report')
    # Write some data headers.
    worksheet.write('B2', 'Prediction report', bold)
    worksheet.write('A2', 'Ingredient', bold)
    worksheet.write('B2', 'Quantity*', bold)
    worksheet.write('C3', '*Quantity indicates how many rations of a medium pizza you need of each ingredient')
    lista_compra=[]
    for i in range (len(ingredientes)):
        lista_compra.append([ingredientes[i],quantity[i]])
    # Start from the first cell below the headers.
    row = 2
    col = 0

    # Iterate over the data and write it out row by row.
    for ingrs, quantyti in (lista_compra):
        worksheet.write(row, col,     ingrs)
        worksheet.write(row, col + 1, quantyti)
        row += 1

    
    f = plt.figure(figsize=(7, 30))
    plt.barh(ingredientes,quantity)
    plt.yticks(fontsize= 10)
    f.savefig('baringredients.jpg', bbox_inches='tight')
    worksheet.insert_image('E5', 'baringredients.jpg',{'x_offset': 6, 'y_offset': 30})  

    wb.close()
    pass

def createmenu(): # coloca las pizzas y sus ingredientes como texto para obtener una especie de menú
    raw= pd.read_csv('pizza_types.csv')
    raw = raw.drop(columns=['pizza_type_id','category'])
    menu = []
    for i in range(2,len(raw['ingredients'])):
        name = raw['name'][i]
        name = name.split(' ')
        name.pop(0)
        name.pop(-1)
        rname = ''
        for j in name:
            rname += j + ' '
        ingr = raw['ingredients'][i]
        ingr.replace('�','')
        menu.append([rname,[ingr]])
    return menu


def limpiar_orders():# limpiamos el orders.csv, del cual no nos importa la hora
    df = pd.read_csv('order_details.csv',sep=";")
    df.columns=['order_details_id','order_id','pizza_id','quantity']
    df_orders_details=df[['order_id','pizza_id','quantity']]
    df_orders_details = df_orders_details.set_index('order_id')
    return df_orders_details

def limpiar_fechas():
    df = pd.read_csv('orders.csv',sep = ';')
    df.columns = ['order_id','date','time']
    df_orders = df[['order_id','date']]
    df_orders = df_orders.set_index('order_id')
    return df_orders

def cleanquantity(x): # se limpian las imperfecciones al meter en número de pizzas
    ones = [1,-1,'NaN','Nan','nan','one','One','1','-1'] 
    twos = [2,-2,'2','-2','two','Two']
    threes = [3,-3,'3','-3','three','Three']
    fours = [4,-4,'4','-4','four','Four']
    if x in ones:
        return str(1)
    elif x in twos:
        return str(2)
    elif x in threes:
        return str(3)
    elif x in fours:
        return str(4)
    return str(1)

def cleansize(x): # para obtener el tamñano de la pizza deseada, es el último dígito si es cualquier cosa que no sea 'xl' ni 'xxl'
    x=str(x)
    if x[-2] == 'x':
        if x[-3] =='x':
            return 'xxl'
        return 'xl'
    return x[-1]

def cleantext(x):
    x = str(x).replace('@','a')
    x = str(x).replace('0','o')
    x = str(x).replace('3','e')
    separadores = ['-',' ','_']
    for divisor in separadores:
        if x.find(divisor) != -1:
            pizzalist = x.split(divisor)
            pizza = "" 
            for i in range (0,len(pizzalist)):
                pizza += pizzalist[i]
                if i < len(pizzalist)-1:
                    pizza += "_"
            return pizza
    return x

def order(df): # devuelve el dataframe con nombre_tamaño_cantidads
    auxiliar = pd.DataFrame([{"size":'NaN',"aux":'_'}]) # se añaden una columnas vacia de apoyo
    df = pd.merge(df, auxiliar, how= "outer",left_index= True, right_index=True)
    df['size']=df['pizza_id'].apply(cleansize) # obtener el size de la pizza
    df["pizza_id"]=df["pizza_id"].apply(cleantext) # limpiar el texto de fallos en la escritura
    df['pizza_id'] = df["pizza_id"]+'_'+df['quantity'] # finalmente nuestra pizza tiene el formato, nombre_tamaño_cantidad
    return df

def contar(x):  #contar el final
    global npizzas, sizetorations
    x= str(x)
    pizzalist=x.split("_")
    if pizzalist[0] == 'nan':
        return 0
    sabor = "" 
    for i in range (0,len(pizzalist)-2):
        sabor += pizzalist[i]
        if i < len(pizzalist)-3:
            sabor += "_"
    size = pizzalist[-2]
    cantidad = pizzalist[-1]
    proportion = sizetorations[size]
    npizzas[sabor] += float(proportion)*float(cantidad)
    return 0

def fechasiguales(x): # con ayuda de pandas se corrige el formato de las fechas
    try: 
        x = pd.to_datetime(float(x)+3600, unit='s').date()
    except:
        x = pd.to_datetime(x).date()
    return x

def dividirycontar(df):
    global npizzas
    anual = []
    for day in df['date'].unique():
        npizzas={"bbq_ckn":0,"cali_ckn":0,"ckn_alfredo":0,"ckn_pesto":0,"southw_ckn":0,"thai_ckn":0,"big_meat":0,"classic_dlx":0,"hawaiian":0,"ital_cpcllo":0,"napolitana":0,"pep_msh_pep":0,"pepperoni":0,"the_greek":0,"brie_carre":0,"calabrese":0,"ital_supr":0,"peppr_salami":0,"prsc_argla":0,"sicilian":0,"soppressata":0,"spicy_ital":0,"spinach_supr":0,"five_cheese":0,"four_cheese":0,"green_garden":0,"ital_veggie":0,"mediterraneo":0,"mexicana":0,"spin_pesto":0,"spinach_fet":0,"veggie_veg":0}
        dfsito = df[df['date']==day].copy()
        dfsito['aux'] = dfsito['pizza_id'].apply(contar) # se cuenta el número total de ingredientes
        anual.append(npizzas)
    return anual

def obtaindict():
    # de dos datasets obtener el numero de ingredientes para la próxima semana 
    df = limpiar_orders() # se descargan los orders
    dfo = limpiar_fechas() # se descargan las fechas
    dfo['date'] = dfo['date'].apply(fechasiguales) # se arreglan todas las fechas posibles
    df = pd.merge(df, dfo, how= "outer",left_index= True, right_index=True) # se juntan los dos csvs
    df['quantity'] = df['quantity'].apply(cleanquantity) # se limpia la cantidad 'orders'
    df = order(df) #se obtiene el order completo como pizza_tamaño_cantidad 
    df.drop('aux', inplace=True, axis=1) # se elimina la columna auxiliar
    df.dropna() # en este momento solo quedan los datos que no tienen las pizzas, es decir, inservibles
    anual = dividirycontar(df) # se obtiene el numero de pizzas por cada día del 2016
    return anual
if __name__ == '__main__':
    menu = createmenu()
    diccionarios = obtaindict()
    cells(menu,diccionarios)
    