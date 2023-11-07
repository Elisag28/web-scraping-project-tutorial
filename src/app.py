import requests
import pandas as pd
import numpy as np
import time
from bs4 import BeautifulSoup as bs 
import io
import sqlite3
import matplotlib.pyplot as plt

#Sorce
web = ('https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue')
headers =  {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
data_ = requests.get(web, time.sleep(10), headers = headers)

#To text

data_string = io.StringIO(data_.text)
#table_ = pd.read_html(data_string)[0] not necessary
table_2 = pd.read_html(data_string)[1]
#annual_rev = pd.DataFrame(table_) not necessary
quarterly_rev = pd.DataFrame(table_2)
tesla_quarterly = quarterly_rev.rename(columns= {'Tesla Quarterly Revenue (Millions of US $)' : 'Date','Tesla Quarterly Revenue (Millions of US $).1' : 'Revenue'})

#Cleaning the data

tesla_quarterly = tesla_quarterly[tesla_quarterly['Revenue'].notna()]
tesla_quarterly['Revenue'] = tesla_quarterly['Revenue'].apply(lambda x: x.replace("$", ""))
tesla_quarterly['Revenue'] = tesla_quarterly['Revenue'].apply(lambda x: x.replace(",", ""))

#Store the data in SQL

conn = sqlite3.connect("Tesla_revenue.db")
cur = conn.cursor()
cur.execute("""CREATE TABLE Revenue (Date, Revenue)""")

#Transform to list to store in the data base

tesla_sql = tesla_quarterly.to_numpy().tolist()
tesla_sql[:2]

#Insert the data
cur.executemany("INSERT INTO revenue VALUES (?,?)", tesla_sql)
conn.commit()

#Checking if is OK
for row in cur.execute("SELECT * FROM Revenue"):
    print(row)

#Data visualization

x = tesla_quarterly['Date']
y = tesla_quarterly['Revenue']
plt.figure(figsize = (10, 5))
plt.plot(x, y)
plt.title('Yearly Revenue')
plt.show()

monthly_revenue = tesla_quarterly.groupby(tesla_quarterly.Date.dt.month)['Revenue'].sum()
monthly_revenue.plot.pie(figsize=(10, 5))
plt.title('Quarterly revenue')
plt.show

yearly_revenue = tesla_quarterly.groupby(tesla_quarterly.Date.dt.year)['Revenue'].sum()
yearly_revenue.plot.pie(figsize=(10, 7))
plt.title('Yearly revenue')
plt.show

monthly_revenue.plot.line(y=['Date'], figsize=(10,6))
plt.title('Monthly revenue')
plt.show()