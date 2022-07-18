from multiprocessing.connection import wait
import threading, os, owncloud, time, vlc, requests, json, webcolors, tkinter as tk
import tkinter.font as font, pyautogui
from tkinter.constants import CENTER, NW, SE, W
from random import randint
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
from io import BytesIO
from colorthief import ColorThief


global player, skip_bool, stop_bool, pp_bool
global file_name, file_location, playlists, previous_file_name


pp_bool = True
skip_bool = False
stop_bool = True

screen_width = 1366
screen_height = 768
# screen_width, screen_height = pyautogui.size()
image_size = int(screen_height / 3)
button_size = int(image_size / 4)
offset_y = 25
left = ((screen_width / 2) - (image_size / 2))
right = ((screen_width / 2) + (image_size / 2)) - button_size - 27.5
top = (screen_height / 2) - (image_size / 2) - offset_y - button_size - 17
bottom = (screen_height / 2) + (image_size / 2) + offset_y
offset_x = (right - left) / 2

playlists = {"CB" : True, "DK" : True, "JK" : True}


def get_image(search):
    try:
        url = "https://www.bing.com/images/search"

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0"
        }
        params = {"q": search.rstrip(".mp3"), "form": "HDRSC2", "first": "1", "scenario": "ImageBasicHover"}
        r = requests.get(url, headers=headers, params=params)

        soup = BeautifulSoup(r.text, "html.parser")

        data = soup.find_all("a", {"class": "iusc"})[0]
        json_data = json.loads(data["m"])
        img_link = json_data["murl"]
        r = requests.get(img_link, headers=headers)
        return r.content

    except:
        with open('scraped_images/Raphson.PNG', 'rb') as f:
            return f.readall()



def find_dominant_color(image):
    color_thief = ColorThief(BytesIO(image))
    dominant_color = color_thief.get_color(quality=1)
    return webcolors.rgb_to_hex(dominant_color)


def start_music():
    global skip_bool, stop_bool, player, file_name, file_location, window
    global image_title, screen_width, screen_height, image_size, playlists

    oc = owncloud.Client('http://raphson.rkslot.nl')
    oc.login('MusicLaptop', '5pzZ4-cLNTg-kj24x-8FBes-YC38R')

    i = randint(0, len(playlists) - 1)
    startCount = i

    previous_file_name = ""

    # play music
    while stop_bool:

        dir_list = []
        for x in playlists.keys():
            if playlists[x] == True:
                dir_list.append(x)
        if (len(dir_list) > 0):
            dir_name = dir_list[i % len(dir_list)]

        print('Download music')

        random_num = randint(0, len(oc.list('Music/' + dir_name))-1)
        file_name = (oc.list('Music/' + dir_name)[random_num]).name
        oc.get_file('Music/' + dir_name + "/" + file_name, 'temp.mp3')

        # Download and print image in center of screen.
        print('Download image')
        img = get_image(file_name)
        window.configure(bg=find_dominant_color(img))

        tk_img = ImageTk.PhotoImage(Image.open(BytesIO(img)).resize((image_size, image_size)))

        label = tk.Label(window, image=tk_img, bd=-2)
        label.place(x=screen_width / 2, y=screen_height / 2, anchor=CENTER)

        text_label1 = tk.Label(window, text="Currently playing: \"" + file_name.rstrip(".mp3") +"\" from folder " + dir_name + ", " + str(i - startCount + 1) + " played in this sesh.")
        text_label1.place(x=offset_y, y=screen_height / 2 - offset_y, anchor=W)

        text_label2 = tk.Label(window, text="Previously played: \"" + previous_file_name.rstrip(".mp3") + "\"")
        text_label2.place(x=offset_y, y=screen_height / 2, anchor=W)

        print("Currently playing: \"" + file_name.rstrip(".mp3") +"\" from folder " + dir_name + ", " + str(i - startCount + 1) + " played in this sesh.")
        start_time = time.time()
        player = vlc.MediaPlayer('temp.mp3')
        player.play()

        time.sleep(0.5)
        duration = player.get_length() / 1000

        time_played = time.time() - start_time
        while(skip_bool == False and (time_played < duration)):
            if (pp_bool == True):
                duration_label = tk.Label(window, text=duration - time_played)
                duration_label.place(x=screen_width / 2, y=screen_height - offset_y, anchor=CENTER)
                time.sleep(1)
                duration_label.destroy()
                time_played = time.time() - start_time
            else:
                duration_label = tk.Label(window, text=duration - time_played)
                duration_label.place(x=screen_width / 2, y=screen_height - offset_y, anchor=CENTER)
                time.sleep(1)
                duration_label.destroy()
                start_time += 1
        player.stop()
        text_label1.destroy()
        text_label2.destroy()
        skip_bool = False
        i += 1
        previous_file_name = file_name


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
    global playlists, CB_button, DK_button, JK_button
    if directory == "CB":
        if (playlists["CB"]):
            CB_button.config(height=button_size, width=button_size, bg='red', activebackground='red', image=empty_img, compound=CENTER)
            playlists["CB"] = False
        else:
            CB_button.config(height=button_size, width=button_size, bg='green', activebackground='green', image=empty_img, compound=CENTER)
            playlists["CB"] = True
    if directory == "DK":
        if (playlists["DK"]):
            DK_button.config(height=button_size, width=button_size, bg='red', activebackground='red', image=empty_img, compound=CENTER)
            playlists["DK"] = False
        else:
            DK_button.config(height=button_size, width=button_size, bg='green', activebackground='green', image=empty_img, compound=CENTER)
            playlists["DK"] = True
    if directory == "JK":
        if (playlists["JK"]):
            JK_button.config(height=button_size, width=button_size, bg='red', activebackground='red', image=empty_img, compound=CENTER)
            playlists["JK"] = False
        else:
            JK_button.config(height=button_size, width=button_size, bg='green', activebackground='green', image=empty_img, compound=CENTER)
            playlists["JK"] = True


