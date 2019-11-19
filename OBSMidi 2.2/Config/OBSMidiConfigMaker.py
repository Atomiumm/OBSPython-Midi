from guizero import *



def Open_BC(value):
	if value != "":
		BC.show(wait=True)
		print(value)

def Open_FC(value):
	if value != "":
		FC.show(wait=True)
		print(value)

def ChangeLayerA():
	LayerA.disable()
	if ButtonOrFader.value_text == "Buttons":
		Button0.text  = "0"
		Button1.text  = "1"
		Button2.text  = "2"
		Button3.text  = "3"
		Button4.text  = "4"
		Button5.text  = "5"
		Button6.text  = "6"
		Button7.text  = "7"
		Button8.text  = "8"
		Button9.text  = "9"
		Button10.text = "10"
		Button11.text = "11"
		Button12.text = "12"
		Button13.text = "13"
		Button14.text = "14"
		Button15.text = "15"
		Button16.text = "16"
		Button17.text = "17"
		Button18.text = "18"
		Button19.text = "19"
		Button20.text = "20"
		Button21.text = "21"
		Button22.text = "22"
		Button23.text = "23"
		Fader9.text   = ""
	else:
		Fader1.text   = "1"
		Fader2.text   = "2"
		Fader3.text   = "3"
		Fader4.text   = "4"
		Fader5.text   = "5"
		Fader6.text   = "6"
		Fader7.text   = "7"
		Fader8.text   = "8"
		Fader9.text   = "9"
		Button8.text  = ""
		Button9.text  = ""
		Button10.text = ""
		Button11.text = ""
		Button12.text = ""
		Button13.text = ""
		Button14.text = ""
		Button15.text = ""
		Button16.text = ""
		Button17.text = ""
		Button18.text = ""
		Button19.text = ""
		Button20.text = ""
		Button21.text = ""
		Button22.text = ""
		Button23.text = ""
	LayerB.enable()

def ChangeLayerB():
	LayerB.disable()
	if ButtonOrFader.value_text == "Buttons":
		Button0.text  = "24"
		Button1.text  = "25"
		Button2.text  = "26"
		Button3.text  = "27"
		Button4.text  = "28"
		Button5.text  = "29"
		Button6.text  = "30"
		Button7.text  = "31"
		Button8.text  = "32"
		Button9.text  = "33"
		Button10.text = "34"
		Button11.text = "35"
		Button12.text = "36"
		Button13.text = "37"
		Button14.text = "38"
		Button15.text = "39"
		Button16.text = "40"
		Button17.text = "41"
		Button18.text = "42"
		Button19.text = "43"
		Button20.text = "44"
		Button21.text = "45"
		Button22.text = "46"
		Button23.text = "47"
		Fader9.text   = ""
	else:
		Fader1.text   = "11"
		Fader2.text   = "12"
		Fader3.text   = "13"
		Fader4.text   = "14"
		Fader5.text   = "15"
		Fader6.text   = "16"
		Fader7.text   = "17"
		Fader8.text   = "18"
		Fader9.text   = "10"
		Button8.text  = ""
		Button9.text  = ""
		Button10.text = ""
		Button11.text = ""
		Button12.text = ""
		Button13.text = ""
		Button14.text = ""
		Button15.text = ""
		Button16.text = ""
		Button17.text = ""
		Button18.text = ""
		Button19.text = ""
		Button20.text = ""
		Button21.text = ""
		Button22.text = ""
		Button23.text = ""

	LayerA.enable()

def ToggleButtonsFaders(value):
	if value == "Buttons":
		Fader1.hide()
		Fader2.hide()
		Fader3.hide()
		Fader4.hide()
		Fader5.hide()
		Fader6.hide()
		Fader7.hide()
		Fader8.hide()
		Button0.show()
		Button1.show()
		Button2.show()
		Button3.show()
		Button4.show()
		Button5.show()
		Button6.show()
		Button7.show()
	else:
		Fader1.show()
		Fader2.show()
		Fader3.show()
		Fader4.show()
		Fader5.show()
		Fader6.show()
		Fader7.show()
		Fader8.show()
		Button0.hide()
		Button1.hide()
		Button2.hide()
		Button3.hide()
		Button4.hide()
		Button5.hide()
		Button6.hide()
		Button7.hide()
		
	if LayerA.enabled == True:
		ChangeLayerB()
	else:
		ChangeLayerA()







MAIN = App(title="Config Maker", layout="auto")

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
Fader1.hide()
Fader2.hide()
Fader3.hide()
Fader4.hide()
Fader5.hide()
Fader6.hide()
Fader7.hide()
Fader8.hide()

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

LayerA   = PushButton(PAD, text="LA", grid=[9, 1, 1, 2], command=ChangeLayerA, width=2, height=1, enabled=False)
LayerB   = PushButton(PAD, text="LB", grid=[9, 3, 1, 2], command=ChangeLayerB, width=2, height=1, enabled=True)

ButtonOrFader = ButtonGroup(PAD, options=["Buttons", "Faders"], grid=[0, 6, 9, 1], selected="Buttons", horizontal=True, command=lambda:ToggleButtonsFaders(ButtonOrFader.value_text))



BC = Window(MAIN, title="Button Config")
BC.hide()



FC = Window(MAIN, title="Fader Config")
FC.hide()







MAIN.display()