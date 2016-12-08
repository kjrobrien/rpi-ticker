from config import *
import time

class TickerPricesAPI():
	def __init__(self, symbols):
		self.symbols = symbols
		self.prices = []
		self.pricesUpdating = []

	def updatePrices(self):
		pass

	def clearPrices(self):
		self.pricesUpdating = []

	def syncPrices(self):
		self.prices = self.pricesUpdating

	def updatePrice(self, price):
		self.pricesUpdating.append(price)

	def update(self):
		if CONFIG["debug"]:
			print("Updating Prices")
		self.clearPrices()
		self.updatePrices()
		if CONFIG["debug"]:
			print(self.pricesUpdating)
		self.syncPrices()

	def timedUpdate(self):
		while True:
			self.update()
			time.sleep(CONFIG["refresh"])

	def latestPrices(self):
		return self.prices

	def webMessage(self):
		return ''