def play_pause():
    global player, pp_bool
    if pp_bool:
        player.set_pause(1)
        pp_bool = False
    else:
        player.play()
        pp_bool = True


def skip():
    global skip_bool
    player.stop()
    skip_bool = True


if __name__ == '__main__':
    window = tk.Tk()
    window.title("Super fancy music player")
    screen_size = str(screen_width) + "x" + str(screen_height)
    window.geometry(screen_size)
    # window.attributes("-fullscreen", True)
    window.bind("<Escape>", close)

    # vignette = tk.PhotoImage(file="resources/vignette.png")
    # background_label = tk.Label(window, image=vignette)
    # background_label.pack()

    music_thread = threading.Thread(target=start_music)
    music_thread.start()

    # creating buttons
    empty_img = tk.PhotoImage(width=10, height=10)
    button_font = font.Font(family="Roboto", size=45)

    CB_button = tk.Button(window, text="CB", font=button_font, command=lambda : change_state("CB"), bd=-2)
    CB_button.config(height=button_size, width=button_size, bg='green', activebackground='green', image=empty_img, compound=CENTER)

    DK_button = tk.Button(window, text="DK", font=button_font, command=lambda : change_state("DK"), bd=-2)
    DK_button.config(height=button_size, width=button_size, bg='green', activebackground='green', image=empty_img, compound=CENTER)

    JK_button = tk.Button(window, text="JK", font=button_font, command=lambda : change_state("JK"), bd=-2)
    JK_button.config(height=button_size, width=button_size, bg='green', activebackground='green', image=empty_img, compound=CENTER)

    RW_button = tk.Button(window, text='RW', font=button_font, bd=-2)
    RW_button.config(height=button_size, width=button_size, image=empty_img, compound=CENTER)

    PP_button = tk.Button(window, text='PP', font=button_font, command=play_pause, bd=-2)
    PP_button.config(height=button_size, width=button_size, image=empty_img, compound=CENTER)

    FF_button = tk.Button(window, text='FF', font=button_font, command=skip, bd=-2)
    FF_button.config(height=button_size, width=button_size, image=empty_img, compound=CENTER)

    # placing buttons
    CB_button.place(x=left, y=top, anchor=NW)
    DK_button.place(x=left + offset_x, y=top, anchor=NW)
    JK_button.place(x=right, y=top, anchor=NW)
    RW_button.place(x=left, y=bottom, anchor=NW)
    PP_button.place(x=left + offset_x, y=bottom, anchor=NW)
    FF_button.place(x=right, y=bottom, anchor=NW)

    window.mainloop()
