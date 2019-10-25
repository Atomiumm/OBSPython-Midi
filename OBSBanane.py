#!/usr/bin/env python
# -*- coding: utf-8 -*-

#These variables are here to prevent having undeclared variables in case we have a problem with the config JSON
server_ip = "localhost"
server_port = 4444
server_password = "secret"
ConfigName = "SOS"
StudioMode = False
DefaultTransition = "Cut"
DefaultTransitionDuration = 300






from obswebsocket import obsws, requests
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame.midi as midi
import time
import json
import sys






#This function is the first to be called. It is used only once to execute the necessary setup.
def Setup():
	print("[" + time.strftime("%H:%M:%S", time.localtime()) + "]", end = "	")
	print("Program started")


	#First we read the config to correctly define our global variables
	global setup_json
	try:
		#This allows us to either put the config name in the argv variables or to get asked for the config
		#Example: python ProgramName.py ConfigName
		if len(sys.argv) > 1:
			Filename = sys.argv[1]
		else:
			Filename = input("What is the name of your config file?")
		if Filename == "":
			Filename = "FrequenceBanane"
		#Open the config JSON
		setup_json = json.loads(''.join(open("Config\\" + Filename + ".json", "r")))
		print("Opened config:  " + Filename)
		#Define the global config variables correctly
		if "config_general" in setup_json:
			config_general = setup_json["config_general"]
			if "ConfigName" in config_general:
				global ConfigName
				ConfigName = config_general["ConfigName"]
			else:
				print("ERROR 404:  ConfigName argument was not found")
			if "StudioMode" in config_general:
				global StudioMode
				StudioMode = config_general["StudioMode"]
			else:
				print("ERROR 404:  StudioMode argument was not found")
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
		else:
			print("No general config in config file")
	except FileNotFoundError:
		print("Config file " + Filename + " not found")


	#Here we connect to the OBS Websocket
	global ws
	try:
		ws = obsws(server_ip, server_port, server_password)
		ws.connect()
		print("Connected to Websocket")
	except:
		print("Connection to OBS Websocket is impossible")
		print("Exiting program")
		exit()


	#Here we connect to the midi pad
	global midi_in
	global midi_out
	try:
		midi.init()
		midi_in = midi.Input(1, 1024)
		midi_out = midi.Output(3, 1024)
		print("Connected Midi Pad")
	except:
		print("Midi Pad not found")
		print("Chaque année, des millions de programmeurs disent qu'ils vont régler ce problème, et ils ne le font jamais. Si vous voyez ce message, c'est que nous faisons parti de ces programmeurs.")
		print("Exiting program")
		exit()


	print("[" + time.strftime("%H:%M:%S", time.localtime()) + "]", end = "	")
	print("Program is ready to use")






#This function checks whether the StudioMode is on or not and returns the answer
def CheckStudioState():
	StudioState = False
	try:
		StudioState = ws.call(requests.GetStudioModeStatus())
		StudioState = StudioState.getStudioMode()
	except:
		print("Couldn't get StudioModeStatus")
	return StudioState



#This function is used to set the transitionmode in OBS
def SetTransitionMode(Transition, Duration):
	#This variable is used to check whether an error occured
	Error = False
	#Here we set the transition type
	if Transition != None:
		try:
			ws.call(requests.SetCurrentTransition(Transition))
			print("TransitionMode was changed to " + Transition)
		except:
			print("Couldn't set transition: " + Transition)
			Error = True
	#Here we set the transition duration
	if Duration != None:
		try:
			ws.call(requests.SetTransitionDuration(Duration))
			print("TransitionDuration was changed to " + str(Duration) + "ms")
		except:
			print("Couldn't set transition duration: " + str(Duration) + "ms")
			Error = True
	#Here we return whether or not an error occured
	return Error






#This function is used to set the scene to be viewed
def SwitchScene(BUTTONCONF):
	#Here we check whether StudioMode is on
	StudioState = CheckStudioState()
	if StudioState == True:
		#Here we set the preview scene
		try:
			ws.call(requests.SetPreviewScene(BUTTONCONF["DestinationScene"]))
			print("Set Target to preview")
		except:
			print("Couldn't set Target to preview")
		#These lines are here to change the transition mode when pressing scene button. They produce lag and are commented out
	#	if "Transition" in BUTTONCONF:
	#		if "TransitionDuration" in BUTTONCONF:
	#			SetTransitionMode(BUTTONCONF["Transition"], BUTTONCONF["TransitionDuration"])
	#		else:
	#			SetTransitionMode(BUTTONCONF["Transition"], None)
	#		
	#	if "Transition" not in BUTTONCONF:
	#		SetTransitionMode(DefaultTransition, DefaultTransitionDuration)

	else:
		#Here we set the transition specified in config
		if "Transition" in BUTTONCONF:
			if "TransitionDuration" in BUTTONCONF:
				SetTransitionMode(BUTTONCONF["Transition"], BUTTONCONF["TransitionDuration"])
			else:
				SetTransitionMode(BUTTONCONF["Transition"], None)
		#Here we set the scene being viewed
		try:
			ws.call(requests.SetCurrentScene(BUTTONCONF["DestinationScene"]))
			print("Set " + BUTTONCONF["DestinationScene"] + " to program")
		except:
			print("Couldn't set " + BUTTONCONF["DestinationScene"] + " to program")
		#Here we set back the transition to the defaults
		if "Transition" in BUTTONCONF:
			time.sleep(BUTTONCONF["TransitionDuration"] / 1000 + 0.1)
			SetTransitionMode(DefaultTransition, DefaultTransitionDuration)



