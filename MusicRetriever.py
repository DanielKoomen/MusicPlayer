import owncloud, os, time, vlc, threading
from playsound import playsound
from random import randint

global player
global skip_bool
skip_bool = False

def input_function():
    input()
    global skip_bool
    skip_bool = True
    player.stop()

oc = owncloud.Client('http://192.168.1.109')
oc.login('MusicLaptop', '5pzZ4-cLNTg-kj24x-8FBes-YC38R')

os.environ["VLC_VERBOSE"] = str("-1")

dirList = ['DK', 'JK', 'CB']
i = randint(0, len(dirList)-1)
startCount = i

while True:
    dirName = dirList[i % len(dirList)]
    randomNum = randint(0, len(oc.list('Music/' + dirName))-1)
    fileName = (oc.list('Music/' + dirName)[randomNum]).name
    oc.get_file('Music/' + dirName + "/" + fileName, 'temp.mp3')
    loc = os.path.dirname(os.path.realpath(__file__))
    print("Currently playing: \"" + fileName.rstrip(".mp3") +"\" from folder " + dirName + ", " + str(i - startCount + 1) + " played in this sesh.")
    # playsound(loc+'/temp.mp3')
    start_time = time.time()
    player = vlc.MediaPlayer('temp.mp3')
    player.play()

    time.sleep(0.5)
    duration = player.get_length()/1000
    thread = threading.Thread(target=input_function)
    thread.start()
    while(skip_bool == False and ((time.time() - start_time) < duration)):
        pass
    player.stop()
    skip_bool = False
    i += 1
