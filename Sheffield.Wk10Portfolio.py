"""
Anna Sheffield
Python Programming ICT 4370
June 5, 2022
Week 10: Portfolio Programming Assignment- Improving the Stock Problem with Additional Functionality
"""


#Import libraries and modules
from datetime import datetime
import pandas as pd
from AnnaModules import *
import sqlite3
import matplotlib
import matplotlib.pyplot as plt
import json
import pygal
import numpy

#Connect to database
conn = sqlite3.connect('BobStocksBonds.db')

#Create a cursor
cur = conn.cursor()

#Deletes tables if they existed
try:
	cur.execute(""" DROP TABLE stocks""")
	cur.execute(""" DROP TABLE bonds""")
	cur.execute(""" DROP TABLE investor""")
	print("Existing Tables tables have been deleted.")
except: print("Tables didn't exist.")


#Create new tables for Stocks, Bonds, and Investor info
stocks_table = """ CREATE TABLE IF NOT EXISTS stocks (
                                SYMBOL text PRIMARY KEY,
                                NO_SHARES integer NOT NULL,
                                PURCHASE_PRICE real NOT NULL,
                                CURRENT_VALUE real NOT NULL,
                                PURCHASE_DATE date NOT NULL,
                                STOCK_ID integer NOT NULL) """
bonds_table = """ CREATE TABLE IF NOT EXISTS bonds (
                                SYMBOL text PRIMARY KEY,
                                NO_SHARES integer NOT NULL,
                                PURCHASE_PRICE real NOT NULL,
                                CURRENT_VALUE real NOT NULL,
                                PURCHASE_DATE date NOT NULL,
                                Coupon real NOT NULL,
                                Yield real NOT NULL,
                                BOND_ID integer NOT NULL) """
investor_table = """ CREATE TABLE IF NOT EXISTS investor ( 
								investorID integer PRIMARY KEY,
								name integer NOT NULL,
                                address text NOT NULL,
                                phone text NOT NULL) """    

#Set up exceptions                                                            
try:
	cur.execute(stocks_table)
	cur.execute(bonds_table)
	cur.execute(investor_table)
	print("Tables have been created.")
except: print("Tables failed to be created.")


#Setup empty lists, import needed files with pandas
stocks_list = []
bonds_list = []

dfStocks = pd.read_csv('C:/Users/ashef/Downloads/Lesson6_Data_Stocks.csv')
dfStocksSorted = (dfStocks.sort_values(by=['SYMBOL'], ignore_index=True))
dfBonds = pd.read_csv('C:/Users/ashef/Downloads/Lesson6_Data_Bonds.csv')
dfJSONstocks = pd.read_json('C:/sqlite/AllStocks.json')

try:
    dfStocksSorted
    dfBonds
    dfJSONstocks
except: FileNotFoundError

#Function to Load stocks from CSV into list
def load_stocks():
    col1 = 0
    for StocksInd in dfStocks.index:
        stockVal = dfStocks.values[col1]
        stocks_list.append(Stocks(stockVal[0],stockVal[1], stockVal[2], stockVal[3],stockVal[4]))
        col1 = col1 + 1
    return(stocks_list)
load_stocks()

#Function to load Bonds from CSV file into list
def load_bonds():
    bondValue = dfBonds.values[0]
    bonds_list.append(Bonds(bondValue[0], bondValue[1], bondValue[2], bondValue[3], bondValue[4], bondValue[5], bondValue[6]))
    return(bonds_list)
load_bonds()

#Add Bob Smith as an Investor
bobSmith = (Investor(1234, "Bob Smith", "10 Main St., Denver CO", "555-555-555"))

#Print original reports
printStockHeader()
for obj in stocks_list:
    obj.printStockReport()

printBondHeader()
for obj in bonds_list:
    obj.printBondReport()

bobSmith.printInvestor()
print(" " *100)


#Call function that adds data to the tables
try:
	add_data(cur, stocks_list, bonds_list, bobSmith)
