
#https://github.com/Palakis/obs-websocket/blob/4.x-current/docs/generated/protocol.md


from obswebsocket import requests
import time


#This is the main function being called by MAIN.py
def execute_action(Action, Value, ws, midi_out):
	if "Action" in Action:
		if Action["Action"] == "SwitchScene":
			SwitchScene(Action, ws)
		elif Action["Action"] == "SetTransition":
			SetTransition(Action, ws)
		elif Action["Action"] == "SetTransitionDuration":
			SetTransitionDuration(Action, Value, ws)
		elif Action["Action"] == "ToggleStream":
			ToggleStream(Action, ws, midi_out)
		elif Action["Action"] == "ToggleRecording":
			ToggleRecording(Action, ws, midi_out)
		elif Action["Action"] == "TransitionToProgram":
			TransitionToProgram(Action, ws)
		#elif Action["Action"] == "ToggleStudioMode":   ---Causes crashes
		#	ToggleStudioMode(Action, ws, midi_out)
		elif Action["Action"] == "SetSourceVolume":
			SetSourceVolume(Action, Value, ws)
		elif Action["Action"] == "ToggleMuteSource":
			ToggleMuteSource(Action, ws, midi_out)
		else:
			print("Action unknown")
	else:
		print("No action argument in action config")



#The functions down this line are the functions executing the called actions


def SwitchScene(Action, ws):
	#Here we check whether StudioMode is on
	StudioState = CheckStudioState(ws)

	if StudioState == True:
		#Here we set the preview scene
		try:
			ws.call(requests.SetPreviewScene(Action["DestinationScene"]))
		except:
			print("Couldn't set " + Action["DestinationScene"] + " to program")
		else:
			PrintWithTime("Set " + Action["DestinationScene"] + " to program")
	else:
		#Here we set the configured transition mode
		if "Transition" in Action:
			Transition_old = GetTransition(ws)
			SetTransition(Action, ws)
		#Here we set the scene being viewed
		try:
			ws.call(requests.SetCurrentScene(Action["DestinationScene"]))
		except:
			print("Couldn't set " + Action["DestinationScene"] + " to program")
		else:
			PrintWithTime("Set " + Action["DestinationScene"] + " to program")
		#Here we set the transition mode back
		if "Transition" in Action:
			try:
				Duration = ws.call(requests.GetTransitionDuration())
				Duration = Duration.getTransitionDuration()
			except:
				print("Couldn't get transition duration")
			else:
				time.sleep(Duration/1000 + 0.1)
			finally:
				SetTransition(Transition_old, ws)



def SetTransition(Action, ws):
	if "Transition" in Action:
		try:
			ws.call(requests.SetCurrentTransition(Action["Transition"]))
		except:
			print("Couldn't set transition: " + Action["Transition"])
		else:
			PrintWithTime("TransitionMode was changed to " + Action["Transition"])
	else:
		print("No transition set up in action config")
	if "TransitionDuration" in Action:
		SetTransitionDuration(Action, None, ws)



def SetTransitionDuration(Action, Value, ws):
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
		print("Couldn't set transition duration: " + str(Value) + "ms")
	else:
		PrintWithTime("TransitionDuration was changed to " + str(Value) + "ms")



def ToggleStream(Action, ws, midi_out):
	#Here we check whether or not the stream is on
	try:
		StreamingState = ws.call(requests.GetStreamingStatus())
		StreamingState = StreamingState.getStreaming()
	except:
		print("Couldn't get streaming status")
	else:
		if StreamingState == True:
			try:
				#Here we turn the stream off
				ws.call(requests.StopStreaming())
			except:
				print("Couldn't stop stream")
			else:
				#Here we turn the Led on the midi pad off
				MidiLed(Action, "off", midi_out)
				#Here we wait for the stream to be turned off
				while StreamingState == True:
					try:
						StreamingState = ws.call(requests.GetStreamingStatus())
						StreamingState = StreamingState.getStreaming()
					except:
						print("Couldn't get streaming status")
						break
				PrintWithTime("Stopped Streaming")
		else:
			try:
				#Here we turn the stream on
				ws.call(requests.StartStreaming())
			except:
				print("Couldn't start stream")
			else:
				#Here we turn the Led on the midi pad on
				MidiLed(Action, "on", midi_out)
				#Here we wait for the stream to be turned on
				while StreamingState == False:
					try:
						StreamingState = ws.call(requests.GetStreamingStatus())
						StreamingState = StreamingState.getStreaming()
					except:
						print("Couldn't get streaming status")
						break
				PrintWithTime("Started Streaming")



