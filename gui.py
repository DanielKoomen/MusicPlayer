import sys, os, requests, json, shutil
from bing_image_downloader import downloader
from colorthief import ColorThief
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO



def blockPrint():
    sys.stdout = open(os.devnull, 'w')


def enablePrint():
    sys.stdout = sys.__stdout__

blockPrint()
import pygame
enablePrint()

def findDominantColor(imageToCheck):
    global folderString, queryString, fileName
    color_thief = ColorThief(folderString + "/" + fileName)
    dominant_color = color_thief.get_color(quality=1)
    return dominant_color


global queryString, folderString, fileName
imageSize = 500

def screen():
    global queryString, folderString, fileName

    pygame.init()
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    image = pygame.image.load(folderString + "/" + fileName)
    vignette = pygame.image.load("resources/vignette.png")
    vignette.set_alpha(100)
    fill_color = findDominantColor(image)
    w, h = screen.get_size()

    running = True
    while running:

        screen.fill(fill_color)
        vignette = pygame.transform.scale(vignette, (w, h))
        screen.blit(vignette, (0, 0))
        imageHeight = image.get_height()
        imageWidth = image.get_width()
        newSize = min(imageHeight, imageWidth)
        image = image.subsurface((imageWidth/2-newSize/2, imageHeight/2-newSize/2, imageWidth/2+newSize/2, imageHeight/2+newSize/2))
        image = pygame.transform.scale(image, (imageSize, imageSize))
        screen.blit(image, (w/2-imageSize/2, h/2-imageSize/2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

    pygame.quit()


def downloadImage(search):
    global folderString, queryString, fileName

    queryString = search
    folderString = "downloads"

    blockPrint()
    downloader.download(queryString, limit=1, output_dir=folderString)
    enablePrint()

    loc = os.path.dirname(os.path.realpath(__file__))
    fileName = os.listdir(loc + "/" + folderString + "/" + queryString)[0]

    shutil.copyfile(loc + "/" + folderString + "/" + queryString + "/" + fileName, loc + "/" + folderString + "/" + fileName)
    shutil.rmtree(loc + "/" + folderString + "/" + queryString)


def another_downloader(search):


    global folderString, queryString, fileName
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
    # title = title.split("?")[0]

    img = Image.open(BytesIO(img_object.content))
    img.save("./scraped_images/" + title)

    folderString = "./scraped_images"
    fileName = title



def main():
    global folderString, fileName
    search = "red bull racing"
    # downloadImage(search)
    try:
        another_downloader(search)
    except:
        folderString = "./resources"
        fileName = "Raphson.PNG"
    screen()


if __name__ == '__main__':
    main()
