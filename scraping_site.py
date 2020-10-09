import requests
import re
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode
print('connecting to db')
try:
  mydb = mysql.connector.connect(
    user="kilid",
    password='123',
    host="127.0.0.1",
    database="db1",
    charset='utf8'
)
  print('connected to db')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)

mycursor = mydb.cursor()
# Enforce UTF-8 for the connection.
mycursor.execute('SET NAMES utf8mb4')
mycursor.execute("SET CHARACTER SET utf8mb4")
mycursor.execute("SET character_set_connection=utf8mb4")
r = requests.get('https://divar.ir/s/tehran/laptop-notebook-macbook?price=10000000-20000000')
soup = BeautifulSoup(r.text, 'html.parser')
elements = soup.find_all('div',attrs={'class':'kt-post-card__body'})
for item in elements:
    laptop = item.find('div',attrs={'class':"kt-post-card__title"})
    price = item.find('div', attrs={'class': "kt-post-card__top-description kt-post-card-description"})
    mycursor.execute("""INSERT INTO divar (laptop, price) VALUES ('%s', '%s')""" % (laptop.text.strip(), price.text.strip()))
mydb.commit()
