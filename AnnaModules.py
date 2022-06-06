import pandas as pd


#Create class for Stocks
class Stocks:
    def __init__(self, symbol, quantity, purchasePrice, currentPrice, purchaseDate):
        self.symbol = symbol
        self.quantity = quantity
        self.purchasePrice = purchasePrice
        self.currentPrice = currentPrice
        self.purchaseDate = purchaseDate

#Function to Calculate yeild/loss
    def calc_lossgain(self):
        lossGain = round(( (self.currentPrice) - (self.purchasePrice)) * (self.quantity),2)
        return lossGain
    
#Function to Calculate difference between today and purchase date
    def calc_dates(self):
        from datetime import datetime
        today = datetime.today()
        d2 = self.purchaseDate
        d_format = (datetime.strptime(d2, "%m/%d/%Y"))
        datecalc = ((today - d_format).days)
        return datecalc

#Function to Calculate yearly yield/loss percent
    def calc_yearpercent(self):
        yearPercent = round((((((self.currentPrice) - (self.purchasePrice)) / self.purchasePrice) / Stocks.calc_dates(self))) * 100, 2)
        return yearPercent
    
    def printStockReport(self):
        print(str(self.symbol) + "\t"*2 + str(self.quantity) + "\t"*2 + "$" +str(Stocks.calc_lossgain(self)) + "\t"*2 + "%" + str(Stocks.calc_yearpercent(self)))
        

#Function to print Stock Reports header
def printStockHeader():
    print("-" *120)
    print("Stock Ownership for Bob Smith")
    print("-"*120)
    print("Stock Symbol" + "\t" + "Quantity" + "\t" + "Earnings/Loss" + "\t" + "Yearly Gain/Loss Percentage")




#Make class for Bonds
class Bonds(Stocks): 
    def __init__(self, symbol, purchasePrice, currentPrice, quantity, purchaseDate, coupon, yields):
        super().__init__(symbol, purchasePrice, currentPrice, quantity, purchaseDate)
        self.coupon = coupon
        self.yields = yields
    
    def printBondReport(self):
        print(str(self.symbol) + "\t"*2 + str(self.quantity) + "\t"*3 + "$" + str(self.purchasePrice) + "\t"*3 + "$" + str(self.currentPrice) + "\t"*3 + (self.purchaseDate) + "\t"*2 + str(self.coupon) + "\t"*1 + "%" + str(self.yields))

def printBondHeader():
    print(" " *100)
    print("-" *120)
    print("Bond Ownership for Bob Smith")
    print("-"*120)
    print("Stock Symbol" + "\t" + "Quantity" + "\t" + "Purchase Price" + "\t" + "Current Price" + "\t" + "Purchase Date" + "\t" + "Coupon" + "\t" + "Yields")


#Make class for Investor 
class Investor:
    def __init__(self, investorID, name, address, phone):
        self.investorID = investorID
        self.name = name
        self.address = address
        self.phone = phone
        
#Function to print Investor line
    def printInvestor(self):
        print(" " *100)
        print("-" *120)
        print ("Investor Info for Bob Smith")
        print("-" *120)
        print ("Investor ID" + "\t"*2 + "Name" + "\t"*2 + "Address" + "\t"*5 + "Phone Number")
        print(str(self.investorID) + "\t"*3 + self.name + "\t"*1 + self.address + "\t"*1 + str(self.phone))
        print(" " *100)

# import data from lists to SQL database tables
def add_data(cur, stocks_list, bonds_list, bobSmith):
    print("-"*80)
    col = 0
    for stock in stocks_list:
        new_stock = "INSERT INTO stocks VALUES ('" + stock.symbol
        new_stock = new_stock + "',' " + str(stock.quantity) + "' "
        new_stock = new_stock + ",' " + str(stock.purchasePrice) + "' "
        new_stock = new_stock + ",' " + str(stock.currentPrice) + "' "
        new_stock = new_stock + ",' " + stock.purchaseDate + "' "
        new_stock = new_stock + ",' " + str(col) + " ');"
        print(new_stock)
        col = col + 1
        cur.execute(new_stock)

    for bond in bonds_list:
        new_bond = "INSERT INTO bonds VALUES (' " + bond.symbol
        new_bond = new_bond + "',' " + str(bond.quantity) + "' "
        new_bond = new_bond + ",' " + str(bond.purchasePrice) + "' "
        new_bond = new_bond + ",' " + str(bond.currentPrice) + "' "
        new_bond = new_bond + ",' " + bond.purchaseDate + "' "
        new_bond = new_bond + ",' " + str(bond.coupon) + "' "
        new_bond = new_bond + ",' " + str(bond.yields) + "' "
        new_bond = new_bond + ",' " + str(col) + "' );"
        print(new_bond)
        cur.execute(new_bond)

 
    new_inv = "INSERT INTO investor VALUES (' " + str(bobSmith.investorID)
    new_inv = new_inv  + "',' " + str(bobSmith.name) + "' "
    new_inv = new_inv + ",' " + str(bobSmith.address) + "' "
    new_inv = new_inv + ",' " + str(bobSmith.phone) + "' );"
    print(new_inv)
    cur.execute(new_inv)
    print("-"*80)


#Create class for JSON stocks to add to graph
class Graph:
    def __init__(self, symbol2, closingCost, date):
        self.symbol2 = symbol2
        self.closingCost = closingCost
        self.date = date
        self.stockDateList = []
        self.stockYList = []

    def add_axis(self, closingCost, date):
        self.stockYList.append(closingCost)
        self.stockDateList.append(date)

    def describe_stock(self):
        print("\n" + str(self.symbol2) + ":" + self.closingCost + "," + self.date)