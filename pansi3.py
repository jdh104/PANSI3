#!/usr/bin/env python3

PRGM_AUTHOR = "Jonah Haney"
PRGM_VERSION = "2018.1.7"
DEBUG = False

ESC = "\033"
STX = "\02"

# Escape Sequences
CSI = "["  # Control Sequence Introducer
OSC = "]"  # Operating System Command
RIS = "c"  # Reset to Initial State

# Control Sequences
CUU = "A"  # Cursor Up
CUD = "B"  # Cursor Down
CUF = "C"  # Cursor Forward
CUB = "D"  # Cursor Back
CNL = "E"  # Cursor Next Line
CPL = "F"  # Cursor Previous Line
CHA = "G"  # Cursor Horizontal Absolute
CUP = "H"  # Cursor Position
ED  = "J"  # Erase in Display
EL  = "K"  # Erase in Line
SU  = "S"  # Scroll Up
SD  = "T"  # Scroll Down
SGR = "m"  # Select Graphic Rendition
SCP = "s"  # Save Cursor Position
RCP = "u"  # Restore Cursor Position

# SGR Codes
RSET = "0"      # All attributes off
BOLD = "1"      # Bold or increased intensity
BOLD_OFF = "22" # ^ off
UNDL = "4"      # Underline
UNDL_OFF = "24" # ^ off
BLNK = "5"      # Slow blink
BLNK_OFF = "25" # ^ off
RVRS = "7"      # Swap foreground and background
FONT = [str(i+10) for i in range(10)]
                # Alternate Fonts FONT[10-19]
DFNT = FONT[0]  # Default Font
FCLR = "38"     # Set foreground color
BCLR = "48"     # Set background color

class pansi:

	def printANSI(self, C1, *args, ender="", seper=";"):
		"""Construct and Print an ANSI Escape Code"""
		print(ESC, C1, sep="", end="")
		if args:
			print(*args, end="", sep=seper, flush=True)
		print(ender, end="")
		if DEBUG:
			print("\n", C1, *args, end=ender, sep=seper, file=sys.stderr)

	def printCS(self, code, *args):
		"""Construct and Print a Control Sequence"""
		self.printANSI(CSI, *args, ender=code)

	def printSGR(self, *args):
		"""Construct and Print a Select Graphic Rendition Sequence"""
		self.printCS(SGR, *args)

	def printOSC(self, *args):
		"""Construct and Print an Operating System Command"""
		self.printANSI(OSC, *args)

	def printRIS(self):
		"""Reset the screen to its original state"""
		self.printANSI(RIS)

	def resetAll(self):
		"""Reset the screen to its original state"""
		self.printRIS()

	def resetStyle(self):
		"""Turn off all SGR attributes"""
		self.printSGR(RSET)

	def clearToTop(self):
		"""Clear the screen from cursor to top"""
		self.printCS(ED, 0)

	def clearToBottom(self):
		"""Clear the screen from cursor to bottom"""
		self.printCS(ED, 1)

	def clear(self):
		"""Clear the screen from top to bottom"""
		self.printCS(ED, 2)

	def scrollUp(self, scroll = 1):
		"""Scroll the screen up 'scroll' lines"""
		if scroll > 0:
			self.printCS(SU, scroll)

	def scrollDown(self, scroll = 1):
		"""Scroll the screen down 'scroll' lines"""
		if scroll > 0:
			self.printCS(SD, scroll)

	def scroll(self, signed_scroll):
		"""Scrolls down if 'signed_scroll' is positive, up if negative"""
		if signed_scroll < 0:
			self.scrollUp(-signed_scroll)
		elif signed_scroll > 0:
			self.scrollDown(signed_scroll)

	def moveCursorTo(self, new_cursor_x, new_cursor_y):
		"""Move the cursor to the specified position"""
		if new_cursor_x > 0 and new_cursor_y > 0:
			self.printCS(CUP, new_cursor_x, new_cursor_y)

	def moveCursorUp(self, n = 1):
		"""Move the cursor up 'n' cells"""
		if n > 0:
			self.printCS(CUU, n)

	def moveCursorDown(self, n = 1):
		"""Move the cursor down 'n' cells"""
		if n > 0:
			self.printCS(CUD, n)

	def moveCursorLeft(self, n = 1):
		"""Move the cursor left (back) 'n' cells"""
		if n > 0:
			self.printCS(CUB, n)

	def moveCursorRight(self, n = 1):
		"""Move the cursor right (forward) 'n' cells"""
		if n > 0:
			self.printCS(CUF, n)

	def newLine(self, n = 1):
		"""Move the cursor to beginning of 'n' lines down"""
		self.printCS(CNL, n)

	def prevLine(self, n = 1):
		"""Move the cursor to beginning of 'n' lines up"""
		self.printCS(CPL, n)

	def setForeground(self, *args):
		"""Set the text color. Use color code or R, G, B as arguments"""
		if len(args) == 3:
			self.printSGR(FCLR, 2, *args)
		elif len(args) == 1:
			self.printSGR(FCLR, 5, args[0])

	def setBackground(self, *args):
		"""Set the background color. Use color code or R, G, B as arguments"""
		if len(args) == 3:
			self.printSGR(BCLR, 2, *args)
		elif len(args) == 1:
			self.printSGR(BCLR, 5, arg[0])

	def invertColors(self):
		"""Set foreground color to background color, and vice-versa"""
		self.printSGR(RVRS)

	def setBold(self, *args):
		"""Set boldness: setBold() == setBold(True)"""
		if len(args) == 1:
			if args[0]:
				self.printSGR(BOLD)
			else:
				self.printSGR(BOLD_OFF)
		else:
			self.printSGR(BOLD)

	def setUnderline(self, *args):
		"""Set Underline: setUnderline() == setUnderline(True)"""
		if len(args) == 1:
			if args[0]:
				self.printSGR(UNDL)
			else:
				self.printSGR(UNDL_OFF)
		else:
			self.printSGR(UNDL)

	def setBlink(self, *args):
		"""Set Slow Blink: setBlink() == setBlink(True)"""
		if len(args) == 1:
			if args[0]:
				self.printSGR(BLNK)
			else:
				self.printSGR(BLNK_OFF)
		else:
			self.printSGR(BLNK)
			
	def setFont(self, font_code):
		"""Use alternative font, or reset to default"""
		if font_code > 9 and font_code < 20:
			self.printSGR(FONT[font_code])
		else:
			self.printSGR(DFNT)
	
	def resetFont(self):
		"""Reset to default font"""
		self.printSGR(DFNT)

	def output(self, x, y, *args):
		"""Print *args at location x,y"""
		self.moveCursorTo(x, y)
		print(*args)

	def saveCursorPosition(self):
		"""Save current cursor position"""
		self.printCS(SCP)

	def restoreCursorPosition(self):
		"""Restore saved cursor position"""
		self.printCS(RCP)