#This function is used to set the preview to program when in StudioMode
def TransitionToProgram():
	#Here we check whether StudioMode is on
	StudioState = CheckStudioState()
	#Here we make the transition
	if StudioState == True:
		try:
			CurrentsceneObject = ws.call(requests.GetPreviewScene())
			Currentscene = CurrentsceneObject.getName()
			ws.call(requests.SetCurrentScene(Currentscene))
			print("Sent preview to program")
		except:
			print("Couldn't send preview to program")
	else:
		print("StudioMode not enabled")



#This function is used to set the specified transition to OBS and to the defaults
def SetTransition(BUTTONCONF):
	global DefaultTransition
	global DefaultTransitionDuration
	if "Transition" in BUTTONCONF:
		if "TransitionDuration" in BUTTONCONF:
			if SetTransitionMode(BUTTONCONF["Transition"], BUTTONCONF["TransitionDuration"]) == False:
				DefaultTransition = BUTTONCONF["Transition"]
				DefaultTransitionDuration = BUTTONCONF["TransitionDuration"]
				print("Defaults have been changed to " + DefaultTransition + " : " + str(DefaultTransitionDuration) + "ms")
		else:
			if SetTransitionMode(BUTTONCONF["Transition"], None) == False:
				DefaultTransition = BUTTONCONF["Transition"]
				print("Default has been changed to " + DefaultTransition)
	else:
		print("No Transition argument in ButtonConfig")



#This function is used to set the specified transition duration to OBS and to the defaults
def ButtonSetTransitionDuration(BUTTONCONF):
	global DefaultTransitionDuration
	if "TransitionDuration" in BUTTONCONF:
		if SetTransitionMode(None, BUTTONCONF["TransitionDuration"]) == False:
			DefaultTransitionDuration = BUTTONCONF["TransitionDuration"]
			print("Default has been changed to " + str(DefaultTransitionDuration) + "ms")
	else:
		print("No TransitionDuration argument in ButtonConfig")



#This function is used to toggle the stream on and off
def ToggleStream(BUTTONCONF):
	#Here we check whether or not the stream is on
	StreamingState = True
	try:
		StreamingState = ws.call(requests.GetStreamingStatus())
		StreamingState = StreamingState.getStreaming()
	except:
		print("Couldn't get streaming status")

	if StreamingState == True:
		try:
			#Here we turn the stream off
			ws.call(requests.StopStreaming())
			#Here we turn the Led on the midi pad off
			try:
				if "Led" in BUTTONCONF:
					midi_out.write_short(0x90, BUTTONCONF["Led"], 0)
				else:
					print("No Led argument in Button config")
			except:
				pass
			#Here we wait for the stream to be turned off
			while StreamingState == True:
				try:
					StreamingState = ws.call(requests.GetStreamingStatus())
					StreamingState = StreamingState.getStreaming()
				except:
					print("Couldn't get streaming status")
			print("Stopped Streaming")
		except:
			print("Couldn't stop stream")
	else:
		try:
			#Here we turn the stream on
			ws.call(requests.StartStreaming())
			#Here we turn the Led on the midi pad on
			try:
				if "Led" in BUTTONCONF:
					if "LedMode" in BUTTONCONF:
						midi_out.write_short(0x90, BUTTONCONF["Led"], BUTTONCONF["LedMode"])
					else:
						print("No LedMode argument in Button config")
				else:
					print("No Led argument in Button config")
			except:
				pass
			#Here we wait for the stream to be turned on
			while StreamingState == False:
				try:
					StreamingState = ws.call(requests.GetStreamingStatus())
					StreamingState = StreamingState.getStreaming()
				except:
					print("Couldn't get streaming status")
			print("Started Streaming")
		except:
			print("Couldn't start stream")



