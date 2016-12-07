import matrix
from tradeking import TradeKing
import threading
import sys
from config import *
from webserver import webServer



if __name__ == "__main__":
	parser = matrix.RunTicker()
	if (not parser.process()):
		parser.print_help()
		sys.exit(1)
	tk = TradeKing(CONFIG["tickers"])
	server = webServer(tk)

	apiThread = threading.Thread(target=tk.timedUpdate)
	apiThread.daemon = True
	matrixThread = threading.Thread(target=parser.Run, args=(tk,))
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
