'''
Created on 13 Dec 2021

@author: li.yan
'''

import unittest
from selenium import webdriver
import pageobjects
import time

class LoginPageTests(unittest.TestCase):
    '''
    All test cases for login feature 
    '''

    def setUp(self):
        self.browserdriver = webdriver.Chrome()
        print('open page in http://127.0.0.1:8080/')
        self.browserdriver.get("http://127.0.0.1:8080/")

    def test_static_elements(self):
        '''
        Verify static elements on login screen
        '''
        print ('/---------------------------------/')
        print ('Test Case: Login Page - test_static_elements')
        
        login_page = pageobjects.LoginPage(self.browserdriver)
        
        #Checks if title is correct
        assert login_page.is_title_matches(), 'title does not match.'
        
        #Checks if description is correct
        assert login_page.is_description_matches(), 'description does not match.'
        
        #Checks if summary is correct
        assert login_page.is_summary_matches(), 'summary does not match.'        

        #Checks if summary is correct
        assert login_page.is_background_image_path_check(), 'background image path does not match.'        
        
        #Checks if external link is correct
        assert login_page.is_href_check(), 'hyperlink does not match.'
        
    
    def test_create_success(self):
        '''
        Test with valid user, user should be able to login successfully
        '''
        print ('/---------------------------------/')
        print ('Test Case: Login Page - test_create_success')                
        login_page = pageobjects.LoginPage(self.browserdriver)
        
        #Set warrior name
        __random_number = int(time.time())                                                            
        
        login_page.username_element  = r'LY'+ str(__random_number)
        login_page.click_create_button()
                
        # Due to the issue of the page, outcome of this operation cannot be verified

    def test_create_success_long_name_50(self):
        '''
        Expected to successfully create warrior with long name        
        '''   
        print ('/---------------------------------/')
        print ('Test Case: Login Page - test_register_success_long_name_50')           
        login_page = pageobjects.LoginPage(self.browserdriver)
        
        #Set warrior name
        login_page.username_element  = r'LY'+str(int(time.time())).zfill(48)
        login_page.click_create_button()
                
        # Due to the issue of the page, outcome of this operation cannot be verified  

    def test_create_fail_duplicate_name(self):
        '''
        Test with valid user, user should be able to login successfully
        '''        
        print ('/---------------------------------/')
        print ('Test Case: Login Page - test_create_fail_duplicate_name')   
                
        login_page = pageobjects.LoginPage(self.browserdriver)
        
        #Set warrior name
        login_page.username_element  = "ly20211212"
        login_page.click_create_button()
                
        # Due to the issue of the page, outcome of this operation cannot be verified      

    def test_create_fail_xtralong_name_51(self):
        '''
        Expected not to allow create warrior with name longer than field defined        
        '''   
        print ('/---------------------------------/')
        print ('Test Case: Login Page - test_create_fail_xtralong_name_51')           
        login_page = pageobjects.LoginPage(self.browserdriver)
        
        #Set warrior name
        login_page.username_element  = r'LY'+str(int(time.time())).zfill(49)
        login_page.click_create_button()
                
        # Due to the issue of the page, outcome of this operation cannot be verified   

    def test_create_fail_empty_name(self):
        '''
        Expected not to allow create warrior with empty name        
        '''   
        print ('/---------------------------------/')
        print ('Test Case: Login Page - test_create_fail_empty_name')           
        login_page = pageobjects.LoginPage(self.browserdriver)
        
        #Set warrior name
        login_page.username_element  = r''
        login_page.click_create_button()
                
        # Due to the issue of the page, outcome of this operation cannot be verified 
     
    def tearDown(self):
        self.browserdriver.close()

if __name__ == "__main__":
    unittest.main()