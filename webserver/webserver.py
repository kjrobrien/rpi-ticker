from flask import Flask, render_template, request, Markup
from config import *
import json

class webServer():
	def __init__(self, api):
		self.app = Flask(__name__)
		self.api = api
		self.setup()

	def run(self):
		self.app.run('0.0.0.0', CONFIG["webPort"])

	def setup(self):

		@self.app.route("/", methods=['GET', 'POST'])
		def home():
			updated = False
			if request.method == 'POST':
				updated = True
				tickers = request.form['tickers'].upper()
				self.api.symbols = tickers.split(',')
				with open(CONFIG["tickerFile"], 'w') as tickerFile:
					json.dump(self.api.symbols, tickerFile)
			tickers = ','.join(self.api.symbols)
			apimsg = Markup(self.api.webMessage())
			return render_template('index.html', tickers=tickers, updated=updated, apimsg=apimsg)
