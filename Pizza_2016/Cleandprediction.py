import csv
import pandas as pd

npizzas={"bbq_ckn":0,"cali_ckn":0,"ckn_alfredo":0,"ckn_pesto":0,"southw_ckn":0,"thai_ckn":0,"big_meat":0,"classic_dlx":0,"hawaiian":0,"ital_cpcllo":0,"napolitana":0,"pep_msh_pep":0,"pepperoni":0,"the_greek":0,"brie_carre":0,"calabrese":0,"ital_supr":0,"peppr_salami":0,"prsc_argla":0,"sicilian":0,"soppressata":0,"spicy_ital":0,"spinach_supr":0,"five_cheese":0,"four_cheese":0,"green_garden":0,"ital_veggie":0,"mediterraneo":0,"mexicana":0,"spin_pesto":0,"spinach_fet":0,"veggie_veg":0}
sizetorations={"s":0.6,"m":1.0,"l":1.4,"xl":1.8,"xxl":2.1}

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

def pizzatoingredient(npizzas,df_pizzatoingredients): # el numero de ingredientes en base al numero de pizzas
    ingr={}
    for i in range(len(df_pizzatoingredients)):
        ingr[df_pizzatoingredients["pizza_type_id"][i]]=df_pizzatoingredients["ingredients"][i].split(",")
    total={}
    for j in npizzas:
        for k in range(len(ingr[j])):
            total[ingr[j][k]] =0
    for j in npizzas:
        for k in range(len(ingr[j])):
            total[ingr[j][k]] += npizzas[j]
    return total

def createcsv(ningredients):
    # como son datos diarios, para obtener la semana debemos multiplicar por 7
    for i in ningredients:
        ningredients[i] = int((ningredients[i])*7+0.6) # el más 0.6 es redondear hacia la unidad superior en caso de tener más de 4 décimas de ingrediente en la media
    ingr = []
    for i in ningredients:
        one = {'Ingredient':i,'Quantity_for_n_pizzas':ningredients[i]}
        ingr.append(one)
    with open('Shoppinglist(week)2016.csv', 'w',encoding="utf-8") as csvfile: 
        writer = csv.DictWriter(csvfile, fieldnames = ['Ingredient','Quantity_for_n_pizzas']) 
        writer.writeheader() 
        writer.writerows(ingr) 

def dividirycontar(df):
    global npizzas
    anual = []
    for day in df['date'].unique():
        npizzas={"bbq_ckn":0,"cali_ckn":0,"ckn_alfredo":0,"ckn_pesto":0,"southw_ckn":0,"thai_ckn":0,"big_meat":0,"classic_dlx":0,"hawaiian":0,"ital_cpcllo":0,"napolitana":0,"pep_msh_pep":0,"pepperoni":0,"the_greek":0,"brie_carre":0,"calabrese":0,"ital_supr":0,"peppr_salami":0,"prsc_argla":0,"sicilian":0,"soppressata":0,"spicy_ital":0,"spinach_supr":0,"five_cheese":0,"four_cheese":0,"green_garden":0,"ital_veggie":0,"mediterraneo":0,"mexicana":0,"spin_pesto":0,"spinach_fet":0,"veggie_veg":0}
        dfsito = df[df['date']==day] 
        dfsito['aux'] = dfsito['pizza_id'].apply(contar) # se cuenta el número total de ingredientes
        anual.append(npizzas)
    return anual
def limpiar_pizza_types(): # limpiar pizza tipes, del cual solo necesitamos el nombre y los ingredientes
    df = pd.read_csv('pizza_types.csv')
    df.columns = ['pizza_type_id', 'name', 'category', 'ingredients']
    df_pizza_types = df[['pizza_type_id', 'ingredients']]
    return df_pizza_types
 
def fechasiguales(x): # con ayuda de pandas se corrige el formato de las fechas
    try: 
        x = pd.to_datetime(float(x)+3600, unit='s').date()
    except:
        x = pd.to_datetime(x).date()
    return x

def anualtomedia(anual):
    media={"bbq_ckn":0,"cali_ckn":0,"ckn_alfredo":0,"ckn_pesto":0,"southw_ckn":0,"thai_ckn":0,"big_meat":0,"classic_dlx":0,"hawaiian":0,"ital_cpcllo":0,"napolitana":0,"pep_msh_pep":0,"pepperoni":0,"the_greek":0,"brie_carre":0,"calabrese":0,"ital_supr":0,"peppr_salami":0,"prsc_argla":0,"sicilian":0,"soppressata":0,"spicy_ital":0,"spinach_supr":0,"five_cheese":0,"four_cheese":0,"green_garden":0,"ital_veggie":0,"mediterraneo":0,"mexicana":0,"spin_pesto":0,"spinach_fet":0,"veggie_veg":0}
    for pizza in list(media.keys()):
        tot=0
        for dia in anual:
            tot += dia[pizza]
        media[pizza] = tot/365
    return media
    

if __name__ == "__main__":
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
    npizzasdiaria = anualtomedia(anual) # la media de pizzas diaria en base a 'anual'
    # obteniendo asi los ingredientes totales
    df_pizza_types = limpiar_pizza_types() # asociar pizzas a ingredientes
    ningredients = pizzatoingredient(npizzasdiaria,df_pizza_types)
    createcsv(ningredients) # se crea el csv con la compra necesaria para una semana en 2016