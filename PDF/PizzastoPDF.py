from fpdf import FPDF
import pandas as pd
import matplotlib.pyplot as plt   

def topdf():
    pdf = FPDF()
    
    # página 1, título, imagen de pizzas, encuadre
    pdf.add_page()
    pdf.set_font('Arial',size=30)
    pdf.cell(200,80,txt='Executive report: Pizzas 2016',ln = 1, align='C')
    pdf.set_font('Arial',size=15)
    pdf.rect(5.0, 5.0, 200.0,287.0) # encuadre bonito
    pdf.rect(8.0, 8.0, 194.0,282.0)
    pdf.image('pizza.jpg',x=30,y=120,w=155,h=135)

    # página 2, pizzas con sus ingredientes : 
    pdf.add_page()
    data = pd.read_csv('Shoppinglist(week)2016.csv')
    ingredientes = list(data['Ingredient'])
    quantity = list(data['Quantity_for_n_pizzas'])
    pdf.rect(5.0, 5.0, 200.0,287.0) # encuadre bonito
    pdf.rect(8.0, 8.0, 194.0,282.0)
    pdf.set_font('Arial',size=30)
    pdf.cell(200,15,txt='',ln = 1, align='C')
    pdf.cell(200,30,txt='Available pizzas',ln = 1, align='C')
    pdf.set_font('Arial',size=19)
    pdf.cell(200,20,txt='(Ingredients included)',ln = 1, align='C')
    # insert the texts in pdf
    pdf.set_font('Arial',size=10)
    f = open("menu.txt", "r")
    for x in f:
        pdf.cell(190, 6, txt = x, ln = 1, align = 'C')
    
    
    # las page with the final report
    pdf.add_page()
    pdf.rect(5.0, 5.0, 200.0,287.0) # encuadre bonito
    pdf.rect(8.0, 8.0, 194.0,282.0)
    pdf.set_font('Arial',size=30)
   
    pdf.cell(200,60,txt='Weekly Shopping List 2016',ln = 1, align='C')
    f = plt.figure(figsize=(7, 30))
    plt.barh(ingredientes,quantity)
    plt.yticks(fontsize= 10)
    f.savefig('baringredients.jpg', bbox_inches='tight')
    pdf.image('baringredients.jpg',x=18,y=60,w=170,h=200)

    pdf.output('Pizza_report.pdf') # Pdf de destino

def createmenu(): # coloca las pizzas y sus ingredientes como texto para obtener una especie de menú
    raw= pd.read_csv('pizza_types.csv')
    raw = raw.drop(columns=['pizza_type_id','category'])
    menu = ''
    for i in range(2,len(raw['ingredients'])):
        name = raw['name'][i]
        name = name.split(' ')
        name.pop(0)
        name.pop(-1)
        rname = ''
        for j in name:
            rname += j + ' '
        rname += ':'
        ingr = raw['ingredients'][i]
        menu += rname + ' ' + ingr +'\n'
    menu= menu.replace('�','')
    with open('menu.txt', 'w') as f:
        for row in menu:
            f.write(row)

if __name__ == "__main__":
    createmenu() # convertir el csv de pizzas e ingredientes en un fichero que podamos leer más adelante
    topdf()     # creación completa del pdf