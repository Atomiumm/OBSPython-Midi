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
import time
import json
import sys










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
		PrintError("Config " + Filename + " not found")
		PrintError("Exiting program")
		exit()
	except:
		PrintError("Couldn't open " + Filename + ".json")
		PrintError("Exiting program")
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
			PrintError("ERROR 404:  ConfigName argument was not found")
		if "StudioModeDefault" in config_general:
			global StudioModeDefault
			StudioModeDefault = config_general["StudioModeDefault"]
		else:
			PrintError("ERROR 404:  StudioModeDefault argument was not found")
		if "DefaultTransition" in config_general:
			global DefaultTransition
			DefaultTransition = config_general["DefaultTransition"]
		else:
			PrintError("ERROR 404:  DefaultTransition argument was not found")
		if "DefaultTransitionDuration" in config_general:
			global DefaultTransitionDuration
			DefaultTransitionDuration = config_general["DefaultTransitionDuration"]
		else:
			PrintError("ERROR 404:  DefaultTransitionDuration argument was not found")
		if "server_ip" in config_general:
			global server_ip
			server_ip = config_general["server_ip"]
		else:
			PrintError("ERROR 404:  server_ip argument was not found")
		if "server_port" in config_general:
			global server_port
			server_port = config_general["server_port"]
		else:
			PrintError("ERROR 404:  server_port argument as not found")
		if "server_password" in config_general:
			global server_password
			server_password = config_general["server_password"]
		else:
			PrintError("ERROR 404  server_password argument was not found")
		if "SceneCollection" in config_general:
			global SceneCollection
			SceneCollection = config_general["SceneCollection"]
		else:
			PrintError("ERROR 404  SceneCollection argument was not found")
		del config_general
	else:
		PrintError("No general config in config file")
	global config_pad
	if "config_pad" in SETUP_JSON:
		config_pad = SETUP_JSON["config_pad"]
		del SETUP_JSON
	else:
		PrintError("No pad config in config file")
		PrintError("Exiting program")
		exit()


	#Here we connect to the OBS Websocket
	global ws
	try:
		ws = obsws(server_ip, server_port, server_password)
		ws.connect()
	except:
		PrintError("Connection to OBS Websocket is impossible")
		PrintError("Exiting program")
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
		PrintError("Midi Pad not found")
		PrintError("Exiting program")
		exit()
	else:
		PrintWithTime("Connected Midi Pad")


	#Here we set up OBS like configured
	global OldSceneCollection
	try:
		OldSceneCollection = ws.call(requests.GetCurrentSceneCollection())
		OldSceneCollection = OldSceneCollection.getScName()
	except:
		PrintError("Couldn't get scenecollection")
	SetSceneCollection({"SceneCollection" : SceneCollection})
	#if str(CheckStudioState()) != StudioModeDefault:
	#	ToggleStudioMode({})
	SetTransition({"Transition":DefaultTransition, "TransitionDuration":DefaultTransitionDuration})


	PrintWithTime("Program is ready to use")










#The functions down this line are the functions called by the action-functions

def MidiLed(Action, Mode):
	if "Led" in Action:
		if Mode == "on":
			if "LedMode" in Action:
				LedMode = Action["LedMode"]
			else:
				LedMode = 2
		else:
			LedMode = 0
		try:
			midi_out.write_short(0x90, Action["Led"], LedMode)
		except:
			pass


def CheckStudioState():
	StudioState = False
	try:
		StudioState = ws.call(requests.GetStudioModeStatus())
		StudioState = StudioState.getStudioMode()
	except:
		PrintError("Couldn't get StudioModeStatus")
	else:
		return StudioState


def PrintWithTime(Text):
	print("[" + time.strftime("%H:%M:%S", time.localtime()) + "]", end = "	")
	print(Text) 


def PrintError(Text):
	print("ERROR", end = "	")
	PrintWithTime(Text)


def GetTransition():
	Result = {}
	try:
		Transition = ws.call(requests.GetCurrentTransition())
	except:
		PrintError("Couldn't get current transition")
	else:
		try:
			Result["Transition"] = Transition.getName()
		except:
			pass
		try:
			Result["TransitionDuration"] = Transition.getDuration()
		except:
			pass
	return Result










