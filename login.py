from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def login(driver, url, username, password):

    print(username)
    driver.get(url)
    assert "Login" in driver.title
        
        # Set username
    user_input = driver.find_element(by=By.ID, value='user_input')
    user_input.clear()
    user_input.send_keys(username)
    
    # Set password
    passwd_input = driver.find_element(by=By.ID, value='pswrd_input')
    passwd_input.clear()
    passwd_input.send_keys(password)
    
    # Try to login
    passwd_input.send_keys(Keys.RETURN)
    # wait the ready state to be complete
    WebDriverWait(driver=driver, timeout=10).until(
        lambda x: x.execute_script("return document.readyState === 'complete'")
    )
    
    logged = False
        #Verify if the user is logged in with success or not
    error_elem = driver.find_elements(by=By.CLASS_NAME, value='Text-sc-13a1uj3-0 eiEtIk')
    if len(error_elem) >= 0: # TODO: caso erro_elem for > 0 não for conhecido, print algo
        if ("""Usuário ou senha não encontrados, verifique as informações inseridas e, caso persista, 
        utilize nossa recuperação de senha.""") in driver.page_source:
            print('LOGIN FAILED')
        else:
            logged = True
            print('login ok')
    return logged
        
    