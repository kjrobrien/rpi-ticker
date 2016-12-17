import os, sys, json, threading, time
from config import *
import matrix, webserver, pricesapi

if __name__ == "__main__":

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

	# set up api for prices, make sure it has updated before continuing
	api = pricesapi.TradeKing(tickers)
	api.update()
	while not api.hasUpdated:
		time.sleep(2) # wait 2 seconds before trying to update again
		api.update()

	# set up the thread for updating prices
	apiThread = threading.Thread(target=api.timedUpdate)
	apiThread.daemon = True

	# set up the webserver for changing the tickers and create thread
	server = webserver.webServer(api)
	webThread = threading.Thread(target=server.run)
	webThread.daemon = True

	# set up the led matrix and its thread
	ledMatrix = matrix.RunTicker()
	# proper terminal parameters not given
	if (not ledMatrix.process()):
		ledMatrix.print_help()
		sys.exit(1)
	matrixThread = threading.Thread(target=ledMatrix.Run, args=(api,))
	matrixThread.daemon = True

	try:
		# start all threads
		apiThread.start()
		matrixThread.start()
		webThread.start()
		apiThread.join()
		matrixThread.join()
		webThread.join()
	# Handle exiting the program
	except (KeyboardInterrupt, SystemExit):
		print("Exiting\n")
		sys.exit(0)