#The functions down this line are the functions executing the called actions

def SwitchScene(Action):
	#Here we check whether StudioMode is on
	StudioState = CheckStudioState()

	if StudioState == True:
		#Here we set the preview scene
		try:
			ws.call(requests.SetPreviewScene(Action["DestinationScene"]))
		except:
			PrintError("Couldn't set " + Action["DestinationScene"] + " to program")
		else:
			PrintWithTime("Set " + Action["DestinationScene"] + " to program")
	else:
		#Here we set the configured transition mode
		if "Transition" in Action:
			Transition_old = GetTransition()
			SetTransition(Action)
		#Here we set the scene being viewed
		try:
			ws.call(requests.SetCurrentScene(Action["DestinationScene"]))
		except:
			PrintError("Couldn't set " + Action["DestinationScene"] + " to program")
		else:
			PrintWithTime("Set " + Action["DestinationScene"] + " to program")
		#Here we set the transition mode back
		if "Transition" in Action:
			try:
				Duration = ws.call(requests.GetTransitionDuration())
				Duration = Duration.getTransitionDuration()
			except:
				PrintError("Couldn't get transition duration")
			else:
				time.sleep(Duration/1000 + 0.1)
			finally:
				SetTransition(Transition_old)


def SetTransition(Action):
	if "Transition" in Action:
		try:
			ws.call(requests.SetCurrentTransition(Action["Transition"]))
		except:
			PrintError("Couldn't set transition: " + Action["Transition"])
		else:
			PrintWithTime("TransitionMode was changed to " + Action["Transition"])
	else:
		PrintError("No transition set up in action config")
	if "TransitionDuration" in Action:
		SetTransitionDuration(Action, None)


def SetTransitionDuration(Action, Value):
	if Value == None:
		if "TransitionDuration" in Action:
			Value = Action["TransitionDuration"]
		else:
			Value = 0
	elif "MaxValue" in Action:
		if "MinValue" in Action:
			Value = (Action["MaxValue"] - Action["MinValue"]) / 127 * Value + Action["MinValue"]
		else:
			Value = Action["MaxValue"] / 127 * Value
	try:
		ws.call(requests.SetTransitionDuration(Value))
	except:
		PrintError("Couldn't set transition duration: " + str(Value) + "ms")
	else:
		PrintWithTime("TransitionDuration was changed to " + str(Value) + "ms")


def TurnStreamOn(Action):
	try:
		#Here we turn the stream on
		ws.call(requests.StartStreaming())
	except:
		PrintError("Couldn't start stream")
	else:
		#Here we turn the Led on the midi pad on
		MidiLed(Action, "on")
		#Here we wait for the stream to be turned on
		StreamingState = False
		while StreamingState == False:
			try:
				StreamingState = ws.call(requests.GetStreamingStatus())
				StreamingState = StreamingState.getStreaming()
			except:
				PrintError("Couldn't get streaming status")
				break
		PrintWithTime("Started Streaming")


def TurnStreamOff(Action):
	try:
		#Here we turn the stream off
		ws.call(requests.StopStreaming())
	except:
		PrintError("Couldn't stop stream")
	else:
		#Here we turn the Led on the midi pad off
		MidiLed(Action, "off")
		#Here we wait for the stream to be turned off
		StreamingState == True
		while StreamingState == True:
			try:
				StreamingState = ws.call(requests.GetStreamingStatus())
				StreamingState = StreamingState.getStreaming()
			except:
				PrintError("Couldn't get streaming status")
				break
		PrintWithTime("Stopped Streaming")


def ToggleStream(Action):
	#Here we check whether or not the stream is on
	try:
		StreamingState = ws.call(requests.GetStreamingStatus())
		StreamingState = StreamingState.getStreaming()
	except:
		PrintError("Couldn't get streaming status")
	else:
		if StreamingState == True:
			TurnStreamOff(Action)
		else:
			TurnStreamOn(Action)


