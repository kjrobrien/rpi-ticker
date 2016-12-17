from config import *
import time

class TickerPricesAPI():
	def __init__(self, symbols):
		self.symbols = symbols
		self.prices = [] # The latest prices
		self.pricesUpdating = [] # List for prices while updating
		self.hasUpdated = False # whether the prices have ever been updated

	# to be defined in a child class
	def updatePrices(self):
		pass

	# clean pricesUpdating, to be called before updating the prices
	def clearPrices(self):
		self.pricesUpdating = []

	# update prices (our latest prices) with the updated prices. To be called
	# when done updating.
	def syncPrices(self):
		self.prices = self.pricesUpdating

	# add the given price object (price) to our list of pricesUpdating
	def updatePrice(self, price):
		self.pricesUpdating.append(price)

	# updates all prices of given list symbols
	def update(self):
		if CONFIG["debug"]:
			print("Updating Prices")
		self.clearPrices()
		if self.updatePrices():
			self.hasUpdated = True
		if CONFIG["debug"]:
			print(self.pricesUpdating)
		self.syncPrices()

	# Updates prices every CONFIG["refresh"] seconds
	def timedUpdate(self):
		while True:
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
