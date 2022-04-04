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
from selenium.webdriver.common.action_chains import ActionChains
import sys

    #print log
#sys.stdout = open("C:\\funil_login\\output.log", "a")


def check_eventos():
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #driver.maximize_window()
    driver.implicitly_wait(10)
    
    logins = credentials.logins
    #Logging plataform
    url = 'https://previa.plataforma.mediarsolutions.com/home/overview/events'
    for username, password in logins.items():
        logged = login(driver, url, username, password) 
        #acess the analysis of events
        if logged:
            driver.refresh()
            indicador = driver.find_elements(by=By.XPATH, value='/html/body/div/div/div[4]/div[1]/div[2]/div[2]/p')[0]
            indicador.click()
            delay = 15 # seconds
            try:
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'analise_evento'))) # wait until the element is loaded
                print ("Page is ready!")
            except TimeoutException:
                print ("Loading took too much time!")

             #Use active filters in the analise page
            filters = driver.find_elements(by=By.XPATH, value='/html/body/div/div/div[4]/div[1]/div[3]/div[2]')
            stores_filter = filters[0] 
            stores_filter.click()
            sleep(5)

            #Button for select the stores 
            selections = driver.find_elements(by=By.XPATH, value='/html/body/div/div/div[1]/div/div[2]/div[2]/div/li[*]/input')
            for store in selections:
                store.click()
                sleep(0.5)
            
                
            #Select all subcategories
            #count = 0 #todo codigo nao termina o loop
            subcategory_select = driver.find_element(by=By.XPATH, value='/html/body/div/div/div[1]/div/div[3]/div/div[3]/div/div/div/div[2]')
            subcategory_input = driver.find_element(by=By.XPATH, value='/html/body/div/div/div[1]/div/div[3]/div/div[3]/div/div/div/div[1]/div[2]/div/input')
            # while True:
            #     try:
            #         subcategory_select.click()
            #         subcategory_input.send_keys(Keys.ENTER)
            #         count_selected_options = len(driver.find_elements(by=By.XPATH, value='/html/body/div/div/div[1]/div/div[3]/div/div[3]/div/div/div/div[1]/*'))
            #         count += 1
            #         if count >= count_selected_options:
            #             break
            #     except Exception as e:
            #         print(e)
            #         break
            subcategory_select.click()
            subcategory_input.send_keys(Keys.ENTER)
            sleep(3)
               

            #datepciker start #todo impossivel de selecionar data
            baseline_start = driver.find_element(by=By.ID, value = 'baseline_start')
            baseline_start.click()
            print('clicou')
            sleep(2)
            data_days = driver.find_elements(by=By.XPATH, value='/html/body/div/div/div[1]/div/div[1]/div/div/div[2]/div[3]/div[2]/div/div/div/div[2]/div[2]/button[*]')
            data_days = [x for x in data_days if 'rdrDayPassive' not in x.get_attribute('class') and 'rdrDayDisabled' not in x.get_attribute('class')] #filter elements that are not active in calendar
            data_days[0].click()
            data_days[-1].click()

            #datepicker click outside
            date_click = driver.find_element(by=By.ID, value='datepicker_close')
            date_click.click()
            sleep(2)

            #events information #todo create a fild to input some text
            events = driver.find_elements(by=By.XPATH, value='/html/body/div/div/div[1]/div/div[5]/div[2]/div[1]/input')
            for event in events:
                event.click()
                sleep(0.5)
            
            

            #button SAVE
            save_buttons = driver.find_element(by=By.XPATH, value='/html/body/div/div/div[1]/div/div[6]/button')
            save_button = save_buttons
            save_button.click()
            sleep(5)

if __name__ == '__main__':
   check_eventos()
   print('DONE')
elif __name__ == '__check_analise__':
   check_eventos()
else: 
    print('ERROR')
sys.stdout.close() #close print log
    


    
    
