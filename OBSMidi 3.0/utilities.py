import time


def PrintWithTime(Text):
	print("[" + time.strftime("%H:%M:%S", time.localtime()) + "]", end = "	")
	print(Text) 


def PrintError(Text):
	print("ERROR", end = "	")
	PrintWithTime(Text)
