#!/usr/bin/env python3

import sys

__author__ = "Jonah Haney"
__version__ = "2018.1.7"

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
	def __init__(self, DEBUG=False):
		self.DEBUG = DEBUG

	def fstr(self, obj):
		"""Allow objects to define formatted strings as self-representation.

		To use this feature, give any class a __fstr__() method that returns a string compatible with pansi.printf().
		"""
		try:
			return obj.__fstr__()
		except:
			return str(obj)
				

	def printf(self, *args, sep=" ", end="\n", file=sys.stdout, flush=False):
		for arg in args:
			steps = []
			for s in arg.split("{"):
				steps.extend(s.split("}"))
			cmd_switch = False
			for s in steps:
				if cmd_switch:
					params = s.split(",")
					params[0] = params[0].upper()
					for i in range(len(params)-1):
						params[i+1] = int(params[i+1])
					if params[0] == "RIS" or params[0] == "RESET":
						self.printRIS()
					elif params[0] == "CUU":
						if len(params) > 1:
							self.move_cursor_up(n=params[1])
						else:
							self.move_cursor_up()
					elif params[0] == "CUD":
						if len(params) > 1:
							self.move_cursor_down(n=params[1])
						else:
							self.move_cursor_down()
					elif params[0] == "CUF" or params[0] == "CUR":
						if len(params) > 1:
							self.move_cursor_right(n=params[1])
						else:
							self.move_cursor_right()
					elif params[0] == "CUB" or params[0] == "CUL":
						if len(params) > 1:
							self.move_cursor_left(n=params[1])
						else:
							self.move_cursor_left()
					elif params[0] == "CNL":
						if len(params) > 1:
							self.new_line(n=params[1])
						else:
							self.new_line()
					elif params[0] == "CPL":
						if len(params) > 1:
							self.prev_line(n=params[1])
						else:
							self.prev_line()
					elif params[0] == "CUP":
						self.move_cursor_to(params[1], params[2])
					elif params[0] == "CLR_RIGHT":
						self.clear_to_right()
					elif params[0] == "CLR_LEFT":
						self.clear_to_left()
					elif params[0] == "CLR_LINE":
						self.clear_line()
					elif params[0] == "CLR_TOP":
						self.clear_to_top()
					elif params[0] == "CLR_BOTTOM":
						self.clear_to_bottom()
					elif params[0] == "CLR" or params[0] == "CLS" or params[0] == "CLR_SCREEN":
						self.clear()
					elif params[0] == "SU" or params[0] == "SCRL_UP":
						if len(params) > 1:
							self.scroll_up(n=params[1])
						else:
							self.scroll_up()
					elif params[0] == "SD" or params[0] == "SCRL_DOWN":
						if len(params) > 1:
							self.scroll_down(n=params[1])
						else:
							self.scroll_down()
					elif params[0] == "SCRL" or params[0] == "SCROLL":
						self.scroll(signed_scroll=params[1])
					elif params[0] == "SCP":
						self.save_cursor_position()
					elif params[0] == "RCP":
						self.restore_cursor_position()
					elif params[0] == "RSS" or params[0] == "RSET_STYLE":
						self.reset_style()
					elif params[0] == "BOLD":
						self.set_bold()
					elif params[0] == "BOLD_OFF":
						self.set_bold(False)
					elif params[0] == "UNDL":
						self.set_underline()
					elif params[0] == "UNDL_OFF":
						self.set_underline(False)
					elif params[0] == "BLNK":
						self.set_blink()
					elif params[0] == "BLNK_OFF":
						self.set_blink(False)
					elif params[0] == "RVRS" or params[0] == "INVERT":
						self.invert_colors()
					elif params[0] == "FONT":
						if len(params) > 1:
							self.set_font(font_code=params[1])
						else:
							self.reset_font()
					elif params[0] == "DFNT" or params[0] == "RSET_FONT":
						self.reset_font()
					elif params[0] == "FCLR" or params[0] == "FG":
						if len(params) == 2:
							self.set_foreground(params[1])
						elif len(params) == 4:
							self.set_foreground(params[1], params[2], params[3])
						else:
							raise SyntaxError("FCLR expected 1 or 3 arguments, recieved " + str(len(params)-1))
					elif params[0] == "BCLR" or params[0] == "BG":
						if len(params) == 2:
							self.set_background(params[1])
						elif len(params) == 4:
							self.set_background(params[1], params[2], params[3])
						else:
							raise SyntaxError("BCLR expected 1 or 3 arguments, recieved " + str(len(params)-1))
					else:
						raise SyntaxError("Unrecognized ANSI code:\n\t" + str(params[0]))
				else:
					print(s, end="")
				cmd_switch = not cmd_switch
			print(sep, end="")
		print(end, end="")
		return self

	def printANSI(self, C1, *args, ender="", seper=";", file=sys.stdout):
		"""Construct and print an ANSI Escape Code."""
		if self.DEBUG:
			print("\n", C1, end="", sep="", file=sys.stderr)
			print(*args, end=ender, sep=seper, file=sys.stderr)
		else:
			print(ESC, C1, sep="", end="")
			if args:
				print(*args, end="", sep=seper, flush=True, file=file)
			print(end=ender)
		return self

	def printCS(self, code, *args, file=sys.stdout):
		"""Construct and Print a Control Sequence."""
		return self.printANSI(CSI, *args, ender=code, file=file)

	def printSGR(self, *args, file=sys.stdout):
		"""Construct and Print a Select Graphic Rendition Sequence."""
		return self.printCS(SGR, *args, file=file)

	def printOSC(self, *args, file=sys.stdout):
		"""Construct and Print an Operating System Command."""
		return self.printANSI(OSC, *args, file=file)

	def printRIS(self, file=sys.stdout):
		"""Reset the screen to its original state."""
		return self.printANSI(RIS, file=file)

	def reset(self, file=sys.stdout):
		"""Reset the screen to its original state."""
		return self.printRIS(file=file)

	def reset_style(self, file=sys.stdout):
		"""Turn off all SGR attributes."""
		return self.printSGR(RSET, file=file)

	def clear_to_right(self, file=sys.stdout):
		"""Clear current line to the right edge without changing cursor position."""
		return self.printCS(EL, 0, file=file)

	def clear_to_left(self, file=sys.stdout):
		"""Clear current line to the left edge without changing cursor position."""
		return self.printCS(EL, 1, file=file)

	def clear_line(self, file=sys.stdout):
		"""Clear current line without changing cursor position."""
		return self.printCS(EL, 2, file=file)

	def clear_to_top(self, file=sys.stdout):
		"""Clear the screen from cursor to top."""
		return self.printCS(ED, 1, file=file)

	def clear_to_bottom(self, file=sys.stdout):
		"""Clear the screen from cursor to bottom."""
		return self.printCS(ED, 0, file=file)

	def clear(self, file=sys.stdout):
		"""Clear the screen from top to bottom."""
		return self.printCS(ED, 2, file=file)

	def scroll_up(self, n=1, file=sys.stdout):
		"""Scroll the screen up 'scroll' lines."""
		if n > 0:
			return self.printCS(SU, n, file=file)
		return self

	def scroll_down(self, n=1, file=sys.stdout):
		"""Scroll the screen down 'scroll' lines"""
		if n > 0:
			return self.printCS(SD, n, file=file)
		return self

	def scroll(self, signed_scroll, file=sys.stdout):
		"""Scrolls down if 'signed_scroll' is positive, up if negative"""
		if signed_scroll < 0:
			return self.scroll_up(-signed_scroll, file=file)
		elif signed_scroll > 0:
			return self.scroll_down(signed_scroll, file=file)
		return self

	def move_cursor_to(self, new_cursor_x, new_cursor_y, file=sys.stdout):
		"""Move the cursor to the specified position"""
		if new_cursor_x > 0 and new_cursor_y > 0:
			return self.printCS(CUP, new_cursor_x, new_cursor_y, file=file)
		return self

	def move_cursor_up(self, n=1, file=sys.stdout):
		"""Move the cursor up 'n' cells"""
		if n > 0:
			return self.printCS(CUU, n, file=file)
		return self

	def move_cursor_down(self, n=1, file=sys.stdout):
		"""Move the cursor down 'n' cells"""
		if n > 0:
			return self.printCS(CUD, n, file=file)
		return self

	def move_cursor_left(self, n=1, file=sys.stdout):
		"""Move the cursor left (back) 'n' cells"""
		if n > 0:
			return self.printCS(CUB, n, file=file)
		return self

	def move_cursor_right(self, n=1, file=sys.stdout):
		"""Move the cursor right (forward) 'n' cells"""
		if n > 0:
			return self.printCS(CUF, n, file=file)
		return self

	def new_line(self, n=1, file=sys.stdout):
		"""Move the cursor to beginning of 'n' lines down"""
		return self.printCS(CNL, n, file=file)

	def prev_line(self, n=1, file=sys.stdout):
		"""Move the cursor to beginning of 'n' lines up"""
		return self.printCS(CPL, n, file=file)

	def set_foreground(self, *args, file=sys.stdout):
		"""Set the text color. Use color code or R, G, B as arguments"""
		#for a in args:
		#	a = int(a)
		if len(args) == 3:
			return self.printSGR(FCLR, 2, *args, file=file)
		elif len(args) == 1:
			return self.printSGR(FCLR, 5, args[0], file=file)
		return self

	def set_background(self, *args, file=sys.stdout):
		"""Set the background color. Use color code or R, G, B as arguments"""
		if len(args) == 3:
			return self.printSGR(BCLR, 2, *args, file=file)
		elif len(args) == 1:
			return self.printSGR(BCLR, 5, arg[0], file=file)
		return self

	def invert_colors(self, file=sys.stdout):
		"""Set foreground color to background color, and vice-versa"""
		return self.printSGR(RVRS, file=file)

	def set_bold(self, *args, file=sys.stdout):
		"""Set boldness: setBold() is equivalent to setBold(True)"""
		if len(args) == 1:
			if args[0]:
				return self.printSGR(BOLD, file=file)
			return self.printSGR(BOLD_OFF, file=file)
		return self.printSGR(BOLD, file=file)

	def set_underline(self, *args, file=sys.stdout):
		"""Set Underline: setUnderline() is equivalent to setUnderline(True)"""
		if len(args) == 1:
			if args[0]:
				return self.printSGR(UNDL, file=file)
			return self.printSGR(UNDL_OFF, file=file)
		return self.printSGR(UNDL, file=file)

	def set_blink(self, *args, file=sys.stdout):
		"""Set Slow Blink: setBlink() is equivalent to setBlink(True)"""
		if len(args) == 1:
			if args[0]:
				return self.printSGR(BLNK, file=file)
			return self.printSGR(BLNK_OFF, file=file)
		return self.printSGR(BLNK, file=file)

	def set_font(self, font_code, file=sys.stdout):
		"""Use alternative font, or reset to default"""
		if font_code > 0 and font_code < 10:
			return self.printSGR(FONT[font_code], file=file)
		return self.printSGR(DFNT, file=file)
	
	def reset_font(self, file=sys.stdout):
		"""Reset to default font"""
		return self.printSGR(DFNT, file=file)

	def save_cursor_position(self, file=sys.stdout):
		"""Save current cursor position"""
		return self.printCS(SCP, file=file)

	def restore_cursor_position(self, file=sys.stdout):
		"""Restore saved cursor position"""
		return self.printCS(RCP, file=file)

	def output(self, x, y, *args, end="", sep="", file=sys.stdout):
		"""Print *args at location x,y"""
		#self.save_cursor_position().move_cursor_to(x, y, file=file)
		#print(*args, end=end, sep=sep, file=file)
		#return self.restore_cursor_position()
		if self.DEBUG:		
			print("{SCP}{CUP," + str(x) + "," + str(y) + "}" + sep.join(args) + "{RCP}")
		return self.printf("{SCP}{CUP," + str(x) + "," + str(y) + "}" + sep.join(args) + "{RCP}", end=end, file=file)
