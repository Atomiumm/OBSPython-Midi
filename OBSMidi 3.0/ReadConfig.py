from utilities import PrintWithTime, PrintError
import globalvars as GVar
import sys
import json


def getConfigName():
	#This allows us to either put the config name in the argv variables or to get asked for the config
	#Example: python ProgramName.py ConfigName
	if len(sys.argv) > 1:
		Filename = sys.argv[1]
	else:
		Filename = input("What is the name of your config file? --> ")
	if Filename == "":
		Filename = "FrequenceBanane"
	return Filename	

def openConfigFile(Filename):
	try:
		with open("Config\\" + Filename + ".json", "r") as f:
			SETUP_JSON = json.loads(''.join(f))
	except FileNotFoundError:
		PrintError("Config " + Filename + " not found")
		PrintError("Exiting program")
		exit()
	except Exception as e:
		PrintError("Couldn't open " + Filename + ".json")
		print(e)
		PrintError("Exiting program")
		exit()
	else:
		PrintWithTime("Opened config:  " + Filename)
		return SETUP_JSON

def updateGlobalVariables(SETUP_JSON):
	if "config_general" in SETUP_JSON:
		config_general = SETUP_JSON["config_general"]
		if "ConfigName" in config_general:
			GVar.ConfigName = config_general["ConfigName"]
		else:
			PrintError("ERROR 404:  ConfigName argument was not found")
		if "StudioModeDefault" in config_general:
			GVar.StudioModeDefault = config_general["StudioModeDefault"]
		else:
			PrintError("ERROR 404:  StudioModeDefault argument was not found")
		if "DefaultTransition" in config_general:
			GVar.DefaultTransition = config_general["DefaultTransition"]
		else:
			PrintError("ERROR 404:  DefaultTransition argument was not found")
		if "DefaultTransitionDuration" in config_general:
			GVar.DefaultTransitionDuration = config_general["DefaultTransitionDuration"]
		else:
			PrintError("ERROR 404:  DefaultTransitionDuration argument was not found")
		if "server_ip" in config_general:
			GVar.server_ip = config_general["server_ip"]
		else:
			PrintError("ERROR 404:  server_ip argument was not found")
		if "server_port" in config_general:
			GVar.server_port = config_general["server_port"]
		else:
			PrintError("ERROR 404:  server_port argument as not found")
		if "server_password" in config_general:
			GVar.server_password = config_general["server_password"]
		else:
			PrintError("ERROR 404  server_password argument was not found")
		if "SceneCollection" in config_general:
			GVar.SceneCollection = config_general["SceneCollection"]
		else:
			PrintError("ERROR 404  SceneCollection argument was not found")
		del config_general
	else:
		PrintError("No general config in config file")
	if "config_pad" in SETUP_JSON:
		GVar.config_pad = SETUP_JSON["config_pad"]
	else:
		PrintError("No pad config in config file")
		PrintError("Exiting program")
		exit()






Filename = getConfigName()
SETUP_JSON = openConfigFile(Filename)
del Filename
updateGlobalVariables(SETUP_JSON)
del SETUP_JSON
