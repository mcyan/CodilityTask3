'''
Created on 13 Dec 2021

@author: li.yan
'''

from selenium.webdriver.common.by import By

class LoginPageLocators(object):
    '''
    Class for login page locators
    '''
    btn_create_warrior = (By.ID, r'warrior')    
    lbl_title = (By.XPATH, r'/html/body/div[1]/h1/p')
    lbl_desciption = (By.XPATH, r'/html/body/row[1]/div/div/p')
    lbl_summary = (By.XPATH, r'/html/body/row[3]/div/div/h2')
    href_this_project = (By.XPATH, r'/html/body/row[4]/div/div/p/a')
    image_background = (By.XPATH, r'/html/body/row[2]/div/div/div/div/div/img')
    
    
    