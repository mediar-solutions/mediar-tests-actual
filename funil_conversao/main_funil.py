from cgitb import text
from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime as dt
import credentials
from login import login

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import sys

    #print log
#sys.stdout = open("C:\\funil_login\\output.log", "a")


def check_funil():
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #driver.maximize_window()
    driver.implicitly_wait(10)
    
    logins = credentials.logins
    #Logging plataform
    url = 'https://plataforma.mediarsolutions.com/'
    for username, password in logins.items():
        logged = login(driver, url, username, password) 
        #acess the funil page
        if logged:
            indicador = driver.find_elements(by=By.XPATH, value='/html/body/div/div/div[4]/div[2]/div[1]/div/div[1]')[0]
            indicador.click()
            delay = 10 # seconds
            try:
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'funil_conversão'))) # wait until the element is loaded
                print ("Page is ready!")
            except TimeoutException:
                print ("Loading took too much time!")
            sleep(5)
            #Button for select all stores
            while True:
                try:
                    selections = driver.find_element(by=By.ID, value='select_all')
                    selections_button = selections
                    selections_button.click()           
                    sleep(5)
                    if selections_button.is_displayed():
                        break
                except Exception as e:
                    print('------deu ruim mas deu bom--------')
                    print(e)
                    break

            #Select all subcategories
            limit = 9999
            options = []
            for i in range(0, limit):
                #Use active filters in the funil page
                filters = driver.find_elements(by=By.XPATH, value='/html/body/div/div/div[4]/div[1]/div[3]/div[2]')
                stores_filter = filters[0] 
                stores_filter.click()
                sleep(3)
                #subcategory selection
                subcategory_select = driver.find_element(by=By.XPATH, value='/html/body/div/div/div[1]/div/div[3]/div/div[3]/div/div/div/div[2]')
                subcategory_select.click()
                sleep(2.8)
                if i == 0:
                    options = driver.find_elements(by=By.XPATH, value='/html/body/div/div/div[1]/div/div[3]/div/div[3]/div/div/div/div[1]/*')
                    limit = len(options)
                options[i].click()
                sleep(2.5)
                #button SAVE 
                save_buttons = driver.find_element(by=By.ID, value='save_params')
                save_button = save_buttons
                save_button.click()
                #loading_icon = driver.find_element(by=By.XPATH, value = '/html/body/div/div/div[4]/div[3]/div/svg')
                #while loading_icon.is_displayed():
                sleep(5)
                    
                        



                
                
            
            

            #Store flow variation
                store_variation = driver.find_element(by=By.ID, value='variation_0')
                store_variation = store_variation.text
                print(store_variation)
                sleep(5)    
                print('------------')
                
                    #Category Flow Variation
                category_variation = driver.find_element(by=By.ID, value='variation_1')
                category_variation = category_variation.text
                print(category_variation)
                sleep(5)    
                print('------------')

                    #Stopping Power Variation
                stoppingp_variation = driver.find_element(by=By.ID, value='variation_2')
                stoppingp_variation = stoppingp_variation.text
                print(stoppingp_variation)
                sleep(5)
                print('------------')

                    #Conversion Variation
                conversion_variation = driver.find_element(by=By.ID, value='variation_3')
                conversion_variation = conversion_variation.text
                print(conversion_variation)
                sleep(5)
                print('------------')

if __name__ == '__main__':
   check_funil()
   print('DONE')
elif __name__ == '__check_funil__':
   check_funil()
else: 
    print('ERROR')
sys.stdout.close() #close print log
    


    
    
