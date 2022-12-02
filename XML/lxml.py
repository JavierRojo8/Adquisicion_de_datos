import csv

f_orders = csv.reader(open('orders.csv'))
f_datadictionary = csv.reader(open('data_dictionary.csv'))
f_order_details = csv.reader(open('order_details.csv'))
f_pizza_types = csv.reader(open('pizza_types.csv'))
f_pizzas = csv.reader(open('pizzas.csv'))
f_shoppinglist = csv.reader(open('Shoppinglist(week)2016.csv'))

data = []
todos = []
for row in f_orders:
  data.append(row)
todos.append(data[1])
(open('orders.csv')).close()
data = []
for row in f_datadictionary:
  data.append(row)
todos.append(data[1])
(open('data_dictionary.csv')).close()
data = []
for row in f_order_details:
  data.append(row)
todos.append(data[1])
(open('order_details.csv')).close()
data = []
for row in f_pizza_types:
  data.append(row)
todos.append(data[1])
(open('pizza_types.csv')).close()
data = []
for row in f_pizzas:
  data.append(row)
todos.append(data[1])
(open('pizzas.csv')).close()
data = []
for row in f_shoppinglist:
  data.append(row)
todos.append(data[2])
(open('Shoppinglist(week)2016.csv')).close()



def orders(row):
  return """<Orders>
  <atributo nombre = "Order_id">%s</atributo>
  <atributo nombre = "Date">%s</atributo>
  <atributo nombre = "Time">%s</atributo>
  </Orders>""" % (type(row[0]),type(row[1]),type(row[2]))

def datadict(row):
  return """<Dictionary>
  <atributo nombre = "Table">%s</atributo>
  <atributo nombre = "Field">%s</atributo>
  <atributo nombre = "Description">%s</atributo>
  </Dictionary>""" % (type(row[0]),type(row[1]),type(row[2]))

def order_details(row):
  return """<Order_detail>
  <atributo nombre = "order_details_id">%s</atributo>
  <atributo nombre = "order_id">%s</atributo>
  <atributo nombre = "pizza_id">%s</atributo>
  <atributo nombre = "quantity">%s</atributo>
  </Order_detail>""" % (type(row[0]),type(row[1]),type(row[2]),type(row[3]))

def pizza_types(row):
  return """<Pizza_type>
  <atributo nombre = "pizza_type_id">%s</atributo>
  <atributo nombre = "name">%s</atributo>
  <atributo nombre = "category">%s</atributo>
  <atributo nombre = "ingredients">%s</atributo>
  </Order_detail>""" % (type(row[0]),type(row[1]),type(row[2]),type(row[3]))

def pizzas(row):
  return """<Pizzas>
  <atributo nombre = "date">%s</atributo>
  <atributo nombre = "pizza_id">%s</atributo>
  <atributo nombre = "quantity">%s</atributo>
  <atributo nombre = "pizza_type_id">%s</atributo>
  <atributo nombre = "size">%s</atributo>
  <atributo nombre = "ration">%s</atributo>
  <atributo nombre = "totn">%s</atributo>
  </Order_detail>""" % (type(row[0]),type(row[1]),type(row[2]),type(row[3]),type(row[4]),type(row[5]),type(row[6]))

def shopping(row):
  return """<Pizza_type>
  <atributo nombre = "ingredient">%s</atributo>
  <atributo nombre = "Quantity_for_n_pizzas">%s</atributo>
  </Order_detail>""" % (type(row[0]),type(row[1]))


with open('ordersdata.xml','w') as f:
  f.write(orders(todos[0]))
  f.write('\n')
  f.write(datadict(todos[1]))
  f.write('\n')
  f.write(order_details(todos[2]))
  f.write('\n')
  f.write(pizza_types(todos[3]))
  f.write('\n')
  f.write(pizzas(todos[4]))
  f.write('\n')
  f.write(shopping(todos[5]))

