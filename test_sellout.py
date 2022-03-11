# -*- coding: utf-8 -*-
"""
Modify on tuesday Feb 22 12:12:46 2022

@author: Felipe/ Marco / Luiz
"""
from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime as dt
import credentials
from login import login
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import sys

#print log
sys.stdout = open("C:\\sellout_login\\output.log", "a")


def map_sellout(df):
    #query that fetches the value in bigquery
    df['industry'] = df['industry'].map(credentials.industry_dict)
    df = df.groupby('industry')['total_value'].sum()
    return df
    #query that replaces month and year automatically
def check_sellout():
    query = f"""SELECT industry, total_value FROM `mediar-painel.selenium.test_sellout` 
                WHERE year = {dt.now().year}
                AND month = {dt.now().month-1}"""
    sellout_bq = pd.read_gbq(query, project_id='mediar-painel')
    sellout_bq = map_sellout(sellout_bq)

    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #driver.maximize_window()
    driver.implicitly_wait(10)
    
    logins = credentials.logins
    
    
    for username, password in logins.items():
        url = 'https://plataforma.mediarsolutions.com/login'        
        logged = login(driver, url, username, password)
        #Verify if the user is logged in with success or not
        error_elem = driver.find_elements(by=By.CLASS_NAME, value='Text-sc-13a1uj3-0 eiEtIk')
        if len(error_elem) >= 0: 
            if ("""Usuário ou senha não encontrados, verifique as informações inseridas e, caso persista, 
                utilize nossa recuperação de senha.""") in driver.page_source:
                print('LOGIN FAILED')
            else:
                logged = True
        #acess the sellout page
        if logged:
            indicador = driver.find_elements(by=By.XPATH, value='/html/body/div/div/div[2]/div[1]/div[3]')[0]
            indicador.click()

            
            delay = 20 # seconds
            try:
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'sellout_value'))) # wait until the element is loaded
                print ("Page is ready!")
            except TimeoutException:
                print ("Loading took too much time!")
             #Use active filters in the sellout page
            filters = driver.find_elements(by=By.XPATH, value='/html/body/div/div/div[4]/div[1]/div[3]')
            stores_filter = filters[0] 
            stores_filter.click()
            sleep(5)

            #Button for select all stores
            selections = driver.find_element(by=By.ID, value='select_all')
            selections_button = selections
            selections_button.click()
            sleep(5)

            #Button to close MS BASELINE
            buttons_x = driver.find_element(by=By.XPATH, value = '/html/body/div/div/div[1]/div/div[3]/div/div[3]/div/div/div/div[2]/div[1]')
            button_x = buttons_x 
            button_x.click()
            sleep(5)

            #button SAVE
            save_buttons = driver.find_element(by=By.ID, value='save_params')
            save_button = save_buttons
            save_button.click()
            sleep(5)

            #SELLOUT OUT
            sleep(10)    
            selloutElem = driver.find_element(by=By.ID, value='sellout_value')
            sellout_plataforma = round(float(selloutElem.text[3:].replace(',', '')), 2)
            sellout_bigquery = round(sellout_bq.loc[username], 2)
            print('Sellout Plataforma:', sellout_plataforma)
            print('Sellout BigQuery:', sellout_bigquery)
            if sellout_plataforma == sellout_bigquery:
                print('sellout ok')
            else:
                print('sellout incorreto')

            if sellout_plataforma > sellout_bigquery: # if sellout plataform is bigger than bigquery
                print('sellout da plataforma maior')
            else:
                print('sellout da plataforma menor')
        else:
            print('login not completed')
                
    print('------------')
    driver.close()

if __name__ == '__main__':
   check_sellout()
   print('DONE')
elif __name__ == '__check_sellout__':
   check_sellout()
else: 
    print('ERROR')
sys.stdout.close() #close print log
    


    
    