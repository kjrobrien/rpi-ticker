from flask import Flask


class webServer():
	def __init__(self, api):
		self.app = Flask(__name__)
		self.api = api
		self.setup()

	def run(self):
		self.app.run('0.0.0.0', 8080)

	def setup(self):

		@self.app.route("/")
		def hello():
			return "Hello World!"


		@self.app.route("/edit")
		def edit():
			return str(self.api.symbols)
