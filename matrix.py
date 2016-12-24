#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time, os, sys, collections
from config import *

class RunTicker(SampleBase):
	def __init__(self, modules, *args, **kwargs):
		super(RunTicker, self).__init__(*args, **kwargs)
		self.modules = modules

	def run(self):
		self.api = self.modules["api"]
		offscreenCanvas = self.matrix.CreateFrameCanvas()
		font = graphics.Font()
		font.LoadFont(os.path.join(sys.path[0], CONFIG["fontFile"]))
		pos = offscreenCanvas.width
		self.runText(font)

	def runText(self, font):
		canvas = self.matrix.CreateFrameCanvas()
		pos = canvas.width
		combos = collections.OrderedDict()
		combos.update(self.api.latestPrices())
		while self.modules["keepRunning"]:
			canvas = self.matrix.SwapOnVSync(canvas)
			canvas.Clear()
			if self.modules["pwrSwitch"]:
				if self.api.tickersChanged:
					self.api.tickersChanged = False
					pos = 0
					combos.clear()
					combos.update(self.api.latestPrices())
				updatedCombos = collections.OrderedDict()
				updatedOffscreen = collections.OrderedDict()
				offset = 0
				len = 0
				trimmedPos = 0
				for key, value in combos.items():
					len1 = graphics.DrawText(canvas, font, pos + offset,
						self.matrix.height/2 - 1, value.color, value.firstLine)
					len2 = graphics.DrawText(canvas, font, pos + offset,
						self.matrix.height - 1, value.color, value.secondLine)
					max_length = max(len1, len2)
					if (pos + max_length + offset == 0):
						new_combo = self.api.latestPrices()[key]
						updatedOffscreen[key] = new_combo
						trimmedPos += max_length
					else:
						updatedCombos[key] = value
					len = len + max_length
					offset = offset + max_length
				pos -= 1
				pos += trimmedPos
				combos.clear()
				combos.update(updatedCombos)
				combos.update(updatedOffscreen)
				time.sleep(CONFIG["scrollDelay"])