#This function is used to toggle the recording on and off
def ToggleRecording(BUTTONCONF):
	RecordOn = True
	try:
		#Here we try to turn the recording on
		if str(ws.call(requests.StartRecording())) != "<StartRecording request ({}) called: failed ({'error': 'recording already active'})>":
			print("Recording started")
			RecordOn = False
			#Here we turn the Led on the midi pad on
			try:
				if "Led" in BUTTONCONF:
					if "LedMode" in BUTTONCONF:
						midi_out.write_short(0x90, BUTTONCONF["Led"], BUTTONCONF["LedMode"])
					else:
						print("No LedMode argument in Button config")
				else:
					print("No Led argument in Button config")
			except:
				pass
	except:
		pass
	#Here we try to turn the recording off if the first try failed
	if RecordOn == True:
		try:
			ws.call(requests.StopRecording())
			print("Recording stopped")
			#Here we turn the Led on the midi pad off
			try:
				if "Led" in BUTTONCONF:
					midi_out.write_short(0x90, BUTTONCONF["Led"], 0)
				else:
					print("No Led argument in Button config")
			except:
				pass
		except:
			print("Recording couldn't be toggled")



#This function is used to set the specified transition duration to OBS and to the defaults
def FaderSetTransitionDuration(FADERCONF, Value):
	global DefaultTransitionDuration
	if "MinValue" in FADERCONF and "MaxValue" in FADERCONF:
		#Here we calculate the duration value
		Value = (FADERCONF["MaxValue"] - FADERCONF["MinValue"]) / 127 * Value + FADERCONF["MinValue"]
		#Here we set the transition
		if SetTransitionMode(None, Value) == False:
			DefaultTransitionDuration = Value
			print("Default has been changed to " + str(DefaultTransitionDuration) + "ms")
	else:
		print("No reference values in Fader config")






#This function is to decide what to do depending on the button that was pressed
def press_button(Button, Event):
	#This is to find out what action is supposed to be done
	Action = None
	if "config_pad" in setup_json:
		if "Buttons" in setup_json["config_pad"]:
			if Button in setup_json["config_pad"]["Buttons"]:
				BUTTONCONF = setup_json["config_pad"]["Buttons"][Button]
				if "Event" in BUTTONCONF:
					if (BUTTONCONF["Event"] == "OnRelease" and Event == 138) or (BUTTONCONF["Event"] == "OnPress" and Event == 154):
						if "Action" in BUTTONCONF:
							Action = BUTTONCONF["Action"]
						else:
							print("No Action argument in Button config")
				else:
					print("No Event argument in Button config")
			else:
				if Event != 138:
					print("Button " + Button + " not found")
		else:
			print("No Button argument in config_pad argument")
	else:
		print("No config_pad argument in config")

	#Here we execute the defined action
	if Action == "SwitchScene":
		SwitchScene(BUTTONCONF)

	if Action == "TransitionToProgram":
		TransitionToProgram()

	if Action == "SetTransition":
		SetTransition(BUTTONCONF)

	if Action == "SetTransitionDuration":
		ButtonSetTransitionDuration(BUTTONCONF)

	if Action == "ToggleStream":
		ToggleStream(BUTTONCONF)

	if Action == "ToggleRecording":
		ToggleRecording(BUTTONCONF)



#This function is to decide what to do depending on the fader that was sled
def fader(Fader, Value):
	#This is to find out what action is supposed to be done
	Action = None
	if "config_pad" in setup_json:
		if "Faders" in setup_json["config_pad"]:
			if Fader in setup_json["config_pad"]["Faders"]:
				FADERCONF = setup_json["config_pad"]["Faders"][Fader]
				if "Action" in FADERCONF:
					Action = FADERCONF["Action"]
				else:
					print("No Action argument in Fader config")
			else:
				print("Fader " + Fader + " not found")
		else:
			print("No Fader argument in config_pad argument")
	else:
		print("No config_pad argument in config")

	#Here we execute the defined action
	if Action == "SetTransitionDuration":
		FaderSetTransitionDuration(FADERCONF, Value)










#This is the main program
Setup()
while True:
	while midi_in.poll():
		midi_read = midi_in.read(1)
		#print(midi_read)
		if midi_read[0][0][0] != 138:
			print("[" + time.strftime("%H:%M:%S", time.localtime()) + "]", end = "	")
		if midi_read[0][0][0] == 154 or midi_read[0][0][0] == 138:
			press_button(str(midi_read[0][0][1]), midi_read[0][0][0])
		if midi_read[0][0][0] == 186:
			next_read = midi_read
			while midi_in.poll():
				next_read = midi_in.read(1)
				time.sleep(0.01)
			fader(str(next_read[0][0][1]), next_read[0][0][2])
	time.sleep(0.01)
