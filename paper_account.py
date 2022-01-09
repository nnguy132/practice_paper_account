import yfinance as yf
import stock as st

class paper_account:

    def __init__(self, account_name, balance):
        self.name = account_name
        self.balance = balance
        self.stocks = {}



    def calculate_stock_worth(self):
        #Initialize stock names, quantity and total asset price
        assets = 0

        #Pull ticker info
        tickers = yf.Tickers(list(self.stocks.keys()))

        #Sum up assets
        for stock in self.stocks:
            assets += tickers.tickers[stock].info["regularMarketPrice"] * int(self.stocks.get(stock).quantity)
        return assets



    def buy(self, stock, quantity):
        #Pull ticker info
        ticker = yf.Ticker(stock)
        price = ticker.info["regularMarketPrice"]


        #Check for pre-existing stock
        is_in_list = False

        for stocks in self.stocks:
            if stock == stocks:
                self.stocks[stocks].add_position(price, quantity)
                is_in_list = True

        #If it is not in the list append
        if not is_in_list:
            self.stocks[stock] = st.stock(price, quantity)

        #Take money
        self.balance -= price * quantity



    def sell(self, stock, quantity):
        #Pull ticker info
        ticker = yf.Ticker(stock)
        price = ticker.info["regularMarketPrice"]

        #Loop through stock list
        for stocks in self.stocks:
            if stock == stocks:
                if self.stocks[stocks].quantity > quantity:
                    self.stocks[stocks].remove_position(quantity)
                elif self.stocks[stocks].quantity == quantity:
                    self.stocks.pop(stock)
                    break
                else:
                    print("Oversold")

        #Give money
        self.balance += price * quantity



    def __repr__(self):
        assets = self.calculate_stock_worth()
        quantity = []
        stocks = list(self.stocks.keys())
        for stock in self.stocks:
            quantity.append(self.stocks.get(stock).quantity)
        return 'Account %s has: $%s \nis worth $%s \nand is invested in %s \nat %s quantity' % (self.name, self.balance, assets, stocks, quantity)
