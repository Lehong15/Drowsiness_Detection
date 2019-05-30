import time
from pygame import mixer 

def warning(a):
	num = 2
	while num:
		voice_warning(a)
		time.sleep(5)
		num -= 1


def voice_warning(a):
	mixer.init()
	mixer.music.load('..\\tools\\'+ str(a) + '.mp3')	
	mixer.music.play()
	time.sleep(10)
	mixer.music.stop()




