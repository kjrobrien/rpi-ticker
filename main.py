import matrix
import threading
import sys
import importlib
from config import *
from webserver import webServer
import pricesapi
import json



if __name__ == "__main__":
	# load tickers
	with open(CONFIG["tickerFile"]) as tickerFile:
		try:
			tickers = json.load(tickerFile)
		except Exception:
			tickers = []

	parser = matrix.RunTicker()
	if (not parser.process()):
		parser.print_help()
		sys.exit(1)

	api = pricesapi.TradeKing(tickers)
	server = webServer(api)

	apiThread = threading.Thread(target=api.timedUpdate)
	apiThread.daemon = True
	matrixThread = threading.Thread(target=parser.Run, args=(api,))
	matrixThread.daemon = True
	webThread = threading.Thread(target=server.run)
	webThread.daemon = True

	try:
		# Start loop
		print("Press CTRL-C to stop sample")
		apiThread.start()
		matrixThread.start()
		webThread.start()
		apiThread.join()
		matrixThread.join()
		webThread.join()

	except KeyboardInterrupt:
		print("Exiting\n")
		sys.exit(0)
