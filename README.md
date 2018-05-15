# DarkWebDreamMarketScrapper
Helping my friend to scrape information on drugs sold on DarkWeb by integrating selenium, Tor, openCV, tesseract and Python to crawl darkweb and overcome CAPTCHA check which activates every 100th click.  
  
test_OCR.py - basically keeps refreshing main page and prints the captcha text as recognized by OCR. It usually guesses correctly 1 in 8 attempts. When it fails to produce anything meaningful, "fail" is returned    
  
  
main.py - runs the main loop. After browser is open, the user is given a minute to navigate to the listing she wants to scrap. Then the program automatically clicks on all the drug items, goes to individual pages and gets relevant information from them. After all items on the page are scraped the program automatically navigates to the next page, until all the listing is scraped.  
   
   
captcha_hack.py - contains some of the OCR-related functions used in main.py
