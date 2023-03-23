import math
import os
import time
import io
import requests
import random
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image

# driver downloaded from https://chromedriver.chromium.org/downloads
DRIVER_PATH = "./chromedriver/chromedriver.exe"


def scroll_down(wd, delay=2):
    wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(delay)


def get_images_from_google(query, max_images, wd, delay=2):
    search_url = "https://www.google.com/search?q={q}&tbm=isch&ved=2ahUKEwjykJ779tbzAhXhgnIEHSVQBksQ2-cCegQIABAA&oq=cats&gs_lcp=CgNpbWcQAzIHCAAQsQMQQzIHCAAQsQMQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzoHCCMQ7wMQJ1C_31NYvOJTYPbjU2gCcAB4AIABa4gBzQSSAQMzLjOYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=7vZuYfLhOeGFytMPpaCZ2AQ&bih=817&biw=1707&rlz=1C1CHBF_enCA918CA918"
    wd.get(search_url.format(q=query))
    image_urls = []

    while len(image_urls) < max_images:
        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        for img in thumbnails:
            if len(image_urls) < max_images:
                curr_src = img.get_attribute('src')
                if curr_src and 'http' in curr_src and curr_src not in image_urls:
                    image_urls.append(img.get_attribute('src'))
            else:
                break

        if len(image_urls) < max_images:
            scroll_down(wd)

    return image_urls


def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = os.path.join(download_path, file_name)

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

    except Exception as e:
        print('DOWNLOADING FAILED -', e)


def download_images_to_folder(urls, destination_folder, offset: int = 0):
    for i, url in enumerate(urls):
        str_num = str(i + offset)
        zeros_filling = (6 - len(str_num)) * '0'
        file_name = "img" + zeros_filling + str_num + ".jpg"
        download_image(destination_folder, url, file_name)


def get_category_images(urls, category: str, num: int, test_size: float = 0.2, valid_size: float = 0.1):
    random.shuffle(urls)

    test_num = math.floor(test_size * num)
    test_urls = urls[:test_num]

    valid_num = math.floor(valid_size * num) + test_num
    valid_urls = urls[test_num:valid_num]

    train_urls = urls[valid_num:]

    main_folder = '.\\downloaded_photos'
    if not os.path.exists(main_folder):
        os.mkdir(main_folder)

    train_folder = os.path.join(main_folder, "train")
    test_folder = os.path.join(main_folder, "test")
    valid_folder = os.path.join(main_folder, "valid")
    folders = [train_folder, test_folder, valid_folder]

    train_folder_category = os.path.join(train_folder, category.lower().replace(' ', '_'))
    test_folder_category = os.path.join(test_folder, category.lower().replace(' ', '_'))
    valid_folder_category = os.path.join(valid_folder, category.lower().replace(' ', '_'))

    folders_category = [train_folder_category, test_folder_category, valid_folder_category]

    for folder in folders:
        if not os.path.exists(folder):
            os.mkdir(folder)

    for folder in folders_category:
        if not os.path.exists(folder):
            os.mkdir(folder)

    download_images_to_folder(test_urls, test_folder_category)
    download_images_to_folder(valid_urls, valid_folder_category, test_num)
    download_images_to_folder(train_urls, train_folder_category, valid_num)


def get_images(categories: list, num: int, test_size: float = 0.2, valid_size: float = 0.1):
    wd = webdriver.Chrome(DRIVER_PATH)
    wd.get("https://www.google.com/search?q=google&tbm=isch&ved=2ahUKEwiMydWsq-_9AhUJwCoKHfdkBBEQ2-cCegQIABAA&oq=google&gs_lcp=CgNpbWcQAzIECCMQJzIHCAAQsQMQQzIECAAQQzIICAAQgAQQsQMyBQgAEIAEMgUIABCABDIECAAQQzIECAAQQzIECAAQQzIHCAAQsQMQQzoICAAQsQMQgwE6BwgjEOoCECc6CwgAEIAEELEDEIMBOgcIABCABBAYOgQIABAeOgoIABCxAxCDARBDUKIIWKhTYNJXaBBwAHgAgAGBAYgByxCSAQQxNi42mAEAoAEBqgELZ3dzLXdpei1pbWewAQrAAQE&sclient=img&ei=yNkaZIzFBYmAqwH3yZGIAQ&bih=1329&biw=1282")
    reject = wd.find_element(By.CLASS_NAME, "Nc7WLe")
    reject.click()

    downloading_threads = []

    for category in categories:
        urls = get_images_from_google(category, num, wd)

        downloading_thread = threading.Thread(target=get_category_images,
                                              args=(urls, category, num, test_size, valid_size))
        downloading_threads.append(downloading_thread)
        downloading_thread.start()

    wd.quit()

    for thread in downloading_threads:
        thread.join()

    print("DOWNLOADING COMPLETED")

# get_images(["cat", "dog", "hamster", "gold fish"], 100)
