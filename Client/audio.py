from playsound import playsound
import subprocess
import time

alarm1 = '/home/pi4/Music/Alarm1.mp3'
alarm2 = '/home/pi4/Music/Alarm2.mp3'

def turn_on_alarm1():
	sp = subprocess.Popen(["vlc", alarm1], stdout=subprocess.PIPE)
	time.sleep(2)
	sp.terminate()
	
def turn_on_alarm2():
	sp = subprocess.Popen(["vlc", alarm2], stdout=subprocess.PIPE)
	time.sleep(2)
	sp.terminate()
		
def main():
	#turn_on_alarm1()
	turn_on_alarm2()
	
if __name__ == "__main__":
	main()