def ToggleRecording(Action, ws, midi_out):
	try:
		Response = str(ws.call(requests.StartRecording()))
	except:
		print("Recording can't be toggled")
	else:
		if Response == "<StartRecording request ({}) called: failed ({'error': 'recording already active'})>":
			try:
				ws.call(requests.StopRecording())
			except:
				print("Couldn't turn recording off")
			else:
				MidiLed(Action, "off", midi_out)
				PrintWithTime("Recording stopped")
		elif Response == "<StartRecording request ({}) called: success ({})>":
			MidiLed(Action, "on", midi_out)
			PrintWithTime("Recording started")
		else:
			print("Couldn't toggle recording")



def TransitionToProgram(Action, ws):
	#Here we check whether StudioMode is on
	StudioState = CheckStudioState(ws)
	#Here we make the transition
	if StudioState == True:
		#Here we set the configured transition mode
		if "Transition" in Action:
			Transition_old = GetTransition(ws)
			SetTransition(Action, ws)
		#Here we make the transition
		try:
			CurrentsceneObject = ws.call(requests.GetPreviewScene())
			Currentscene = CurrentsceneObject.getName()
			ws.call(requests.SetCurrentScene(Currentscene))
		except:
			print("Couldn't send preview to program")
		else:
			PrintWithTime("Sent preview to program")
		#Here we set the transition mode back
		if "Transition" in Action:
			try:
				Duration = ws.call(requests.GetTransitionDuration())
				Duration = Duration.getTransitionDuration()
			except:
				print("Couldn't get transition duration")
			else:
				time.sleep(Duration/1000 + 0.1)
			finally:
				SetTransition(Transition_old, ws)
	else:
		print("StudioMode not enabled")
	

#Causes crashes
def ToggleStudioMode(Action, ws, midi_out):
	StudioState = CheckStudioState(ws)
	if StudioState == True:
		try:
			ws.call(requests.DisableStudioMode())
		except:
			print("Couldn't turn Studio Mode off")
		else:
			MidiLed(Action, "off", midi_out)
			PrintWithTime("Studio mode stopped")
	else:
		try:
			ws.call(requests.EnableStudioMode())
		except:
			print("Couldn't turn Studio Mode on")
		else:
			MidiLed(Action, "on", midi_out)
			PrintWithTime("Studio mode started")


#works but creates weird message
def SetSourceVolume(Action, Value, ws):
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
			print("Couldn't set source volume: " + str(Value * 100) + "%")
		else:
			PrintWithTime("Source volume was changed to " + str(Value * 100) + "%")
	else:
		print("No SourceName argument in action config")


#works but creates weird message
def ToggleMuteSource(Action, ws, midi_out):
	if "SourceName" in Action:
		try:
			MuteState = ws.call(requests.GetMute(Action["SourceName"]))
			MuteState = MuteState.getMuted()
		except:
			print("Couldn't get mute state")
		else:
			try:
				ws.call(requests.SetMute(Action["SourceName"], not MuteState))
			except:
				print("Couldn't toggle mute state of " + Action["SourceName"])
			else:
				if MuteState == True:
					MidiLed(Action, "off", midi_out)
				else:
					MidiLed(Action, "on", midi_out)
				PrintWithTime("Toggled the mute state of " + Action["SourceName"])
	else:
		print("No SourceName argument in action config")



def SetSceneCollection(Action, ws):
	try:
		ws.call(requests.SetCurrentSceneCollection(Action["SceneCollection"]))
	except:
		print("Couldn't set scene collection: " + Action["SceneCollection"])
	else:
		PrintWithTime("Set scene collection: " + Action["SceneCollection"])



#The functions down this line are the functions called by the action-functions


def MidiLed(Action, Mode, midi_out):
	if "Led" in Action:
		if Mode == "on":
			if "LedMode" in Action:
				Value = Action["LedMode"]
			else:
				Value = 2
		else:
			Value = 0
		try:
			midi_out.write_short(0x90, Action["Led"], Value)
		except:
			pass



def CheckStudioState(ws):
	StudioState = False
	try:
		StudioState = ws.call(requests.GetStudioModeStatus())
		StudioState = StudioState.getStudioMode()
	except:
		print("Couldn't get StudioModeStatus")
	else:
		return StudioState



def PrintWithTime(Text):
	print("[" + time.strftime("%H:%M:%S", time.localtime()) + "]", end = "	")
	print(Text) 



def GetTransition(ws):
	Result = {}
	try:
		Transition = ws.call(requests.GetCurrentTransition())
	except:
		print("Couldn't get current transition")
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

