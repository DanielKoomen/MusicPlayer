import sys, os, requests, json
from colorthief import ColorThief
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO


def block_print():
    sys.stdout = open(os.devnull, 'w')


def enable_print():
    sys.stdout = sys.__stdout__

block_print()
import pygame
enable_print()



global folder_string, file_name

color_text = (255, 255, 255)
red = (255, 0, 0)
color_light = (170, 170, 170)
color_dark = (100, 100, 100)



def find_dominant_color():
    global folder_string, file_name
    color_thief = ColorThief(folder_string + "/" + file_name)
    dominant_color = color_thief.get_color(quality=1)
    return dominant_color


def button(screen, position, text, color, font_size, button_size, state=False):
    pygame.font.init()
    font = pygame.font.Font("resources/seguisym.ttf", font_size)
    if state:
        text_render = font.render(text, 1, red)
    else:
        text_render = font.render(text, 1, color_text)
    text_x, text_y, w , h = text_render.get_rect()
    x, y = position
    text_x = x + ((button_size - w) / 2)
    text_y = y + ((button_size - h) / 2)
    pygame.draw.rect(screen, color, (x, y, button_size, button_size))
    return screen.blit(text_render, (text_x, text_y))


def screen():
    global folder_string, file_name
    image_size = 500

    pygame.init()
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    image = pygame.image.load(folder_string + "/" + file_name)
    vignette = pygame.image.load("resources/vignette.png")
    vignette.set_alpha(100)
    fill_color = find_dominant_color()
    w, h = screen.get_size()

    CB = False
    DK = False
    JK = False
    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        screen.fill(fill_color)
        vignette = pygame.transform.scale(vignette, (w, h))
        screen.blit(vignette, (0, 0))
        image_height = image.get_height()
        image_width = image.get_width()
        new_size = min(image_height, image_width)
        image = image.subsurface(((image_width / 2) - (new_size / 2),
                                  (image_height / 2) - (new_size / 2),
                                  (image_width / 2) + (new_size / 2),
                                  (image_height / 2) + (new_size / 2)))
        image = pygame.transform.scale(image, (image_size, image_size))
        screen.blit(image, ((w / 2) - (image_size / 2),
                            (h / 2) - (image_size / 2)))

        # parameters for buttons
        button_font_size = 90
        button_size = 120
        offset_y = 25
        left = ((w / 2) - (new_size / 2))
        right = ((w / 2) + (new_size / 2) - button_size)
        top = (h / 2) - (new_size / 2) - offset_y - button_size
        bottom = (h / 2) + (new_size / 2) + offset_y
        offset_x = (right - left) / 2

        # creating buttons
        CB_button = button(screen, (left, top), "CB", color_dark, button_font_size, button_size, CB)
        DK_button = button(screen, (left + offset_x, top), "DK", color_dark, button_font_size, button_size, DK)
        JK_button = button(screen, (right, top), "JK", color_dark, button_font_size, button_size, JK)

        back_button = button(screen, (left, bottom), "\u23EE", color_dark, button_font_size, button_size)
        pp_button = button(screen, (left + offset_x, bottom), "\u23EF", color_dark, button_font_size, button_size)
        fw_button = button(screen, (right, bottom), "\u23ED", color_dark, button_font_size, button_size)

        # hoovering for buttons
        if (CB_button.collidepoint(mouse)):
            CB_button = button(screen, (left, top), "CB", color_light, button_font_size, button_size, CB)
        if (DK_button.collidepoint(mouse)):
            DK_button = button(screen, (left + offset_x, top), "DK", color_light, button_font_size, button_size, DK)
        if (JK_button.collidepoint(mouse)):
            JK_button = button(screen, (right, top), "JK", color_light, button_font_size, button_size, JK)

        if (back_button.collidepoint(mouse)):
            back_button = button(screen, (left, bottom), "\u23EE", color_light, button_font_size, button_size)
        if (pp_button.collidepoint(mouse)):
            pp_button = button(screen, (left + offset_x, bottom), "\u23EF", color_light, button_font_size, button_size)
        if (fw_button.collidepoint(mouse)):
            fw_button = button(screen, (right, bottom), "\u23ED", color_light, button_font_size, button_size)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (CB_button.collidepoint(mouse)):
                    CB = False if CB else True
                if (DK_button.collidepoint(mouse)):
                    DK = False if DK else True
                if (JK_button.collidepoint(mouse)):
                    JK = False if JK else True

        pygame.display.update()

    pygame.quit()


def download_image(search):
    global folder_string, file_name
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

    folder_string = "./scraped_images"
    file_name = title


def main():
    global folder_string, file_name
    search = "Sultans of swing dire straits"
    try:
        download_image(search)
    except:
        folder_string = "./resources"
        file_name = "Raphson.PNG"
    screen()


if __name__ == '__main__':
    main()
