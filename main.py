# All the relevant libraries are attached below here
import os
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime
import csv
from captcha_hack import if_dos, dos_actions, too_many_windows

# Seeting the geckodriver path
os.environ["PATH"] = "/Users/heather/Documents/Scraping/Gecko driver/"

# path to the firefox binary inside the Tor package
# binary = '/Applications/TorBrowser.app/Contents/MacOS/firefox'
binary = "/Applications/TorBrowser.app/Contents/MacOS/firefox"
# Copied from stackoverfolow- initiating Tor Browser
if os.path.exists(binary) is False:
    raise ValueError("The binary path to Tor firefox does not exist.")
firefox_binary = FirefoxBinary(binary)
browser = None

# Copied from stackoverflow, initiates the tor browser
def get_browser(binary=None):

    global browser
    # only one instance of a browser opens, remove global for multiple instances
    if not browser:
        browser = webdriver.Firefox(firefox_binary=binary)
    return browser


# Support functions which are used to get the information from the page
def get_title(browser):
    # Try except makes sure scapper does not die when it encounters a bug
    try:
        # Finds the element with class title and get the textual information from it
        title = browser.find_element_by_class_name("title")
        return title.text
    except:
        return "NA"


def get_basic_info(browser):
    inidividual_item = []
    # find element with clas tabularDetails.
    # THen looks for all children divs and gets textual information
    tabularDetails = browser.find_element_by_class_name("tabularDetails")
    # Be careful DISTINGUISHING find_ELEMENTS and find_ELEMENT
    for element in tabularDetails.find_elements_by_tag_name("div"):
        individual_item.append(element.text)
    return inidividual_item


def get_product_description(browser):
    try:
        # Find element with id offerDescription and gets the text
        product_description = browser.find_element_by_id("offerDescription")
        return product_description.text
    except:
        return "NA"


def get_terms_and_conditions(browser):
    try:
        # Counld not find a good
        terms_and_conditions = browser.find_element_by_css_selector(
            ".viewProduct > div:nth-child(8) > div:nth-child(2) > pre:nth-child(1)"
        )
        return terms_and_conditions.text
    except:
        return "NA"


def get_shipping_options_and_currencies(browser, individual_item):
    try:
        new_thing = individual_item
        shipping_options = browser.find_elements_by_class_name("shippingTable")
        counter = 0
        for z in shipping_options:
            result2 = []
            for i in z.find_elements_by_tag_name("tr"):
                result2.append(i.text)
            new_thing.append(result2)
            counter += 1
        if counter == 1:
            new_thing.append("NA")

        return new_thing
    except:
        return individual_item + ["NA", "NA"]


def get_product_ratings(browser):
    result = []
    try:
        ratings = browser.find_element_by_class_name("ratings")
    except:
        return "NA"
    try:
        for tr in ratings.find_elements_by_tag_name("tr"):
            interm = []
            interm.append(tr.find_element_by_class_name("age").text)
            stars = tr.find_element_by_class_name("rating")
            counter = 0
            for star in stars.find_elements_by_class_name("star"):
                counter += 1
            interm.append(str(counter) + " stars")
            interm.append(tr.find_element_by_class_name("ratingText").text)
            result.append(interm)
        return result
    except:
        return "NA"


browser = get_browser(binary=firefox_binary)
# url='https://check.torproject.org/'
url = "http://fkqzda67aavjkhui.onion/?ai=1675"
browser.get(url)
# Example with prices
# time.sleep(60)
# for timer in range(15):
#    prices=browser.find_elements_by_class_name('oPrice')
#    for i in prices:
#        print(i.text)
#    time.sleep(5)
#    elem=browser.find_element_by_class_name('lastPager')
#    elem.click()
#    time.sleep(5)
titles = []
counter = 0
counter2 = 0
time.sleep(60)
while True:
    # finds al the images on the main_page
    while True:
        try:
            images = browser.find_elements_by_class_name("oImage")
            break
        except:
            browser.refresh()
            time.sleep(5)
            continue
    # need to return to main_page after the page is closing
    main_window = browser.current_window_handle
    for image in images:

        # Emulates keybord, presses shift to open a new window
        while True:
            try:
                counter += 1
                print(counter)
                image.click()
                time.sleep(2)
                # Referes to "VIEW OFFER button"
                view_offer = browser.find_element_by_id("openProduct")
                ActionChains(browser).key_down(Keys.SHIFT).click(view_offer).key_up(
                    Keys.SHIFT
                ).perform()
                time.sleep(3)
                # Shift to the new window with specific product info
                windows = browser.window_handles
                browser.switch_to.window(windows[1])
                time.sleep(0.5)
                # Get all the information into list called INDIVIDUAL_ITEM
                individual_item = []
                individual_item.append(get_title(browser))
                individual_item = individual_item + get_basic_info(browser)
                individual_item.append(get_product_description(browser))
                individual_item.append(get_terms_and_conditions(browser))
                individual_item = get_shipping_options_and_currencies(
                    browser, individual_item
                )
                individual_item.append(get_product_ratings(browser))
                individual_item.append(str(datetime.datetime.now()))
                break
            except:
                time.sleep(5)
                if if_dos(browser):
                    dos_actions(browser)
                    browser.switch_to_window(main_window)
                    time.sleep(0.5)
                    continue
                else:
                    browser.switch_to_window(main_window)
                    time.sleep(0.5)
                    continue
        # APPEND INDIVIDUAL_ITEM to the csv file
        with open("output.csv", "a", encoding="utf-8") as fp:
            wr = csv.writer(fp, dialect="excel")
            wr.writerow(individual_item)
        # Closing the specific information windown and switching back to the main window
        browser.close()
        time.sleep(0.5)
        browser.switch_to_window(main_window)
    time.sleep(3)
    current_url = browser.current_url
    too_many_windows(browser, main_window)
    try:
        # when there is end of the page switch to the new page
        elem = browser.find_element_by_class_name("lastPager")
        elem.click()
        time.sleep(5)
        counter2 += 1
        print(counter2)
    except:
        time.sleep(5)
        if if_dos(browser):
            dos_actions(browser)
            browser.get(current_url)
            elem = browser.find_element_by_class_name("lastPager")
            elem.click()
            time.sleep(5)
            counter2 += 1
            print(counter2)
        # if no new pages finish
        else:
            print("Scraping ended succesfully!")
            break
