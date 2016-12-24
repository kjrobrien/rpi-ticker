from requests import Session
from requests_oauthlib import OAuth1
from config import *
from price import Price
from .tickerpricesapi import TickerPricesAPI


class TradeKing(TickerPricesAPI):

	def __init__(self, symbols, modules):
		super(TradeKing, self).__init__(symbols, modules)
		self.url = "https://api.tradeking.com/v1/market/ext/quotes.json"

	def updatePrices(self):
		if len(self.symbols) < 1:
			return
		params = dict(symbols=','.join(self.symbols))
		c = CONFIG["TradeKing"]
		r = Session()
		r.auth = OAuth1(c["CONSUMER_KEY"], c["CONSUMER_SECRET"],
				c["OAUTH_TOKEN"], c["OAUTH_SECRET"])
		try:
			r = r.get(self.url, params=params)
		except Exception:
			return False
		if CONFIG["debug"]:
			print(self.symbols)
			print(params)
		try:
			prices = r.json()["response"]["quotes"]["quote"]
		except Exception:
			return False
		if len(self.symbols) == 1:
			prices = [prices]


		for price in prices:
			ticker = price["symbol"]

			sign = price["chg_sign"]

			percent = price["pchg"]
			try:
				movement = '{:.2f}'.format(round(float(price["chg"]), 2))
				last_price = '{:.2f}'.format(round(float(price["last"]), 2))
			except ValueError:
				movement = price["chg"]
				last_price = price["last"]

			price_obj = Price(ticker, last_price, sign, movement, percent)
			self.updatePrice(price_obj)
		return True
	def webMessage(self):
		return 'Uses TradeKing for quotes. You can confirm the proper tickers at ' \
		'<a href="https://research.tradeking.com/research/markets/index.asp">their website</a>.'
