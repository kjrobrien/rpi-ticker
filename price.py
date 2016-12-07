from rgbmatrix import graphics

class Price():
	def __init__(self, ticker, price, sign, movement, percent):
		self.ticker = ticker
		self.price = price
		self.sign = sign
		self.movement = movement
		self.percent = percent
		self.color()
		self.chgSymbol()
		self.firstLine = self.ticker + " " + self.price + " "
		self.secondLine = self.chgSymbol + self.movement + " " + self.percent + "% "

	def chgSymbol(self):
		if(self.sign == "u"):
			self.chgSymbol = "▲"
		elif(self.sign == "d"):
			self.chgSymbol = "▼"
		else:
			self.chgSymbol = " "

	def color(self):
		if(self.sign == "u"):
			self.color = graphics.Color(0,255,0)
		elif(self.sign == "d"):
			self.color = graphics.Color(255,0,0)
		else:
			self.color = graphics.Color(0,0,255)

	def __repr__(self):
		return self.firstLine + self.secondLine