def TurnRecordingOn():
	try:
		Response = str(ws.call(requests.StartRecording()))
	except:
		PrintError("Recording can't be turned on")
	else:
		if Response == "<StartRecording request ({}) called: failed ({'error': 'recording already active'})>":
			PrintError("Recording can't be turned on")
		else:
			MidiLed(Action, "on")
			PrintWithTime("Recording started")


def TurnRecordingOff():
	try:
		Response = str(ws.call(requests.StopRecording()))
	except:
		PrintError("Recording can't be turned off")
	else:
		if Response == "<StopRecording request ({}) called: success ({})>":
			MidiLed(Action, "off")
			PrintWithTime("Recording stopped")
		else:
			PrintError("Recording can't be turned off")


def ToggleRecording(Action):
	try:
		Response = str(ws.call(requests.StartRecording()))
	except:
		PrintError("Recording can't be toggled")
	else:
		if Response == "<StartRecording request ({}) called: failed ({'error': 'recording already active'})>":
			try:
				ws.call(requests.StopRecording())
			except:
				PrintError("Couldn't turn recording off")
			else:
				MidiLed(Action, "off")
				PrintWithTime("Recording stopped")
		elif Response == "<StartRecording request ({}) called: success ({})>":
			MidiLed(Action, "on")
			PrintWithTime("Recording started")
		else:
			PrintError("Couldn't toggle recording")


def TransitionToProgram(Action):
	#Here we check whether StudioMode is on
	StudioState = CheckStudioState()
	#Here we make the transition
	if StudioState == True:
		#Here we set the configured transition mode
		if "Transition" in Action:
			Transition_old = GetTransition()
			SetTransition(Action)
		#Here we make the transition
		try:
			CurrentsceneObject = ws.call(requests.GetPreviewScene())
			Currentscene = CurrentsceneObject.getName()
			ws.call(requests.SetCurrentScene(Currentscene))
		except:
			PrintError("Couldn't send preview to program")
		else:
			PrintWithTime("Sent preview to program")
		#Here we set the transition mode back
		if "Transition" in Action:
			try:
				Duration = ws.call(requests.GetTransitionDuration())
				Duration = Duration.getTransitionDuration()
			except:
				PrintError("Couldn't get transition duration")
			else:
				time.sleep(Duration/1000 + 0.1)
			finally:
				SetTransition(Transition_old)
	else:
		PrintError("StudioMode not enabled")

#Causes crashes
def ToggleStudioMode(Action):
	StudioState = CheckStudioState()
	if StudioState == True:
		try:
			ws.call(requests.DisableStudioMode())
		except:
			PrintError("Couldn't turn Studio Mode off")
		else:
			MidiLed(Action, "off")
			PrintWithTime("Studio mode stopped")
	else:
		try:
			ws.call(requests.EnableStudioMode())
		except:
			PrintError("Couldn't turn Studio Mode on")
		else:
			MidiLed(Action, "on")
			PrintWithTime("Studio mode started")

#works but creates weird message
def SetSourceVolume(Action, Value):
	if "SourceName" in Action:
		if Value == None:
			if "SourceVolume" in Action:
				Value = Action["SourceVolume"]
			else:
				Value = 0
		elif "MaxValue" in Action:
			if "MinValue" in Action:
				Value = (Action["MaxValue"] - Action["MinValue"]) / 127 * Value + Action["MinValue"]
			else:
				Value = Action["MaxValue"] / 127 * Value
		try:
			ws.call(requests.SetVolume(Action["SourceName"], Value))
		except:
			PrintError("Couldn't set source volume: " + str(Value * 100) + "%")
		else:
			PrintWithTime("Source volume was changed to " + str(Value * 100) + "%")
	else:
		PrintError("No SourceName argument in action config")

#not tested
def MuteSourceOn(Action):
	if "SourceName" in Action:
		try:
			ws.call(requests.SetMute(Action["SourceName"], True))
		except:
			PrintError("Couldn't mute " + Action["SourceName"])
	else:
		PrintError("No SourceName argument in action config")

#not tested
def MuteSourceOff(Action):
	if "SourceName" in Action:
		try:
			ws.call(requests.SetMute(Action["SourceName"], False))
		except:
			PrintError("Couldn't unmute " + Action["SourceName"])
	else:
		PrintError("No SourceName argument in action config")

