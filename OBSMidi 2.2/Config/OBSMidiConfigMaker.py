from guizero import *


JSON = {
	"config_general" : {
		"server_ip" : "localhost",
		"server_port" : 4444,
		"server_password" : "banana",
		},
	"config_pad" : {
		"Buttons":{

		},
		"Faders":{

		}
	}
}



def Open_BC(value):
	if value != "":
		BCNumber.value = "Button " + str(value)
		BC.show(wait=True)

def Open_FC(value):
	if value != "":
		FCNumber.value = "Fader " + str(value)
		FC.show(wait=True)


def ChangeLayerA():
	LayerA.disable()
	if ButtonOrFader.value_text == "Buttons":
		for i in range(0, 24):
			Buttons[i].text = str(i)
		Fader9.text = ""
	else:
		for i in range(0, 9):
			Faders[i].text = str(i + 1)
		for i in range(8, 24):
			Buttons[i].text = ""
	LayerB.enable()

def ChangeLayerB():
	LayerB.disable()
	if ButtonOrFader.value_text == "Buttons":
		for i in range(0, 24):
			Buttons[i].text = str(i + 24)
		Fader9.text   = ""
	else:
		for i in range(0, 8):
			Faders[i].text = str(i + 11)
		Fader9.text   = "10"
		for i in range(8, 24):
			Buttons[i].text = ""
	LayerA.enable()

def ToggleButtonsFaders(value):
	if value == "Buttons":
		for i in range(0, 8):
			Faders[i].hide()
		for i in range(0, 8):
			Buttons[i].show()
	else:
		for i in range(0, 8):
			Faders[i].show()
		for i in range(0, 8):
			Buttons[i].hide()

	if LayerA.enabled == True:
		ChangeLayerB()
	else:
		ChangeLayerA()







MAIN = App(title="Config Maker", layout="auto")

CONFIGNAMEBox = Box(MAIN, align="top", layout="grid")
CONFIGNAMEText = Text(CONFIGNAMEBox, grid=[0, 0], text="Name of configuration: ", size=15, width=20, height=3)
CONFIGNAME = TextBox(CONFIGNAMEBox, grid=[1, 0], width=20, height=3)

PAD = Box(MAIN, align="top", layout="grid")

Fader1   = PushButton(PAD, text="1", grid=[0, 0, 1, 2], command=lambda:Open_FC(Fader1.text), width=2, height=1)
Fader2   = PushButton(PAD, text="2", grid=[1, 0, 1, 2], command=lambda:Open_FC(Fader2.text), width=2, height=1)
Fader3   = PushButton(PAD, text="3", grid=[2, 0, 1, 2], command=lambda:Open_FC(Fader3.text), width=2, height=1)
Fader4   = PushButton(PAD, text="4", grid=[3, 0, 1, 2], command=lambda:Open_FC(Fader4.text), width=2, height=1)
Fader5   = PushButton(PAD, text="5", grid=[4, 0, 1, 2], command=lambda:Open_FC(Fader5.text), width=2, height=1)
Fader6   = PushButton(PAD, text="6", grid=[5, 0, 1, 2], command=lambda:Open_FC(Fader6.text), width=2, height=1)
Fader7   = PushButton(PAD, text="7", grid=[6, 0, 1, 2], command=lambda:Open_FC(Fader7.text), width=2, height=1)
Fader8   = PushButton(PAD, text="8", grid=[7, 0, 1, 2], command=lambda:Open_FC(Fader8.text), width=2, height=1)
Fader9   = PushButton(PAD, text="",  grid=[8, 0, 1, 6], command=lambda:Open_FC(Fader9.text), width=2, height=7)
Faders   = [Fader1, Fader2, Fader3, Fader4, Fader5, Fader6, Fader7, Fader8, Fader9]
for i in range(0, 8):
	Faders[i].hide()

