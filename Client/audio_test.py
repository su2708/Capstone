from playsound import playsound
import multiprocessing
import time

alarm1 = '/home/pi4/Music/Alarm1.mp3'
alarm2 = '/home/pi4/Music/Alarm2.mp3'

def turn_on_alarm1():
	playsound(alarm1)
	
def turn_on_alarm2():
	playsound(alarm2)
		
def main():
	turn_on_alarm1()
	turn_on_alarm2()
	
if __name__ == "__main__":
	main()

