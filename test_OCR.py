import os
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime
import csv
import urllib
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageChops
import pytesseract
from scipy import ndimage
import re
from collections import Counter
os.environ["PATH"]="/Users/heather/Documents/Scraping/Gecko driver/"
def get_browser(binary=None):
    
    global browser  
    # only one instance of a browser opens, remove global for multiple instances
    if not browser: 
        browser = webdriver.Firefox(firefox_binary=binary)
    return browser
def trim(im):
   bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
   diff = ImageChops.difference(im, bg)
   diff = ImageChops.add(diff, diff, 2.0, -100)
   bbox = diff.getbbox()
   if bbox:
       return im.crop(bbox)
def change_contrast(img, level):
    factor = (259 * (level + 255)) / (255 * (259 - level))
    def contrast(c):
        return 128 + factor * (c - 128)
    return img.point(contrast)
def clean_captcha(filename):
    captcha = filename
    initial_im = Image.open(captcha).convert("P")
    cleaned_im = Image.new("P", initial_im.size, 255)

    for x in range(initial_im.size[1]):
        for y in range(initial_im.size[0]):
            pix = initial_im.getpixel((y, x))
            if pix > 220:
                cleaned_im.putpixel((y, x), 0)
    cleaned_im.save("cleaned.png")
def get_text():
    param_space=np.linspace(1,3.2,40)
#    param_space2=np.linspace(350,450,5)
    z=400
    poss_results=[]
    for i in param_space:
        final_im=change_contrast(
                Image.fromarray(ndimage.filters.gaussian_filter(
                Image.open("cleaned.png"), i, mode='nearest')),z)
        text = pytesseract.image_to_string(final_im)
        text=re.sub(r'[^\w]', '', str(text))
        if len(str(text))==4:
            poss_results.append(str(text))
    try:
        first=[x[0] for x in poss_results]
        second=[x[1] for x in poss_results]
        third=[x[2] for x in poss_results]
        fourth=[x[3] for x in poss_results]
        return(Counter(first).most_common(1)[0][0]+Counter(second).most_common(1)[0][0]+
      Counter(third).most_common(1)[0][0]+Counter(fourth).most_common(1)[0][0])
    except:
        return "fail"
    

binary = '/Applications/TorBrowser.app/Contents/MacOS/firefox'
#Copied from stackoverfolow- initiating Tor Browser
if os.path.exists(binary) is False:
    raise ValueError("The binary path to Tor firefox does not exist.")
firefox_binary = FirefoxBinary(binary)
browser = None
browser = get_browser(binary=firefox_binary)
url='http://fkqzda67aavjkhui.onion/?ai=1675'
browser.get(url)
counter=0
while True:   
    img=browser.find_element_by_class_name("captcha") 
    location = img.location
    print(location)
    size = img.size
    print(size)
    png = browser.get_screenshot_as_png()
    im = Image.open(BytesIO(png))
    im.save('screenshot2.png')
    location['x']=1152
    location['y']=1440-789
    left = location['x']
    top = location['y']
    right = location['x'] + size['width']+100
    bottom = location['y'] + size['height']+70
    im = im.crop((left, top, right, bottom)) # defines crop points
    counter+=1
    print(counter)
    im.save("screenshot.png")
    im.save('screenshot'+str(counter)+'.png')
    opencvImage = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR) 
    img=opencvImage    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(gray,127,255,1) 
    image, contours, hierarchy = cv2.findContours(thresh,1,2)
 
    for cnt in contours:
        if cv2.contourArea(cnt)>10000:
            print(cv2.contourArea(cnt))
            cv2.drawContours(img,[cnt],0,255,-1)
            (x,y,w,h) = cv2.boundingRect(cnt)
            print((x,y,w,h))
            crop_img = gray[y:y+h, x:x+w]
            cv2.imwrite("cropped.png", crop_img)
            break
    cv2.imwrite("countours.png",img)
    ima = Image.open("cropped.png") # the second one 
    ima = ima.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(ima)
    ima = enhancer.enhance(2)
    ima = ima.convert('1')
    ima.save('temp2.jpg')
    tirmmed=trim(ima)
    tirmmed.save("trimmed.jpg")
    tirmmed.save("trimmed"+str(counter)+".jpg")
    clean_captcha("trimmed.jpg")
    text=get_text()
    print(text)
    browser.refresh()
    time.sleep(2)
