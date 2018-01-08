#!/usr/bin/env python3

PRGM_AUTHOR = "Jonah Haney"
PRGM_VERSION = "2018.1.8"
DEBUG = False#True 

import sys

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

	def printf(self, *args, sep=" ", end="\n", file=sys.stdout, flush=False):
		return self

	def printANSI(self, C1, *args, ender="", seper=";", file=sys.stdout):
		"""Construct and Print an ANSI Escape Code"""
		if DEBUG:
			print("\n", C1, end="", sep="", file=sys.stderr)
			print(*args, end=ender, sep=seper, file=sys.stderr)
		else:
			print(ESC, C1, sep="", end="")
			if args:
				print(*args, end="", sep=seper, flush=True, file=file)
			print(end=ender)
		return self

	def printCS(self, code, *args, file=sys.stdout):
		"""Construct and Print a Control Sequence"""
		return self.printANSI(CSI, *args, ender=code, file=file)

	def printSGR(self, *args, file=sys.stdout):
		"""Construct and Print a Select Graphic Rendition Sequence"""
		return self.printCS(SGR, *args, file=file)

	def printOSC(self, *args, file=sys.stdout):
		"""Construct and Print an Operating System Command"""
		return self.printANSI(OSC, *args, file=file)

	def printRIS(self, file=sys.stdout):
		"""Reset the screen to its original state"""
		return self.printANSI(RIS, file=file)

	def reset(self, file=sys.stdout):
		"""Reset the screen to its original state"""
		return self.printRIS(file=file)

	def resetStyle(self, file=sys.stdout):
		"""Turn off all SGR attributes"""
		return self.printSGR(RSET, file=file)

	def clearToTop(self, file=sys.stdout):
		"""Clear the screen from cursor to top"""
		return self.printCS(ED, 1, file=file)

	def clearToBottom(self, file=sys.stdout):
		"""Clear the screen from cursor to bottom"""
		return self.printCS(ED, 0, file=file)

	def clear(self, file=sys.stdout):
		"""Clear the screen from top to bottom"""
		return self.printCS(ED, 2, file=file)

	def scrollUp(self, scroll = 1, file=sys.stdout):
		"""Scroll the screen up 'scroll' lines"""
		if scroll > 0:
			return self.printCS(SU, scroll, file=file)
		return self

	def scrollDown(self, scroll = 1, file=sys.stdout):
		"""Scroll the screen down 'scroll' lines"""
		if scroll > 0:
			return self.printCS(SD, scroll, file=file)
		return self

	def scroll(self, signed_scroll, file=sys.stdout):
		"""Scrolls down if 'signed_scroll' is positive, up if negative"""
		if signed_scroll < 0:
			return self.scrollUp(-signed_scroll, file=file)
		elif signed_scroll > 0:
			return self.scrollDown(signed_scroll, file=file)
		return self

	def moveCursorTo(self, new_cursor_x, new_cursor_y, file=sys.stdout):
		"""Move the cursor to the specified position"""
		if new_cursor_x > 0 and new_cursor_y > 0:
			return self.printCS(CUP, new_cursor_x, new_cursor_y, file=file)
		return self

	def moveCursorUp(self, n = 1, file=sys.stdout):
		"""Move the cursor up 'n' cells"""
		if n > 0:
			return nself.printCS(CUU, n, file=file)
		return self

	def moveCursorDown(self, n = 1, file=sys.stdout):
		"""Move the cursor down 'n' cells"""
		if n > 0:
			return self.printCS(CUD, n, file=file)
		return self

	def moveCursorLeft(self, n = 1, file=sys.stdout):
		"""Move the cursor left (back) 'n' cells"""
		if n > 0:
			return self.printCS(CUB, n, file=file)
		return self

	def moveCursorRight(self, n = 1, file=sys.stdout):
		"""Move the cursor right (forward) 'n' cells"""
		if n > 0:
			return self.printCS(CUF, n, file=file)
		return self

	def newLine(self, n = 1, file=sys.stdout):
		"""Move the cursor to beginning of 'n' lines down"""
		return self.printCS(CNL, n, file=file)

	def prevLine(self, n = 1, file=sys.stdout):
		"""Move the cursor to beginning of 'n' lines up"""
		return self.printCS(CPL, n, file=file)

	def setForeground(self, *args, file=sys.stdout):
		"""Set the text color. Use color code or R, G, B as arguments"""
		if len(args) == 3:
			return self.printSGR(FCLR, 2, *args, file=file)
		elif len(args) == 1:
			return self.printSGR(FCLR, 5, args[0], file=file)
		return self

	def setBackground(self, *args, file=sys.stdout):
		"""Set the background color. Use color code or R, G, B as arguments"""
		if len(args) == 3:
			return self.printSGR(BCLR, 2, *args, file=file)
		elif len(args) == 1:
			return self.printSGR(BCLR, 5, arg[0], file=file)
		return self

	def invertColors(self, file=sys.stdout):
		"""Set foreground color to background color, and vice-versa"""
		return self.printSGR(RVRS, file=file)

	def setBold(self, *args, file=sys.stdout):
		"""Set boldness: setBold() == setBold(True)"""
		if len(args) == 1:
			if args[0]:
				return self.printSGR(BOLD, file=file)
			return self.printSGR(BOLD_OFF, file=file)
		return self.printSGR(BOLD, file=file)

	def setUnderline(self, *args, file=sys.stdout):
		"""Set Underline: setUnderline() == setUnderline(True)"""
		if len(args) == 1:
			if args[0]:
				return self.printSGR(UNDL, file=file)
			return self.printSGR(UNDL_OFF, file=file)
		return self.printSGR(UNDL, file=file)

	def setBlink(self, *args, file=sys.stdout):
		"""Set Slow Blink: setBlink() == setBlink(True)"""
		if len(args) == 1:
			if args[0]:
				return self.printSGR(BLNK, file=file)
			return self.printSGR(BLNK_OFF, file=file)
		return self.printSGR(BLNK, file=file)

	def setFont(self, font_code, file=sys.stdout):
		"""Use alternative font, or reset to default"""
		if font_code > 0 and font_code < 10:
			return self.printSGR(FONT[font_code], file=file)
		return self.printSGR(DFNT, file=file)
	
	def resetFont(self, file=sys.stdout):
		"""Reset to default font"""
		return self.printSGR(DFNT, file=file)

	def saveCursorPosition(self, file=sys.stdout):
		"""Save current cursor position"""
		return self.printCS(SCP, file=file)

	def restoreCursorPosition(self, file=sys.stdout):
		"""Restore saved cursor position"""
		return self.printCS(RCP, file=file)

	def output(self, x, y, *args, end="", sep="", file=sys.stdout):
		"""Print *args at location x,y"""
		# self.printf("{SCP}{CUP,",x,",",y,"}{RCP}",*args, sep=sep, end=end, file=file)
		self.saveCursorPosition().moveCursorTo(x, y, file=file)
		print(*args, end=end, sep=sep, file=file)
		return self.restoreCursorPosition()
