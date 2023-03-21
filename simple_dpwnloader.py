import os
import time
import io
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image

# driver downloaded from https://chromedriver.chromium.org/downloads
DRIVER_PATH = "./chromedriver/chromedriver.exe"


def get_images_from_google(query, max_images, wd, delay=3):
    def scroll_down(wd):
        time.sleep(delay)
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    search_url = "https://www.google.com/search?q={q}&tbm=isch&ved=2ahUKEwjykJ779tbzAhXhgnIEHSVQBksQ2-cCegQIABAA&oq=cats&gs_lcp=CgNpbWcQAzIHCAAQsQMQQzIHCAAQsQMQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzoHCCMQ7wMQJ1C_31NYvOJTYPbjU2gCcAB4AIABa4gBzQSSAQMzLjOYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=7vZuYfLhOeGFytMPpaCZ2AQ&bih=817&biw=1707&rlz=1C1CHBF_enCA918CA918"
    wd.get(search_url.format(q=query))

    image_urls = []

    while len(image_urls) < max_images:
        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        print("Found: ", len(thumbnails))

        for img in thumbnails:
            if len(image_urls) < max_images:
                curr_src = img.get_attribute('src')
                if curr_src and 'http' in curr_src and curr_src not in image_urls:
                    image_urls.append(img.get_attribute('src'))

        if len(image_urls) < max_images:
            scroll_down(wd)

    return image_urls


def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print("Saved successfully")
    except Exception as e:
        print('FAILED -', e)


def download_asked_photos(question: str, num: int):
    wd = webdriver.Chrome(DRIVER_PATH)
    urls = get_images_from_google(question, num, wd)

    destination_folder = "./downloaded_photos/" + question.replace(' ', '_').lower() + "/"
    os.mkdir(destination_folder)

    for i, url in enumerate(urls):
        file_name = "img" + str(i) + ".jpg"
        download_image(destination_folder, url, file_name)

    wd.quit()
    print("Downloading completed")


download_asked_photos("leopard", 12)
