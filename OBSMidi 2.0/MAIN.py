#!/usr/bin/env python
# -*- coding: utf-8 -*-


#These variables are here to prevent having undeclared variables in case we have a problem with the config JSON
server_ip = "localhost"
server_port = 4444
server_password = "secret"
ConfigName = "SOS"
StudioModeDefault = "False"
DefaultTransition = "Cut"
DefaultTransitionDuration = 300
SceneCollection = "FrequenceBanane"






from obswebsocket import obsws, requests
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame.midi as midi
from time import sleep
import json
import sys

from Functions import *






#This function is the first to be called. It is used only once to execute the necessary setup.
def Setup():
	PrintWithTime("Program started")


	#First we read the config to correctly define our global variables
	global SETUP_JSON
	#This allows us to either put the config name in the argv variables or to get asked for the config
	#Example: python ProgramName.py ConfigName
	if len(sys.argv) > 1:
		Filename = sys.argv[1]
	else:
		Filename = input("What is the name of your config file? --> ")
	if Filename == "":
		Filename = "FrequenceBanane"
	#Open the config JSON
	try:
		SETUP_JSON = json.loads(''.join(open("Config\\" + Filename + ".json", "r")))
	except FileNotFoundError:
		print("Config " + Filename + " not found")
		print("Exiting program")
		exit()
	except:
		print("Couldn't open " + Filename + ".json")
		print("Exiting program")
		exit()
	else:
		PrintWithTime("Opened config:  " + Filename)
	#Define the global variables correctly
	if "config_general" in SETUP_JSON:
		config_general = SETUP_JSON["config_general"]
		if "ConfigName" in config_general:
			global ConfigName
			ConfigName = config_general["ConfigName"]
		else:
			print("ERROR 404:  ConfigName argument was not found")
		if "StudioModeDefault" in config_general:
			global StudioModeDefault
			StudioModeDefault = config_general["StudioModeDefault"]
		else:
			print("ERROR 404:  StudioModeDefault argument was not found")
		if "DefaultTransition" in config_general:
			global DefaultTransition
			DefaultTransition = config_general["DefaultTransition"]
		else:
			print("ERROR 404:  DefaultTransition argument was not found")
		if "DefaultTransitionDuration" in config_general:
			global DefaultTransitionDuration
			DefaultTransitionDuration = config_general["DefaultTransitionDuration"]
		else:
			print("ERROR 404:  DefaultTransitionDuration argument was not found")
		if "server_ip" in config_general:
			global server_ip
			server_ip = config_general["server_ip"]
		else:
			print("ERROR 404:  server_ip argument was not found")
		if "server_port" in config_general:
			global server_port
			server_port = config_general["server_port"]
		else:
			print("ERROR 404:  server_port argument as not found")
		if "server_password" in config_general:
			global server_password
			server_password = config_general["server_password"]
		else:
			print("ERROR 404  server_password argument was not found")
		if "SceneCollection" in config_general:
			global SceneCollection
			SceneCollection = config_general["SceneCollection"]
		else:
			print("ERROR 404  SceneCollection argument was not found")
		del config_general
	else:
		print("No general config in config file")
	global config_pad
	if "config_pad" in SETUP_JSON:
		config_pad = SETUP_JSON["config_pad"]
		del SETUP_JSON
	else:
		print("No pad config in config file")
		print("Exiting program")
		exit()


	#Here we connect to the OBS Websocket
	global ws
	try:
		ws = obsws(server_ip, server_port, server_password)
		ws.connect()
	except:
		print("Connection to OBS Websocket is impossible")
		print("Exiting program")
		exit()
	else:
		PrintWithTime("Connected to Websocket")


	#Here we connect to the midi pad
	global midi_in
	global midi_out
	try:
		midi.init()
		midi_in = midi.Input(1, 1024)
		midi_out = midi.Output(3, 1024)
	except:
		print("Midi Pad not found")
		print("Exiting program")
		exit()
	else:
		PrintWithTime("Connected Midi Pad")


	#Here we set up OBS like configured
	OldSceneCollection = ws.call(requests.GetCurrentSceneCollection())
	OldSceneCollection = OldSceneCollection.getScName()
	SetSceneCollection({"SceneCollection" : SceneCollection})
	#if str(CheckStudioState) != StudioModeDefault:
	#	ToggleStudioMode({}, ws, midi_out)
	SetTransition({"Transition":DefaultTransition, "TransitionDuration":DefaultTransitionDuration}, ws)
	for key in config_pad:
		for key2 in config_pad[key]:
			for key3 in config_pad[key][key2]:
				for Action in config_pad[key][key2][key3]:
					if "SceneCollection" in Action:
						if Action["SceneCollection"] == "Standard":
							Action["SceneCollection"] = OldSceneCollection



	PrintWithTime("Program is ready to use")










#This function is to decide what to do depending on the button that was pressed
def press_button(Button, Event):
	#This is to find out what actions are supposed to be executed
	ACTIONLIST = []
	if "Buttons" in config_pad:
		if Button in config_pad["Buttons"]:
			if Event == 154:
				if "ActionOnPress" in config_pad["Buttons"][Button]:
					ACTIONLIST = config_pad["Buttons"][Button]["ActionOnPress"]
			elif Event == 138:
				if "ActionOnRelease" in config_pad["Buttons"][Button]:
					ACTIONLIST = config_pad["Buttons"][Button]["ActionOnRelease"]
		else:
			if Event == 154:
				print("Button " + Button + " not configured")
	else:
		print("No buttons configured in config")

	#Here we execute the configured actions
	for Action in ACTIONLIST:
		execute_action(Action, None, ws, midi_out)



#This function is to decide what to do depending on the fader that was sled
def fader(Fader, Value):
	#This is to find out what actions are supposed to be executed
	if "Faders" in config_pad:
		if Fader in config_pad["Faders"]:
			if "ActionGeneral" in config_pad["Faders"][Fader]:
				for Action in config_pad["Faders"][Fader]["ActionGeneral"]:
					execute_action(Action, Value, ws, midi_out)
			if Value == 127:
				if "ActionOnMax" in config_pad["Faders"][Fader]:
					for Action in config_pad["Faders"][Fader]["ActionOnMax"]:
						execute_action(Action, None, ws, midi_out)
			elif Value == 0:
				if "ActionOnMin" in config_pad["Faders"][Fader]:
					for Action in config_pad["Faders"][Fader]["ActionOnMin"]:
						execute_action(Action, None, ws, midi_out)
		else:
			print("Fader " + Fader + " not configured")
	else:
		print("No faders configured in config")










Setup()
while True:
	while midi_in.poll():
		midi_read = midi_in.read(1)
		#print(midi_read)
		if midi_read[0][0][0] == 154 or midi_read[0][0][0] == 138:
			press_button(str(midi_read[0][0][1]), midi_read[0][0][0])
		if midi_read[0][0][0] == 186:
			next_read = midi_read
			while midi_in.poll():
				next_read = midi_in.read(1)
				sleep(0.01)
			fader(str(next_read[0][0][1]), next_read[0][0][2])
	sleep(0.01)