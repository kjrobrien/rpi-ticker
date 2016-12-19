import os, sys, json, threading, time
from config import *
import matrix, webserver, pricesapi, marketclose

def readTickers():
	# load tickers from tickerFile
	try:
		# create full path for tickerFile
		tickerFile = os.path.join(sys.path[0], CONFIG["tickerFile"])
		if CONFIG["debug"]:
			print(tickerFile)
		# Load json file
		with open(tickerFile) as file:
			tickers = json.load(file)
	except FileNotFoundError:
		# if tickerFile not found, intialize with empty list
		tickers = []
	return tickers

if __name__ == "__main__":
	modules = {} # keep track of api, webserver, matrix
	# set up api for prices, make sure it has updated before continuing
	api = pricesapi.TradeKing(readTickers(), modules)
	api.initUpdate()
	server = webserver.webServer(modules)
	ledMatrix = matrix.RunTicker(modules)
	# proper terminal parameters not given
	if (not ledMatrix.process()):
		ledMatrix.print_help()
		sys.exit(1)

	modules.update({"api" : api, "webserver" : server, "matrix" : ledMatrix})


	try:
		threads = {}
		for key, value in modules.items():
			threads[key] = threading.Thread(target=value.run)
			threads[key].daemon = True
		for key, value in threads.items():
			threads[key].start()
		for key, value in threads.items():
			threads[key].join()

	# Handle exiting the program
	except (KeyboardInterrupt, SystemExit):
		print("Exiting\n")
		sys.exit(0)
