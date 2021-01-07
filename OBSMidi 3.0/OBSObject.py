from obswebsocket import obsws, requests
#https://github.com/Palakis/obs-websocket/blob/4.x-current/docs/generated/protocol.md#getversion

def PrintWithTime(Text):
	print("[" + time.strftime("%H:%M:%S", time.localtime()) + "]", end = "	")
	print(Text)



class OBSObject(object):
	def __init__(self, server_ip, server_port, server_password, bypassexit = False):
		try:
			self.ws = obsws(server_ip, server_port, server_password)
			self.ws.connect()
		except:
			print("Connection to OBS Websocket is impossible")
		else:
			PrintWithTime("Connected to Websocket")
		

	#
	#	Some Info
	#	
	def GetStats(self):
		try:
			return self.ws.call(requests.GetStats()).__dict__["datain"]
		except Exception as e:
			print(e)

	def GetVideoInfo(self):
		try:
			return self.ws.call(requests.GetVideoInfo()).__dict__["datain"]
		except Exception as e:
			print(e)


	#
	#	Outputs (not sure what it does)
	#
	def ListOutputs(self): #untested
		try:
			return self.ws.call(requests.ListOutputs()).__dict__["datain"]
		except Exception as e:
			print(e)

	def GetOutputInfo(self, Output): #untested
		try:
			return self.ws.call(requests.GetOutputInfo(Output)).__dict__["datain"]["outputs"]
		except Exception as e:
			print(e)

	def StartOutput(self, Output): #untested
		try:
			self.ws.call(requests.StartOutput(Output))
		except Exception as e:
			print(e)

	def StopOutput(self, Output): #untested
		try:
			self.ws.call(requests.StopOutput(Output))
		except Exception as e:
			print(e)


	#
	#	SceneCollections
	#
	def ListSceneCollections(self):
		try:
			return self.ws.call(requests.ListSceneCollections()).__dict__["datain"]["SceneCollections"]
		except Exception as e:
			print(e)
	
	def GetCurrentSceneCollection(self):
		try:
			return self.ws.call(requests.GetCurrentSceneCollection()).__dict__["datain"]["SceneCollection-name"]
		except Exception as e:
			print(e)

	def SetCurrentSceneCollection(self, SceneCollectionName):
		try:
			self.ws.call(requests.SetCurrentSceneCollection(SceneCollectionName))
		except Exception as e:
			print(e)


	#
	#	Recording
	#
	def StartRecording(self):
		try:
			self.ws.call(requests.StartRecording())
		except Exception as e:
			print(e)

	def StopRecording(self):
		try:
			self.ws.call(requests.StopRecording())
		except Exception as e:
			print(e)
		
	def ToggleRecording(self):
		try:
			self.ws.call(requests.StartStopRecording())
		except Exception as e:
			print(e)

	def PauseRecording(self): #untested
		try:
			self.ws.call(requests.PauseRecording())
		except Exception as e:
			print(e)

	def ResumeRecording(self): #untested
		try:
			self.ws.call(requests.ResumeRecording())
		except Exception as e:
			print(e)

	def SetRecordingFolder(self, path):
		try:
			self.ws.call(requests.SetRecordingFolder(path))
		except Exception as e:
			print(e)


	#	
	#	Replay Buffer (not sure what it does)
	#
	def StartReplayBuffer(self): #untested
		try:
			self.ws.call(requests.StartReplayBuffer())
		except Exception as e:
			print(e)

	def StopReplayBuffer(self): #untested
		try:
			self.ws.call(requests.StopReplayBuffer())
		except Exception as e:
			print(e)
		
	def ToggleReplayBuffer(self): #untested
		try:
			self.ws.call(requests.StartStopReplayBuffer())
		except Exception as e:
			print(e)

	def SaveReplayBuffer(self): #untested
		try:
			self.ws.call(requests.SaveReplayBuffer())
		except Exception as e:
			print(e)


	#
	#	Scene Items (to do)
	#
	#GetSceneItemProperties
	#SetSceneItemProperties
	#ResetSceneItem
	#DeleteSceneItem
	

	#	
	#	Scenes
	#
	def ListScenes(self):
		try:
			return self.ws.call(requests.GetSceneList()).__dict__["datain"]["scenes"]
		except Exception as e:
			print(e)
	
	def GetCurrentScene(self):
		try:
			return self.ws.call(requests.GetCurrentScene()).__dict__["datain"]
		except Exception as e:
			print(e)

	def SetCurrentScene(self, SceneName): #weird message i can't explain
		try:
			temp = requests.SetCurrentScene(SceneName)
			print(0)
			self.ws.call(temp)
		except Exception as e:
			print(e)

	#ReorderSceneItems
	
	def SetSceneTransitionOverride(self, SceneName, TransitionName, Duration = None): #untested
		try:
			if Duration == None:
				self.ws.call(requests.SetSceneTransitionOverride(SceneName, TransitionName))
			else:
				self.ws.call(requests.SetSceneTransitionOverride(SceneName, TransitionName, Duration))
		except Exception as e:
			print(e)

	def RemoveSceneTransitionOverride(self): #untested
		try:
			self.ws.call(requests.RemoveSceneTransitionOverride())
		except Exception as e:
			print(e)


	#
	#	Sources
	#
	def ListSources(self):
		try:
			return self.ws.call(requests.GetSourcesList()).__dict__["datain"]["sources"]
		except Exception as e:
			print(e)

	def GetSourceVolume(self, SourceName):
		try:
			return self.ws.call(requests.GetVolume(SourceName)).__dict__["datain"]["volume"]
		except Exception as e:
			print(e)

	def SetSourceVolume(self, SourceName, volume):
		try:
			self.ws.call(requests.SetVolume(SourceName, volume))
		except Exception as e:
			print(e)

	def GetSourceMute(self, SourceName):
		try:
			return self.ws.call(requests.GetMute(SourceName)).__dict__["datain"]["muted"]
		except Exception as e:
			print(e)

	def SetSourceMute(self, SourceName, muteBool):
		try:
			self.ws.call(requests.SetMute(SourceName, muteBool))
		except Exception as e:
			print(e)

	def ToggleSourceMute(self, SourceName):
		try:
			self.ws.call(requests.ToggleMute(SourceName))
		except Exception as e:
			print(e)

	def GetSourceSyncOffset(self, Sourcename): #untested
		try:
			return self.ws.call(requests.GetSyncOffset(SourceName))
		except Exception as e:
			print(e)

	def SetSourceSyncOffset(self, Sourcename, nsOffset): #untested
		try:
			self.ws.call(requests.SetSyncOffset(SourceName, nsOffset))
		except Exception as e:
			print(e)


	#
	#	Streaming
	#	
	def GetStreamingStatus(self):
		try:
			return self.ws.call(requests.GetStreamingStatus()).__dict__["datain"]["streaming"]
		except Exception as e:
			print(e)

	def StartStreaming(self):
		try:
			self.ws.call(requests.StartStreaming())
		except Exception as e:
			print(e)

	def StopStreaming(self):
		try:
			self.ws.call(requests.StopStreaming())
		except Exception as e:
			print(e)

	def StartStopStreaming(self):
		try:
			self.ws.call(requests.StartStopStreaming())
		except Exception as e:
			print(e)


	#
	#	Studio Mode
	#
	def GetStudioModeStatus(self):
		try:
			return self.ws.call(requests.GetStudioModeStatus()).__dict__["datain"]["studio-mode"]
		except Exception as e:
			print(e)

	def EnableStudioMode(self):
		try:
			return self.ws.call(requests.EnableStudioMode())
		except Exception as e:
			print(e)

	def DisableStudioMode(self):
		try:
			return self.ws.call(requests.DisableStudioMode())
		except Exception as e:
			print(e)

	def ToggleStudioMode(self):
		try:
			return self.ws.call(requests.ToggleStudioMode())
		except Exception as e:
			print(e)

	def GetPreviewScene(self):
		try:
			data = self.ws.call(requests.GetPreviewScene()).__dict__["datain"]
			if "error" in data:
				return None
			else:
				return data
		except Exception as e:
			print(e)

	def SetPreviewScene(self, SceneName):
		try:
			self.ws.call(requests.SetPreviewScene(SceneName))
		except Exception as e:
			print(e)

	def TransitionToProgram(self):
		try:
			self.ws.call(requests.TransitionToProgram())
		except Exception as e:
			print(e)


	#
	#	Transitions
	#
	def GetCurrentTransition(self):
		try:
			return self.ws.call(requests.GetCurrentTransition()).__dict__["datain"]["name"]
		except Exception as e:
			print(e)

	def SetCurrentTransition(self, TransitionName):
		try:
			self.ws.call(requests.SetCurrentTransition(TransitionName))
		except Exception as e:
			print(e)

	def GetTransitionDuration(self):
		try:
			return self.ws.call(requests.GetTransitionDuration()).__dict__["datain"]["transition-duration"]
		except Exception as e:
			print(e)

	def SetTransitionDuration(self, msDuration):
		try:
			self.ws.call(requests.SetTransitionDuration(msDuration))
		except Exception as e:
			print(e)





