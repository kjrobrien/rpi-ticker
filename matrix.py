#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time, os, sys
from config import *

class RunTicker(SampleBase):
	def __init__(self, *args, **kwargs):
		super(RunTicker, self).__init__(*args, **kwargs)

	def Run(self, api):
		offscreenCanvas = self.matrix.CreateFrameCanvas()
		font = graphics.Font()
		font.LoadFont(os.path.join(sys.path[0], CONFIG["fontFile"]))
		pos = offscreenCanvas.width

		combos = api.latestPrices()

		while True:
			offscreenCanvas.Clear()
			offset = 0
			len = 0
			for combo in combos:
				len1 = graphics.DrawText(offscreenCanvas, font, pos + offset, self.matrix.height/2 - 1, combo.color, combo.firstLine)
				len2 = graphics.DrawText(offscreenCanvas, font, pos + offset, self.matrix.height - 1, combo.color, combo.secondLine)
				max_length = max(len1, len2)
				len = len + max_length
				offset = offset + max_length
			pos -= 1
			if (pos + len < 0):
				if CONFIG["debug"]:
					print("Reached end of matrix")
				pos = offscreenCanvas.width
				combos = api.latestPrices()

			time.sleep(CONFIG["scrollDelay"])
			offscreenCanvas = self.matrix.SwapOnVSync(offscreenCanvas)
