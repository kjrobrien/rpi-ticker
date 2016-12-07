#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time

class FillWhite(SampleBase):
	def __init__(self, *args, **kwargs):
		super(FillWhite, self).__init__(*args, **kwargs)

	def Run(self):
		matrix = self.matrix
		matrix.Fill(255, 255, 255)
		while True:
			time.sleep(5)




# Main function
if __name__ == "__main__":
	parser = FillWhite()
	if (not parser.process()):
		parser.print_help()
