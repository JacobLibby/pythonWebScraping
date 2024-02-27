from bs4 import BeautifulSoup
import time 
from selenium import webdriver
from selenium.webdriver import Chrome 
from selenium.webdriver.common.by import By 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os 
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import csv

def grab_html():
    # Define the Chrome webdriver options
    options = webdriver.ChromeOptions() 
    options.add_argument("--headless") # Set the Chrome webdriver to run in headless mode for scalability
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--allow-insecure-localhost")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    options.add_argument('ignore-certificate-errors')
    options.add_argument('ignore-ssl-errors')
    options.add_argument('ignore-certificate-errors-spki-list')
    options.add_argument('--allow-insecure-localhost')
    options.add_argument('log-level=3') # Silences all but fatal errors - added to silence ssl and handshake errors
    options.page_load_strategy = "none" # By default, Selenium waits for all resources to download before taking actions. However, we don't need it as the page is populated with dynamically generated JavaScript code.
    driver = webdriver.Chrome(options=options) # Pass the defined options objects to initialize the web driver
    # Set an implicit wait of 5 seconds to allow time for elements to appear before throwing an exception
    driver.implicitly_wait(10)
    
    
    return driver 

def main():
  
    ## WEB SCRAPING ##
    url = "https://en.wikipedia.org/wiki/Polar_bear"

    outputName = url.split('//')[1].split('/')[0].replace('.','_')
    
    output_full = outputName + "_full.txt"
    counter_filename = 0
    output_full_original = output_full
    if os.path.exists(output_full):
        while True:
            counter_filename += 1
            if os.path.exists(output_full_original.split('.')[0] + "(" + str(counter_filename) + ")." + output_full_original.split('.')[1]):
                continue
            else:
                output_full = output_full_original.split('.')[0] + "(" + str(counter_filename) + ")." + output_full_original.split('.')[1]
                break
    
    
    driver = grab_html()
    driver.get(url)
    time.sleep(8)
   
    selenium_fullpage = driver.page_source
    selenium_fullpage = str(selenium_fullpage).replace('\x80', "").replace('\x93',"").replace('\x8d',"").replace('\x9f',"").replace('\u200d',"").replace('\U0001f9e1',"")
    driver.close()

    with open(output_full, 'w', newline='', encoding="utf-8") as output_file:
        output_file.write(str(selenium_fullpage))

    
    soup = BeautifulSoup(selenium_fullpage, features="html.parser")

    # PARSING ELEMENTS WITH BEAUTIFUL SOUP #

    # table = soup.find('div', class_ = 'db_table')
    # header_array = table.find_all('div', class_ = 'db_sort-button')
    # # df = pd.DataFrame(columns = headers)
    # inner_table = soup.find('div', class_ = 'w-dyn-items')
    

    
   
    

if __name__ == '__main__':
    main()