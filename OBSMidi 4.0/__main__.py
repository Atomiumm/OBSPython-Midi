#!/usr/bin/python
# -*- coding: utf-8 -*-

from FunctionMap import function
from config import *
from lib.OBSAPI import OBSObject
import time
import pygame.midi as midi
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


def connect_midi():
	global default_midi_input
	midi_in = None
	while midi_in == None:
		try:
			midi_in = midi.Input(int(default_midi_input), 1024)
			print("Connected to default midi device")
			return midi_in
		except Exception as e:
			print(f"Connection to default midi device failed. Error: {e}")
			print("Choose a device (num) or manual mode (m)")
			for i in range(midi.get_count()):
				info = midi.get_device_info(i)
				if info[2]:
					print(i, info)
			default_midi_input = input("->")
			if default_midi_input == "m":
				return False


def callFunction(action, *args):
	try:
		if action["Action"].startswith("OBS"):
			if len(args) < 1:
				function[action["Action"]](OBSSocket, *(action["args"]), **(action["kwargs"]))
			else:
				function[action["Action"]](OBSSocket, *args, *(action["args"]), **(action["kwargs"]))
	except Exception as e:
		print(e)


if __name__ == "__main__":
	os.system("cls")

	try:
		OBSSocket = OBSObject("localhost", 4444, "password")
	except Exception as e:
		print(f"Couldn't connect to OBS socket. Error : {e}")

	for action in Actions_on_start:
		callFunction(action)

	midi.init()
	midi_in = connect_midi()
	if midi_in:
		while True:
			while midi_in.poll():
				try:
					midi_read = midi_in.read(1)
					print(midi_read)
					if midi_read[0][0][0] == 154:
						for action in Buttons[str(midi_read[0][0][1])]["ActionOnPress"]:
							callFunction(action)
					if midi_read[0][0][0] == 138:
						for action in Buttons[str(midi_read[0][0][1])]["ActionOnRelease"]:
							callFunction(action)
					if midi_read[0][0][0] == 186:
						next_read = midi_read
						while midi_in.poll():
							next_read = midi_in.read(1)
						print(next_read)
						for action in Faders[str(next_read[0][0][1])]["ActionGeneral"]:
							callFunction(action, next_read[0][0][2])
						for delimitation in Faders[str(next_read[0][0][1])]["ActionDelimited"]:
							if next_read[0][0][2] <= delimitation["LimitHigh"] and next_read[0][0][2] >= delimitation["LimitLow"]:
								for action in delimitation["Actions"]:
									callFunction(action, next_read[0][0][2])
				except KeyError:
					print(f"Button {midi_read[0][0][1]} missing or not configured correctly")
				except Exception as e:
					print(e)
			time.sleep(0.01)
	else:
		while True:
			read = input("input --> ")
			try:
				if "b" == read[0].lower():
					for action in Buttons[read[1:]]["ActionOnPress"]:
						callFunction(action)
					for action in Buttons[read[1:]]["ActionOnRelease"]:
						callFunction(action)
				if "f" == read[0].lower():
					for action in Faders[read[1:].split(",")[0]]["ActionGeneral"]:
						callFunction(action, int(read[1:].split(",")[1]))
					for delimitation in Faders[read[1:].split(",")[0]]["ActionDelimited"]:
						if int(read[1:].split(",")[1]) <= delimitation["LimitHigh"] and int(read[1:].split(",")[1]) >= delimitation["LimitLow"]:
							for action in delimitation["Actions"]:
								callFunction(action, int(read[1:].split(",")[1]))
				if "help" in read.lower():
					print(Buttons)
					print(Faders)
			except Exception as e:
				print(e)
	midi.quit()

# how to quit?