except: 
    print("Data not inserted into tables.")

#Commit and close connection
conn.commit()
conn.close()


#Open JSON file and create New Close values using Quanitity from previous list
QuantityList = dfStocksSorted['NO_SHARES'].values.tolist()

file_path = 'C:/sqlite/AllStocks.json'
with open(file_path) as json_file:
    data_set = json.load(json_file)
for jstock in data_set:
    if jstock['Symbol'] == 'AIG': jstock['New Close'] = round(QuantityList[0] * jstock['Close'], 2)
    elif jstock['Symbol'] == 'F': jstock['New Close'] = round(QuantityList[1] * jstock['Close'], 2)
    elif jstock['Symbol'] == 'FB': jstock['New Close'] = round(QuantityList[2] * jstock['Close'], 2)
    elif jstock['Symbol'] == 'GOOG': jstock['New Close'] = round(QuantityList[3] * jstock['Close'], 2)
    elif jstock['Symbol'] == 'IBM': jstock['New Close'] = round(QuantityList[4] * jstock['Close'], 2)
    elif jstock['Symbol'] == 'M': jstock['New Close'] = round(QuantityList[5] * jstock['Close'], 2)
    elif jstock['Symbol'] == 'MSFT': jstock['New Close'] = round(QuantityList[6] * jstock['Close'], 2)
    elif jstock['Symbol'] == 'RDS-A': jstock['New Close'] = round(QuantityList[7] * jstock['Close'], 2)


#Set up empty dictionary to add JSON stocks to after passing through classes to create objects
jDict = {}
for jstock in data_set:
    if jstock['Symbol'] not in jDict:
        newStock = Graph(jstock['Symbol'], jstock['New Close'], jstock['Date'])
        print(jstock['Symbol'] + " added")
        jDict[jstock['Symbol']] = newStock
    else:
        jDict[jstock['Symbol']].closingCost = jstock['New Close']

    jDict[jstock['Symbol']].add_axis(jstock['New Close'], datetime.strptime(jstock['Date'], '%d-%b-%y'))


#Plot the dictionary into a line graph
for jstock in jDict:
    closes = jDict[jstock].stockYList
    dates = matplotlib.dates.date2num(jDict[jstock].stockDateList)
    name = jDict[jstock].symbol2
    plt.plot_date(dates, closes, linestyle ='solid', marker ='None', label = name)
plt.legend()
plt.show()


#Setting up empty lists for bar graph data
list_1 = []
list_2 = []
list_3 = []
list_4 = []
list_5 = []
list_6 = []
list_7 = []
list_8 = []

bar_chart = pygal.HorizontalBar()
bar_chart.title = 'Number of Stocks purchased per Symbol'

for x in data_set:
    if x['Symbol'] == 'AIG': list_1.append(x['Symbol'])
    elif x['Symbol'] == 'F': list_2.append((x['Symbol']))
    elif x['Symbol'] == 'FB': list_3.append((x['Symbol']))
    elif x['Symbol'] == 'GOOG': list_4.append((x['Symbol']))
    elif x['Symbol'] == 'IBM': list_5.append((x['Symbol']))
    elif x['Symbol'] == 'M': list_6.append((x['Symbol']))
    elif x['Symbol'] == 'MSFT': list_7.append((x['Symbol']))
    elif x['Symbol'] == 'RDS-A': list_8.append((x['Symbol']))

#Setting points using the length of number of purchases for each symbol
bar_chart.add('AIG', len(list_1))
bar_chart.add('F', len(list_2))
bar_chart.add('FB', len(list_3))
bar_chart.add('GOOG', len(list_4))
bar_chart.add('IBM', len(list_5))
bar_chart.add('M', len(list_6))
bar_chart.add('MSFT', len(list_6))
bar_chart.add('RDS-A', len(list_7))

bar_chart.render_to_file('C:/sqlite/BarGraph2.svg')
bar_chart



