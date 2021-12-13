'''
Created on 13 Dec 2021

@author: li.yan
'''
from pageelements import BasePageElement
from elementlocators import LoginPageLocators
from selenium.webdriver.common.by import By  

class UsernameElement(BasePageElement):
    '''
    The class allows to set/get warrior name from login page
    '''    
    element_locator = (By.ID,'worrior_username')
        
    
class BasePage(object):
    """Base class to initialize the base page that will be called from all
    pages"""

    def __init__(self, driver):
        self.webdriver = driver

class LoginPage(BasePage):
    '''
    page for login / create warrior
    '''    
    username_element = UsernameElement()

    def is_title_matches(self):
        '''
        Verify the hard-coded title "COVID-19 THE GAME"               
        '''
        element = self.webdriver.find_element(*LoginPageLocators.lbl_title)
                        
        return (element.text.find(r'COVID-19 THE GAME')>=0)         


    def is_description_matches(self):
        '''
        Verify the hard-coded description matches               
        '''
        element = self.webdriver.find_element(*LoginPageLocators.lbl_desciption)
        description = r'The world has been taken over by super villain COVID19 and we need our super heroes to come to the rescue. We need to combat this great threat, so I am looking to recruit a team of Super Heroes and build the CURE team. I am in search of heroes like The HandWasher, Invisible Distance, SOAP, WFH, and any other great warriors against COVID19, until CURE arrives to the rescue.'
        
        return (element.text.find(description)>=0)  

    def is_summary_matches(self):
        '''
        Verify the hard-coded summary matches               
        '''
        element = self.webdriver.find_element(*LoginPageLocators.lbl_summary)
        summary = r'Tell me your warrior name'
        
        return (element.text.find(summary)>=0)

    def is_background_image_path_check(self):
        '''
        Verify the background image path               
        '''
        element = self.webdriver.find_element(*LoginPageLocators.image_background)
        path = r'/img/gamePrinciple.png'
        
        return (element.get_attribute('src').find(path)>=0)

    def is_href_check(self):
        '''
        Verify the hyperlink for "this project"               
        '''
        element = self.webdriver.find_element(*LoginPageLocators.href_this_project)
        href = r'https://github.com/users/ale-sanchez-g/projects/1'
        
        return (element.get_attribute('href').find(href)>=0)

    def click_create_button(self):
        '''
        Click Create warrior
        '''     
        element = self.webdriver.find_element(*LoginPageLocators.btn_create_warrior)        
        element.click() 
