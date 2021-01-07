from obswebsocket import obsws, requests
import time
# https://github.com/Palakis/obs-websocket/blob/4.x-current/docs/generated/protocol.md#getversion


def PrintWithTime(Text):
    print("[" + time.strftime("%H:%M:%S", time.localtime()) + "]", end="	")
    print(Text)


class OBSObject(object):
    # To add:
    #	SceneItems
    def __init__(self, server_ip, server_port, server_password, bypassexit=False):
        try:
            self.ws = obsws(server_ip, server_port, server_password)
            self.ws.connect()
        except Exception as e:
            PrintWithTime(f"Connection to OBS Websocket is impossible. Error: {e}")
        else:
            PrintWithTime("Connected to Websocket")

    #
    #	Profiles
    #

    def Profile_Set(self, ProfileName="", *args, **kwargs):
        try:
            self.ws.call(requests.SetCurrentProfile(ProfileName))
            PrintWithTime(f"Set OBS profile to {ProfileName}")
        except Exception as e:
            PrintWithTime(f"Couldn't set OBS profile to {ProfileName}. Error : {e}")

    #
    #	Scene Collections
    #

    def SceneCollection_Set(self, SceneCollectionName="", *args, **kwargs):
        try:
            self.ws.call(requests.SetCurrentSceneCollection(
                SceneCollectionName))
            PrintWithTime(f"Set scene collection to {SceneCollectionName}")
        except Exception as e:
            PrintWithTime(f"Couldn't set scene collection to {SceneCollectionName}. Error : {e}")

    #
    #	Scenes
    #

    def Scene_Set(self, SceneName="", *args, **kwargs): #Gives weird message but works
        try:
            self.ws.call(requests.SetCurrentScene(SceneName))
            PrintWithTime(f"Set scene to {SceneName}")
        except Exception as e:
            PrintWithTime(f"Couldn't set scene to {SceneName}. Error : {e}")

    def Scene_Set_Safe(self, SceneName="", *args, **kwargs):
    	try:
    		r = self.ws.call(requests.GetStudioModeStatus())
    		r = r.__dict__["datain"]
    		if r["studio-mode"]:
    			self.StudioMode_SetPreview(SceneName = SceneName, *args, **kwargs)
    		else:
    			self.Scene_Set(SceneName = SceneName, *args, **kwargs)
    	except Exception as e:
    		PrintWithTime(f"Couldn't get studio mode status. Error : {e}")

    #
    #	Transition
    #

    def Transition_Set(self, TransitionName="", *args, **kwargs):
        try:
            self.ws.call(requests.SetCurrentTransition(TransitionName))
            PrintWithTime(f"Set transition to {TransitionName}")
        except Exception as e:
            PrintWithTime(f"Couldn't set transition to {TransitionName}. Error : {e}")

    def Transition_SetDuration(self, duration, *args, **kwargs):
        try:
            duration = duration / 127
            minduration = 0
            maxduration = 1000
            if "MinDuration" in kwargs:
            	minduration = kwargs["MinDuration"]
            if "MaxDuration" in kwargs:
            	maxduration = kwargs["MaxDuration"]
            duration = minduration + duration * (maxduration - minduration)
            self.ws.call(requests.SetTransitionDuration(duration))
            PrintWithTime(f"Set transition duration to {duration}")
        except Exception as e:
            PrintWithTime(f"Couldn't set transition duration to {duration}. Error : {e}")

    #
    #	Studio Mode
    #

    def StudioMode_Enable(self, *args, **kwargs):
        try:
            self.ws.call(requests.EnableStudioMode())
            PrintWithTime(f"Enabled Studio Mode")
        except Exception as e:
            PrintWithTime(f"Couldn't enable Studio Mode. Error : {e}")

    def StudioMode_Disable(self, *args, **kwargs):
        try:
            self.ws.call(requests.DisableStudioMode())
            PrintWithTime(f"Disabled Studio Mode")
        except Exception as e:
            PrintWithTime(f"Couldn't disable Studio Mode. Error : {e}")

    def StudioMode_Toggle(self, *args, **kwargs):
        try:
            self.ws.call(requests.ToggleStudioMode())
            PrintWithTime(f"Toggled Studio Mode")
        except Exception as e:
            PrintWithTime(f"Couldn't toggle Studio Mode. Error : {e}")

    def StudioMode_SetPreview(self, SceneName="", *args, **kwargs):
        try:
            self.ws.call(requests.SetPreviewScene(SceneName))
            PrintWithTime(f"Set preview to {SceneName}")
        except Exception as e:
            PrintWithTime(f"Couldn't set preview to {SceneName}. Error : {e}")

    def StudioMode_Transition(self, *args, **kwargs):
        try:
            self.ws.call(requests.TransitionToProgram())
            PrintWithTime(f"Transitioned")
        except Exception as e:
            PrintWithTime(f"Couldn't transition. Error : {e}")

    #
    #	Recording
    #

    def Recording_Toggle(self, *args, **kwargs):
        try:
            self.ws.call(requests.StartStopRecording())
            PrintWithTime(f"Toggled recording")
        except Exception as e:
            PrintWithTime(f"Couldn't toggle recording. Error : {e}")

    def Recording_Start(self, *args, **kwargs):
        try:
            self.ws.call(requests.StartRecording())
            PrintWithTime(f"Started recording")
        except Exception as e:
            PrintWithTime(f"Couldn't start recording. Error : {e}")

    def Recording_Stop(self, *args, **kwargs):
        try:
            self.ws.call(requests.StopRecording())
            PrintWithTime(f"Stopped recording")
        except Exception as e:
            PrintWithTime(f"Couldn't stop recording. Error : {e}")

    def Recording_Pause(self, *args, **kwargs):
        try:
            self.ws.call(requests.PauseRecording())
            PrintWithTime(f"Paused recording")
        except Exception as e:
            PrintWithTime(f"Couldn't pause recording. Error : {e}")

    def Recording_Resume(self, *args, **kwargs):
        try:
            self.ws.call(requests.ResumeRecording())
            PrintWithTime(f"Resumed recording")
        except Exception as e:
            PrintWithTime(f"Couldn't resume recording. Error : {e}")

    #
    #	Streaming
    #

    def Streaming_Toggle(self, *args, **kwargs):
        try:
            self.ws.call(requests.StartStopStreaming())
            PrintWithTime(f"Toggled streaming")
        except Exception as e:
            PrintWithTime(f"Couldn't toggle streaming. Error : {e}")

    def Streaming_Start(self, *args, **kwargs):
        try:
            self.ws.call(requests.StartStreaming())
            PrintWithTime(f"Started streaming")
        except Exception as e:
            PrintWithTime(f"Couldn't start streaming. Error : {e}")

    def Streaming_Stop(self, *args, **kwargs):
        try:
            self.ws.call(requests.StopStreaming())
            PrintWithTime(f"Stopped streaming")
        except Exception as e:
            PrintWithTime(f"Couldn't stop streaming. Error : {e}")

    #
    #	Sources
    #

    def Sources_SetVolume(self, volume, SourceName="", *args, **kwargs): #Not tested
        try:
            volume = volume / 127
            minvolume = 0
            maxvolume = 1
            if "MinVolume" in kwargs:
            	minvolume = kwargs["MinVolume"]
            if "MaxVolume" in kwargs:
            	maxvolume = kwargs["MaxVolume"]
            volume = minvolume + volume * (maxvolume - minvolume)
            self.ws.call(requests.SetVolume(SourceName, volume))
            PrintWithTime(f"Set volume of source {SourceName} to {volume}")
        except Exception as e:
            PrintWithTime(f"Couldn't set volume of source {SourceName} to {volume}. Error : {e}")

    def Sources_SetMute(self, muteStatus = True, SourceName="", *args, **kwargs): # Not tested
        try:
            self.ws.call(requests.SetMute(SourceName, muteStatus))
            PrintWithTime(f"Set mute of source {SourceName} to {muteStatus}")
        except Exception as e:
            PrintWithTime(f"Couldn't set mute of source {SourceName} to {muteStatus}. Error : {e}")

    def Sources_ToggleMute(self, SourceName="", *args, **kwargs): #Not tested
        try:
            self.ws.call(requests.ToggleMute(SourceName))
            PrintWithTime(f"Toggled mute of source {SourceName}")
        except Exception as e:
            PrintWithTime(f"Couldn't toggle mute of source {SourceName}. Error : {e}")
