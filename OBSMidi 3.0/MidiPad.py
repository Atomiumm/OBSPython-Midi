from utilities import PrintWithTime, PrintError
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame.midi as midi


class MidiPad(object):
	def __init__(self, Input = 1, Output = 3, PadConfig = {}, bypassexit = False):
		try:
			midi.init()
			self.In = midi.Input(Input, 1024)
			self.Out = midi.Output(Output, 1024)
		except:
			PrintError("Midi Pad not found")
			if not bypassexit:
				PrintError("Exiting program")
				exit()
		else:
			PrintWithTime("Connected Midi Pad")
		self.Pad = PadConfig

	def LedOff(Action):
		if "Led" in Action:
			try:
				midi_out.write_short(0x90, Action["Led"], 0)
			except:
				pass
		else:
			print("No Led information")

	def LedOn(Action):
		if "Led" in Action:
			if "LedMode" in Action:
				LedMode = Action["LedMode"]
			else:
				LedMode = 2
			try:
				midi_out.write_short(0x90, Action["Led"], LedMode)
			except:
				pass
		else:
			print("No Led information")

