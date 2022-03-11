# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 11:12:46 2021

@author: Felipe
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import credentials 

def check_login(driver_path = 'C:\\Users\\marco\\Documents\\GitHub\\mediar-tests-1\\WebDriver\\chromedriver.exe'):
    driver = webdriver.Chrome(driver_path)
    #driver.maximize_window()
    driver.implicitly_wait(5)
    
    logins = credentials.logins 
    
    for username in logins:
        print(username)
        driver.get("https://plataforma.mediarsolutions.com/login")
        assert "Login" in driver.title
        
        # user
        user = driver.find_elements_by_class_name('Input-sc-1nk5jxq-0')[0]
        user.clear()
        user.send_keys(username)
        
        # password
        password = driver.find_elements_by_class_name('Input-sc-1nk5jxq-0')[1]
        password.clear()
        password.send_keys(logins[username])
        password.send_keys(Keys.RETURN)
        
        # wait the ready state to be complete
        WebDriverWait(driver=driver, timeout=10).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
        )
        
        error_elem = driver.find_elements_by_class_name('Text-sc-13a1uj3-0')
        if len(error_elem) > 0:
            if 'Usuário ou senha não encontrados' in driver.page_source:
                print('LOGIN FAILED')
            else:
                print('login ok')
            
        print('------------')
    driver.close()
#
if __name__ == '__main__':
    check_login()
else :
    print('Not main')
