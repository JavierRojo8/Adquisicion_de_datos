import csv
import pandas as pd
npizzas={"bbq_ckn":0,"cali_ckn":0,"ckn_alfredo":0,"ckn_pesto":0,"southw_ckn":0,"thai_ckn":0,"big_meat":0,"classic_dlx":0,"hawaiian":0,"ital_cpcllo":0,"napolitana":0,"pep_msh_pep":0,"pepperoni":0,"the_greek":0,"brie_carre":0,"calabrese":0,"ital_supr":0,"peppr_salami":0,"prsc_argla":0,"sicilian":0,"soppressata":0,"spicy_ital":0,"spinach_supr":0,"five_cheese":0,"four_cheese":0,"green_garden":0,"ital_veggie":0,"mediterraneo":0,"mexicana":0,"spin_pesto":0,"spinach_fet":0,"veggie_veg":0}
sizetorations={"s":0.6,"m":1.0,"l":1.4,"xl":1.8,"xxl":2.1}

def limpiar_orders():# limpiamos el orders.csv, del cual no nos importa la hora
    df = pd.read_csv('orders.csv')
    df.columns=[ 'order_id', 'date', 'time']
    df_orders=df[['date','order_id']]
    df_orders = df_orders.set_index('order_id')
    return df_orders

def limpiar_od(): # limpiar order details, del cual no necesitamos el order details
    df = pd.read_csv('order_details.csv')
    df.columns = ['order_details_id', 'order_id', 'pizza_id', 'quantity']
    df_orderdetails=df[['order_id', 'pizza_id', 'quantity']]
    df_orderdetails['quantity'] = df_orderdetails['quantity'].astype('string')
    df_orderdetails['quantity'] = df_orderdetails['quantity'][0]
    df_orderdetails = df_orderdetails.set_index('order_id')
    return df_orderdetails

def limpiar_pizza_types(): # limpiar pizza tipes, del cual solo necesitamos el nombre y los ingredientes
    df = pd.read_csv('pizza_types.csv')
    df.columns = ['pizza_type_id', 'name', 'category', 'ingredients']
    df_pizza_types = df[['pizza_type_id', 'ingredients']]
    return df_pizza_types

def clean():# limpiamos los da  taframes de todo lo que no queramos
    df_orders = limpiar_orders()
    df_oderdetails = limpiar_od()
    df_pizza_types = limpiar_pizza_types()
    return df_orders,df_oderdetails,df_pizza_types

def tipodepizza(x): # el tipo de pizza es el principio de la cadena de texto
    pizzalist=x.split("_")
    pizza = "" 
    for i in range (0,len(pizzalist)-1):
        pizza += pizzalist[i]
        if i < len(pizzalist)-2:
            pizza += "_"
    return pizza
    
def tamañopizza(x): # el tamño es el final de la cadena de texto
    pizza = x.split("_")
    return pizza[-1]


def contar(x):
    global npizzas, sizetorations
    pizzalist=x.split("_")
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

def unirdatos(df_orders,df_oderdetails):
    # Usando el id del pedido, se juntan los dataframes de la fecha y las pizzas pedidas
    df_juntos = pd.merge(df_orders, df_oderdetails, how= "outer",left_index= True, right_index=True)

    # transformamos pizza_id en el nombre de la pizza y la talla: five_cheese_l --> five_cheese, L
    auxiliar = pd.DataFrame([{"ration":1.0,"aux":0}]) # se añaden una columnas vacia de apoyo
    df_juntos = pd.merge(df_juntos, auxiliar, how= "outer",left_index= True, right_index=True)
    df_juntos = df_juntos.drop([0],axis=0) # se borra un error de unión que creaba una fila inicial
    return df_juntos

def operar(df_juntos):
    # se descompone la columna de tipo y tamaño en dos
    df_juntos ["ration"] = df_juntos["pizza_id"]+"_"+df_juntos['quantity']
    df_juntos ["aux"] = df_juntos ["ration"].apply(contar) # se cuenta el numero de pizzas totales diviediendo el ration
    return None

def pizzatoingredient(npizzas,df_pizzatoingredients):
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
    # como son datos de todo un año, la media diaria es dividir entre 365 y multiplicar por 7
    for i in ningredients:
        ningredients[i] = int((ningredients[i]/365)*7)
    ingr = []
    for i in ningredients:
        one = {'Ingredient':i,'Quantity_for_n_pizzas':ningredients[i]}
        ingr.append(one)
    with open('Shoppinglist(week)2015.csv', 'w',encoding="utf-8") as csvfile: 
        writer = csv.DictWriter(csvfile, fieldnames = ['Ingredient','Quantity_for_n_pizzas']) 
        writer.writeheader() 
        writer.writerows(ingr) 
    
    


if __name__ == "__main__":
    # se limpian los csvs
    df_orders,df_oderdetails,df_pizza_types = clean()
    print()
    # se juntan para una mayor facilidad de operación
    df_juntos = unirdatos(df_orders,df_oderdetails)
    print()
    # se opera sobre el dataset completo
    operar(df_juntos)
    # obteniendo los ingredientes totales
    ningredients = pizzatoingredient(npizzas,df_pizza_types)
    createcsv(ningredients)

"""
Informe de calidad de los datos, reflejando la tipología de cada columna y el numero de NaN y Null por cada columna:
        No se dispone de ningún NaN ni ningun Null en todo el dataset, por lo cual está muy limpio y podemos usar todos los datos
ETL para transformar los datos en función de los requerimientos decididos por cada uno a la hora de realizar data wrangling, si es necesario
        Con la función "clean" eliminamos columnas innecesarias, como la hora del pedido y juntamos los diferentes csvs para trabajar sobre uno solo con la funcion "unirdatos"
ETL que saque como output un csv con la compra semanal de ingredientes
"""