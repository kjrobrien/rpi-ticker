import os, sys, json, threading, time, multiprocessing
from config import *
import matrix, webserver, pricesapi
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(3, GPIO.IN, GPIO.PUD_UP)
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

def readSwitch(modules):
	while modules["keepRunning"]:
		if (modules["pwrSwitch"]) != (not GPIO.input(3)):
			modules["pwrSwitch"] = not GPIO.input(3)
			if CONFIG["debug"]:
				print("Switch: {}".format(modules["pwrSwitch"]))
		time.sleep(0.5)
	GPIO.cleanup()

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


	modules.update({"api" : api, "webserver" : server, "matrix" : ledMatrix, "pwrSwitch": False, "keepRunning" : True})




	try:
		threads = {}
		for key, value in {"matrix" : ledMatrix, "server" : server, "api" : api}.items():
			threads[key] = threading.Thread(target=value.run)
			threads[key].daemon = True
		GPIOthread = threading.Thread(target=readSwitch, args=(modules,))
		for key, value in threads.items():
			threads[key].start()
		GPIOthread.start()
		for key, value in threads.items():
			threads[key].join()
		GPIOthread.join()

	# Handle exiting the program
	except (KeyboardInterrupt, SystemExit):
		print("Exiting\n")
		modules["keepRunning"] = False
		sys.exit(0)
