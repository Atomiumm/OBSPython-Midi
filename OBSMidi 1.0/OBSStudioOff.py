#!/usr/bin/env python
# -*- coding: utf-8 -*-

host = "localhost"
port = 4444
password = "secret"

from obswebsocket import obsws, requests
import pygame.midi as midi
import time

ws = obsws(host, port, password)
ws.connect()

def press_button(Button):
	if Button == 8:
		try:
			print("Connecting to Camera1")
			ws.call(requests.SetCurrentScene("Camera1"))
		except:
			print("Exception happened")
	elif Button == 9:
		try:
			print("Connecting to Camera2")
			ws.call(requests.SetCurrentScene("Camera2"))
		except:
			print("Exception happened")
	elif Button == 15:
		try:
			print("Connecting to Scene")
			ws.call(requests.SetCurrentScene("Scene"))
		except:
			print("Exception happened")


midi.init()
midi_in = midi.Input(1, 1024)
ws.call(requests.DisableStudioMode())
while True:
	while midi_in.poll():
		midi_read = midi_in.read(1)
#		print(midi_read)
		if midi_read[0][0][0] == 154:
#			print(midi_read[0][0][1])
			press_button(midi_read[0][0][1])
	time.sleep(0.01)