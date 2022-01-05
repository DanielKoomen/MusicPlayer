import threading, os, owncloud, time, vlc, sys, requests, json, tkinter as tk
from tkinter.constants import CENTER, NE, NW
import tkinter.font as font
# import tkMessageBox
from random import randint
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
from io import BytesIO
from colorthief import ColorThief
import webcolors

from gui import button

global player, skip_bool, stop_bool, file_name, file_location, image_title
global window, screen_width, screen_height, image_size, button_size, playlists
skip_bool = False
stop_bool = True
image_title = "Raphson.PNG"

screen_width = 1920
screen_height = 1080
image_size = 500
button_size = 120
offset_y = 25
left = ((screen_width / 2) - (image_size / 2))
right = ((screen_width / 2) + (image_size / 2)) - button_size - 27.5
top = (screen_height / 2) - (image_size / 2) - offset_y - button_size - 17
bottom = (screen_height / 2) + (image_size / 2) + offset_y
offset_x = (right - left) / 2

playlists = {"CB" : True, "DK" : True, "JK" : True}


def download_image(search):
    global image_title, window
    url = "https://www.bing.com/images/search"

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0"
    }
    params = {"q": search, "form": "HDRSC2", "first": "1", "scenario": "ImageBasicHover"}
    r = requests.get(url, headers=headers, params=params)

    soup = BeautifulSoup(r.text, "html.parser")

    data = soup.find_all("a", {"class": "iusc"})[0]
    json_data = json.loads(data["m"])
    img_link = json_data["murl"]
    img_object = requests.get(img_link, headers=headers)
    title = img_link.split("/")[-1]
    title = "temp." + title.split(".")[-1]

    img = Image.open(BytesIO(img_object.content))
    img.save("./scraped_images/" + title)

    image_title = title


def find_dominant_color():
    global image_title
    color_thief = ColorThief("scraped_images/" + image_title)
    dominant_color = color_thief.get_color(quality=1)
    return webcolors.rgb_to_hex(dominant_color)


def start_music():
    global skip_bool, stop_bool, player, file_name, file_location, window
    global image_title, screen_width, screen_heigth, image_size, playlists

    # oc = owncloud.Client('http://192.168.1.109')
    # oc.login('MusicLaptop', '5pzZ4-cLNTg-kj24x-8FBes-YC38R')

    dirList = ['DK', 'JK', 'CB']
    i = randint(0, len(dirList)-1)
    startCount = i

    # play music
    while stop_bool:
        # dir_name = dirList[i % len(dirList)]
        # randomNum = randint(0, len(oc.list('Music/' + dir_name))-1)
        # file_name = (oc.list('Music/' + dir_name)[randomNum]).name

        dir_name = 'CB'
        # file_name = "82_44 Hall & Oates - Private Eyes.mp3"
        file_name = "179 Herman Brood & His Wild Romance - Saturday Night.mp3"
        # file_name = "07 R.E.M. - Losing My Religion.mp3"
        try:
            download_image(file_name)
        except:
            image_title = "Raphson.PNG"
        window.configure(bg=find_dominant_color())


        img = Image.open("scraped_images/" + image_title)
        img = img.resize((image_size, image_size))
        img = ImageTk.PhotoImage(img)
        label = tk.Label(window, image=img, bd=-2)
        # label.pack()
        label.place(x=1920/2, y=1080/2, anchor=CENTER)

        # oc.get_file('Music/' + dir_name + "/" + file_name, 'temp.mp3')
        # #loc = os.path.dir_name(os.path.realpath(__file__))
        print("Currently playing: \"" + file_name.rstrip(".mp3") +"\" from folder " + dir_name + ", " + str(i - startCount + 1) + " played in this sesh.")
        # playsound(loc+'/temp.mp3')
        start_time = time.time()
        # player = vlc.MediaPlayer('temp.mp3')
        player = vlc.MediaPlayer("Music/" + dir_name + "/" + file_name)
        player.play()

        time.sleep(0.5)
        duration = player.get_length()/1000
        # thread = threading.Thread(target=input_function)
        # thread.start()
        while(skip_bool == False and ((time.time() - start_time) < duration)):
            print(playlists["CB"], playlists["DK"], playlists["JK"])
            time.sleep(1)
            pass
        player.stop()
        skip_bool = False
        i += 1


def close(event):
    """
    Close the window.
    """
    global player, stop_bool, skip_bool
    player.stop()
    skip_bool = True
    stop_bool = False
    window.destroy()
    os._exit(1)


def change_state(directory):
    global playlists
    playlists[directory] = False if playlists[directory] else True


if __name__ == '__main__':
    window = tk.Tk()
    window.geometry("1920x1080")
    window.attributes("-fullscreen", True)
    window.bind("<Escape>", close)

    music_thread = threading.Thread(target=start_music)
    music_thread.start()

    # creating buttons
    empty_img = tk.PhotoImage(width=10, height=10)
    button_font = font.Font(family="Roboto", size=45)

    CB_button = tk.Button(window, text="CB", font=button_font, command=lambda : change_state("CB"))
    CB_button.config(height=button_size, width=button_size, image=empty_img, compound=CENTER)

    DK_button = tk.Button(window, text="DK", font=button_font, command=lambda : change_state("DK"))
    DK_button.config(height=button_size, width=button_size, image=empty_img, compound=CENTER)

    JK_button = tk.Button(window, text="JK", font=button_font, command=lambda : change_state("JK"))
    JK_button.config(height=button_size, width=button_size, image=empty_img, compound=CENTER)

    RW_button = tk.Button(window, text='\u23EE', font=button_font)
    RW_button.config(height=button_size, width=button_size, image=empty_img, compound=CENTER)

    PP_button = tk.Button(window, text='\u23EF', font=button_font)
    PP_button.config(height=button_size, width=button_size, image=empty_img, compound=CENTER)

    FF_button = tk.Button(window, text='\u23ED', font=button_font)
    FF_button.config(height=button_size, width=button_size, image=empty_img, compound=CENTER)

    # placing buttons
    CB_button.place(x=left, y=top, anchor=NW)
    DK_button.place(x=left + offset_x, y=top, anchor=NW)
    JK_button.place(x=right, y=top, anchor=NW)
    RW_button.place(x=left, y=bottom, anchor=NW)
    PP_button.place(x=left + offset_x, y=bottom, anchor=NW)
    FF_button.place(x=right, y=bottom, anchor=NW)

    window.mainloop()
