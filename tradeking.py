from requests import Session
from requests_oauthlib import OAuth1
from config import *
from pricesapi import PricesAPI
from price import Price


class TradeKing(PricesAPI):

	def __init__(self, symbols):
		super(TradeKing, self).__init__(symbols)
		self.url = "https://api.tradeking.com/v1/market/ext/quotes.json"

	def updatePrices(self):
		params = dict(symbols=','.join(self.symbols))
		c = CONFIG["TradeKing"]
		r = Session()
		r.auth = OAuth1(c["CONSUMER_KEY"], c["CONSUMER_SECRET"],
				c["OAUTH_TOKEN"], c["OAUTH_SECRET"])
		r = r.get(self.url, params=params)
		prices = r.json()["response"]["quotes"]["quote"]

		for price in prices:
			ticker = price["symbol"]
			last_price = '{:.2f}'.format(round(float(price["last"]), 2))
			sign = price["chg_sign"]
			movement = '{:.2f}'.format(round(float(price["chg"]), 2))
			percent = price["pchg"]

			price_obj = Price(ticker, last_price, sign, movement, percent)
			self.updatePrice(price_obj)