Button0  = PushButton(PAD, text="0",  grid=[0, 0, 1, 2], command=lambda:Open_BC(Button0.text),  width=2, height=1)
Button1  = PushButton(PAD, text="1",  grid=[1, 0, 1, 2], command=lambda:Open_BC(Button1.text),  width=2, height=1)
Button2  = PushButton(PAD, text="2",  grid=[2, 0, 1, 2], command=lambda:Open_BC(Button2.text),  width=2, height=1)
Button3  = PushButton(PAD, text="3",  grid=[3, 0, 1, 2], command=lambda:Open_BC(Button3.text),  width=2, height=1)
Button4  = PushButton(PAD, text="4",  grid=[4, 0, 1, 2], command=lambda:Open_BC(Button4.text),  width=2, height=1)
Button5  = PushButton(PAD, text="5",  grid=[5, 0, 1, 2], command=lambda:Open_BC(Button5.text),  width=2, height=1)
Button6  = PushButton(PAD, text="6",  grid=[6, 0, 1, 2], command=lambda:Open_BC(Button6.text),  width=2, height=1)
Button7  = PushButton(PAD, text="7",  grid=[7, 0, 1, 2], command=lambda:Open_BC(Button7.text),  width=2, height=1)
Button8  = PushButton(PAD, text="8",  grid=[0, 2, 1, 2], command=lambda:Open_BC(Button8.text),  width=2, height=1)
Button9  = PushButton(PAD, text="9",  grid=[1, 2, 1, 2], command=lambda:Open_BC(Button9.text),  width=2, height=1)
Button10 = PushButton(PAD, text="10", grid=[2, 2, 1, 2], command=lambda:Open_BC(Button10.text), width=2, height=1)
Button11 = PushButton(PAD, text="11", grid=[3, 2, 1, 2], command=lambda:Open_BC(Button11.text), width=2, height=1)
Button12 = PushButton(PAD, text="12", grid=[4, 2, 1, 2], command=lambda:Open_BC(Button12.text), width=2, height=1)
Button13 = PushButton(PAD, text="13", grid=[5, 2, 1, 2], command=lambda:Open_BC(Button13.text), width=2, height=1)
Button14 = PushButton(PAD, text="14", grid=[6, 2, 1, 2], command=lambda:Open_BC(Button14.text), width=2, height=1)
Button15 = PushButton(PAD, text="15", grid=[7, 2, 1, 2], command=lambda:Open_BC(Button15.text), width=2, height=1)
Button16 = PushButton(PAD, text="16", grid=[0, 4, 1, 2], command=lambda:Open_BC(Button16.text), width=2, height=1)
Button17 = PushButton(PAD, text="17", grid=[1, 4, 1, 2], command=lambda:Open_BC(Button17.text), width=2, height=1)
Button18 = PushButton(PAD, text="18", grid=[2, 4, 1, 2], command=lambda:Open_BC(Button18.text), width=2, height=1)
Button19 = PushButton(PAD, text="19", grid=[3, 4, 1, 2], command=lambda:Open_BC(Button19.text), width=2, height=1)
Button20 = PushButton(PAD, text="20", grid=[4, 4, 1, 2], command=lambda:Open_BC(Button20.text), width=2, height=1)
Button21 = PushButton(PAD, text="21", grid=[5, 4, 1, 2], command=lambda:Open_BC(Button21.text), width=2, height=1)
Button22 = PushButton(PAD, text="22", grid=[6, 4, 1, 2], command=lambda:Open_BC(Button22.text), width=2, height=1)
Button23 = PushButton(PAD, text="23", grid=[7, 4, 1, 2], command=lambda:Open_BC(Button23.text), width=2, height=1)
Buttons  = [Button0, Button1, Button2, Button3, Button4, Button5, Button6, Button7, Button8, Button9, Button10, Button11, Button12, Button13, Button14, Button15, Button16, Button17, Button18, Button19, Button20, Button21, Button22, Button23]

LayerA   = PushButton(PAD, text="LA", grid=[9, 1, 1, 2], command=ChangeLayerA, width=2, height=1, enabled=False)
LayerB   = PushButton(PAD, text="LB", grid=[9, 3, 1, 2], command=ChangeLayerB, width=2, height=1, enabled=True)

ButtonOrFader = ButtonGroup(PAD, options=["Buttons", "Faders"], grid=[0, 6, 9, 1], selected="Buttons", horizontal=True, command=lambda:ToggleButtonsFaders(ButtonOrFader.value_text))

GENERALCONFIG = Box(MAIN, align="top", layout="grid")
STUDIOMODEDEFAULTText = Text(GENERALCONFIG, grid=[0, 0], text="StudioMode default:", size=11)
STUDIOMODEDEFAULT = ButtonGroup(GENERALCONFIG, options=["True", "False"], grid=[1, 0], selected="False", horizontal=True,)
DEFAULTTRANSITIONText = Text(GENERALCONFIG, grid=[0, 1], text="Default transition:", size=11)
DEFAULTTRANSITION = ButtonGroup(GENERALCONFIG, options=["Cut", "Fade"], grid=[1, 1], selected="Cut", horizontal=True,)
DEFAULTTRANSITIONTRANSITIONDURATIONText = Text(GENERALCONFIG, grid=[0, 2], text="Default transition duration:", size=11)
DEFAULTTRANSITIONTRANSITIONDURATION = Slider(GENERALCONFIG, grid=[1, 2], start=0, end=2000, width=200)
SCENECOLLECTIONText = Text(GENERALCONFIG, grid=[0, 3], text="Scene collection:", size=11)
SCENECOLLECTION = TextBox(GENERALCONFIG, grid=[1, 3], width=25)



BC = Window(MAIN, title="Button Config")
BC.hide()
BCNumber = Text(BC, text="Button ", align="top", size=15)



FC = Window(MAIN, title="Fader Config")
FC.hide()
FCNumber = Text(BC, test="Fader ", align=top, size=15)







MAIN.display()
