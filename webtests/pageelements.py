'''
Created on 13 Dec 2021

@author: li.yan
'''
from selenium.webdriver.support.ui import WebDriverWait


class BasePageElement(object):
    '''
    Parent class for all input elements on page
    '''

    def __set__(self, obj, value):
        '''
        Sets the text to the value supplied
        '''
        driver = obj.driver        
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(*self.element_locator))
        driver.find_element(*self.element_locator).clear()
        driver.find_element(*self.element_locator).send_keys(value)
        
    def __get__(self, obj, owner):
        """Gets the text of the specified object"""

        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(*self.element_locator))
        element = driver.find_element(*self.element_locator)
        return element.get_attribute("value")