#works but creates weird message
def ToggleMuteSource(Action):
	if "SourceName" in Action:
		try:
			MuteState = ws.call(requests.GetMute(Action["SourceName"]))
			MuteState = MuteState.getMuted()
		except:
			PrintError("Couldn't get mute state")
		else:
			try:
				ws.call(requests.SetMute(Action["SourceName"], not MuteState))
			except:
				PrintError("Couldn't toggle mute state of " + Action["SourceName"])
			else:
				if MuteState == True:
					MidiLed(Action, "off")
				else:
					MidiLed(Action, "on")
				PrintWithTime("Toggled the mute state of " + Action["SourceName"])
	else:
		PrintError("No SourceName argument in action config")


def SetSceneCollection(Action):
	if "SceneCollection" in Action:
		if Action["SceneCollection"] == "Standard":
			Action["SceneCollection"] = OldSceneCollection
		try:
			ws.call(requests.SetCurrentSceneCollection(Action["SceneCollection"]))
		except:
			PrintError("Couldn't set scene collection: " + Action["SceneCollection"])
		else:
			PrintWithTime("Set scene collection: " + Action["SceneCollection"])
	else:
		PrintError("No SceneCollection argument in action config")










#This is the main function being called
def execute_action(Action, Value):
	if "Action" in Action:
		if Action["Action"] == "SwitchScene":
			SwitchScene(Action)
		elif Action["Action"] == "SetTransition":
			SetTransition(Action)
		elif Action["Action"] == "SetTransitionDuration":
			SetTransitionDuration(Action, Value)
		elif Action["Action"] == "TurnStreamOn":
			TurnStreamOn(Action)
		elif Action["Action"] == "TurnStreamOff":
			TurnStreamOff(Action)
		elif Action["Action"] == "ToggleStream":
			ToggleStream(Action)
		elif Action["Action"] == "TurnRecordingOn":
			TurnRecordingOn()
		elif Action["Action"] == "TurnRecordingOff":
			TurnRecordingOff()
		elif Action["Action"] == "ToggleRecording":
			ToggleRecording(Action)
		elif Action["Action"] == "TransitionToProgram":
			TransitionToProgram(Action)
		#elif Action["Action"] == "ToggleStudioMode":   ---Causes crashes
		#	ToggleStudioMode(Action)
		elif Action["Action"] == "SetSourceVolume":
			SetSourceVolume(Action, Value)
		elif Action["Action"] == "MuteSourceOn":
			MuteSourceOn(Action)
		elif Action["Action"] == "MuteSourceOff":
			MuteSourceOff(Action)
		elif Action["Action"] == "ToggleMuteSource":
			ToggleMuteSource(Action)
		elif Action["Action"] == "SetSceneCollection":
			SetSceneCollection(Action)
		else:
			PrintError("Action unknown")
	else:
		PrintError("No action argument in action config")










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
				PrintError("Button " + Button + " not configured")
	else:
		PrintError("No buttons configured in config")

	#Here we execute the configured actions
	for Action in ACTIONLIST:
		execute_action(Action, None)


#This function is to decide what to do depending on the fader that was sled
def fader(Fader, Value):
	#This is to find out what actions are supposed to be executed
	if "Faders" in config_pad:
		if Fader in config_pad["Faders"]:
			if "ActionGeneral" in config_pad["Faders"][Fader]:
				for Action in config_pad["Faders"][Fader]["ActionGeneral"]:
					execute_action(Action, Value)
			if Value == 127:
				if "ActionOnMax" in config_pad["Faders"][Fader]:
					for Action in config_pad["Faders"][Fader]["ActionOnMax"]:
						execute_action(Action, None)
			elif Value == 0:
				if "ActionOnMin" in config_pad["Faders"][Fader]:
					for Action in config_pad["Faders"][Fader]["ActionOnMin"]:
						execute_action(Action, None)
		else:
			PrintError("Fader " + Fader + " not configured")
	else:
		PrintError("No faders configured in config")










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
				time.sleep(0.01)
			fader(str(next_read[0][0][1]), next_read[0][0][2])
	time.sleep(0.01)