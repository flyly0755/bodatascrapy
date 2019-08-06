# coding=utf-8
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
import time
import urllib
from urllib.request import urlretrieve
from selenium.webdriver.common.keys import Keys
import xlwt
import xlrd
from xlutils.copy import copy
from datetime import datetime
import re
#from .pyudfunctions import entudfunctions
from entudfunctions import moreindex,dayscrapy


excelcolunm =20



def main():
    print('***********************Open Page********************************')
    driver = webdriver.Firefox()
    url = 'http://ebotapp.entgroup.cn/DataBox/Film/Movie/Index'
    driver.get(url)
    time.sleep(10)
    moreindex(driver)
    #dateymd = driver.find_element_by_xpath('//*[@id="selDate_Btn"]/label/span').text
    driver.find_element_by_xpath('//*[@id="selDate_PerBtn"]').click()
    time.sleep(10)
    dayscrapy(driver,excelcolunm)

    #driver.close()

if __name__ == '__main__':
    main()

