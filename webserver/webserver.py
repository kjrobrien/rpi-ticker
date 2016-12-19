from flask import Flask, render_template, request, Markup
from config import *
import json
import os

class webServer():
	def __init__(self, modules):
		self.app = Flask(__name__)
		self.modules = modules
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
				self.modules["api"].symbols = tickers.split(',')
				self.modules["api"].update()
				with open(CONFIG["tickerFile"], 'w') as tickerFile:
					json.dump(self.modules["api"].symbols, tickerFile)
			tickers = ','.join(self.modules["api"].symbols)
			apimsg = Markup(self.modules["api"].webMessage())
			return render_template('index.html', tickers=tickers, updated=updated, apimsg=apimsg)
		@self.app.route("/kill")
		def kill():
			os._exit(0)
