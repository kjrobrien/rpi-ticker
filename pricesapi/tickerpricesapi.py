from config import *
import time, collections

class TickerPricesAPI():
	def __init__(self, symbols, modules):
		self.symbols = symbols
		self.prices = collections.OrderedDict() # The latest prices
		self.pricesUpdating = collections.OrderedDict() # List for prices while updating
		self.modules = modules
		self.hasUpdated = False # whether the prices have ever been updated
		self.tickersChanged = False # True when webserver changes tickers

	# to be defined in a child class
	def updatePrices(self):
		pass

	# clean pricesUpdating, to be called before updating the prices
	def clearPrices(self):
		self.pricesUpdating.clear()

	# update prices (our latest prices) with the updated prices. To be called
	# when done updating.
	def syncPrices(self):
		self.prices.clear()
		self.prices.update(self.pricesUpdating)

	# add the given price object (price) to our list of pricesUpdating
	def updatePrice(self, price):
		self.pricesUpdating[price.ticker] = price

	# updates all prices of given list symbols
	def update(self):
		if CONFIG["debug"]:
			print("Updating Prices")
		self.clearPrices()
		if self.updatePrices():
			self.hasUpdated = True
			self.syncPrices()
		if CONFIG["debug"]:
			print(self.pricesUpdating)

	# Updates prices every CONFIG["refresh"] seconds
	def timedUpdate(self):
		while self.modules["keepRunning"]:
			if self.modules["pwrSwitch"]:
				self.update()
				time.sleep(CONFIG["refresh"])

	# the latest up to date prices
	def latestPrices(self):
		return self.prices

	# Special message for the given pricesapi to be displayed on web page
	# i.e., where prices come from and how to confirm the syntax of the given
	# api's tickers
	def webMessage(self):
		return ''

	def run(self):
		self.timedUpdate()

	def initUpdate(self):
		self.update()
		while not self.hasUpdated:
			time.sleep(2) # wait 2 seconds before trying to update again
			self.update()
