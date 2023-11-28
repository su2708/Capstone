from playsound import playsound
import multiprocessing
import time

alarm1 = "../Music/Alarm1.mp3"
alarm2 = "../Music/Alarm2.mp3"

def turn_on_alarm1():
    play = multiprocessing.Process(target=playsound, args=(alarm1,))
    play.start()
    time.sleep(3)
    play.terminate()
    
def turn_on_alarm2():
    for i in range(3):
        playsound(alarm2)

def main():
    turn_on_alarm1()
    turn_on_alarm2()
    
if __name__ == "__main__":
    main()
    
