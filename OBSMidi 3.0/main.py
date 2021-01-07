from utilities import PrintWithTime, PrintError
import globalvars as GVar
from MidiPad import MidiPad
from OBSObject import OBSObject
import time


if __name__ == "__main__":
    PrintWithTime("Program started")
    import ReadConfig  # This updates all global variables
    XTouch = MidiPad(Input=1, Output=3,
                     PadConfig=GVar.config_pad, bypassexit=True)
    WS = OBSObject(GVar.server_ip, GVar.server_port,
                   GVar.server_password, bypassexit=True)

    WS.ws.disconnect()
