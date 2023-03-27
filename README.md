# Photos downloader
### Simple app to download photos from Google
It allows user to input classes, for which pictures should be found, number of photos and size of valid and test set. 
App open chrome browser, found images for specific queries and save images to "downloaded_photos" directory.
Images are separated to "train", "test" and "valid" sets. Every set contain a folder named by class with downloaded images for it's query.
They can be easily used in tensorflow or other similar tool.

![interface](https://github.com/mklimek001/photos-downloader/blob/main/app_window.jpg)

It doesn't download photos in full resolution, only thumbnails, but it is enough for study purposes.  
App allows to automatic download over 200 photos for each query.

### Technologies
* GUI - Tkinter
* web seraching - Selenium
* photos dowloading - Pillow
  
In order to run this app, you have to download chrome driver speciffic for your browser from this site: https://chromedriver.chromium.org/downloads and put it in folder 
"chromediver" in project directory.   
Version of chrome browser could be found here: chrome://settings/help.
