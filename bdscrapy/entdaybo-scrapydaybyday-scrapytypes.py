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
from entudfunctions import moreindex,dayscrapy,isElementExist


excelcolunm =21



def main(dated=None):
    choicemode = input("请选择采集方式(1.前一天采集 2.特定某一天采集 3.某个连续时段采集 4.非连续时段多天采集):")
    if choicemode == "2":
        dateymds = input("请输入需采集的日期，格式xxxx-xx-xx：")
    elif choicemode=="3":
        dateymdcs = input("请输入需采集的起始日期，格式xxxx-xx-xx：")
        dateymdce = input("请输入需采集的结束日期，格式xxxx-xx-xx：")

    print('***********************Open Page********************************')
    driver = webdriver.Chrome()
    url = 'http://ebotapp.entgroup.cn/DataBox/Film/Movie/Index'
    driver.get(url)
    time.sleep(10)
    driver.maximize_window() #页面窗口最大化
    moreindex(driver)

    if choicemode=="1":
        #dateymd = driver.find_element_by_xpath('//*[@id="selDate_Btn"]/label/span').text
        driver.find_element_by_xpath('//*[@id="selDate_PerBtn"]').click()
        time.sleep(10)
        print("---------------------------start scrapy data-----------------------------")
        dayscrapy(driver,excelcolunm)
    elif choicemode=="2":

        datey =re.findall(r'\d{4}',dateymds)
        datem = re.findall(r'(?<=-)(.+?)(?=-)',dateymds)
        dated = re.findall(r'(?<=-)\d{2}$',dateymds)
        driver.find_element_by_xpath('//*[@id="selDate_Btn"]').click()
        time.sleep(2)
        datechn=datey[0]+"年"+str(int(datem[0]))+"月"
        print("datechn is %s" %datechn)
        xpathd = driver.find_element_by_xpath('//*[@id="selDate_ListDay"]/div/div/p[contains(text(),"'+str(datechn)+'")]')
        ##print("xpath is %s" %xpathd)
        ifdisplay=xpathd.is_displayed()
        print("ifdisplay is %s"%ifdisplay)

        driver.find_element_by_xpath('//*[@id="selDate_ListDay"]/div/div//table/tbody/tr/td[@data-tag="' + str(dateymds) + '"]').click()

        while not ifdisplay:
            target = driver.find_element_by_xpath('//*[@id="selDate_ListDay"]/div/div/p[contains(text(),"'+str(datechn)+'")]')
            driver.execute_script("arguments[0].scrollIntoView(false);", target)
            time.sleep(2)
            ifdisplay = xpathd.is_displayed()
            print("ifdisplay is:%s"%ifdisplay)
        driver.find_element_by_xpath('//*[@id="selDate_ListDay"]/div/div//table/tbody/tr/td[@data-tag="'+str(dateymds)+'"]')
        time.sleep(10)
        print("---------------------------start scrapy data-----------------------------")
        dayscrapy(driver,excelcolunm)
    elif choicemode=="3":
        # dateymdcs = input("请输入需采集的起始日期，格式xxxx-xx-xx：")
        # dateymdce = input("请输入需采集的结束日期，格式xxxx-xx-xx：")
        dateymdcp = driver.find_element_by_xpath('//*[@id="selDate_Btn"]/label/span').text
        while dateymdcp !=dateymdce:
            driver.find_element_by_xpath('//*[@id="selDate_PerBtn"]').click()
            time.sleep(10)
            dateymdcp = driver.find_element_by_xpath('//*[@id="selDate_Btn"]/label/span').text
        while True:
            print("---------------------------start scrapy data-----------------------------")
            dayscrapy(driver,excelcolunm)
            dateymdcp = driver.find_element_by_xpath('//*[@id="selDate_Btn"]/label/span').text
            if dateymdcp ==dateymdcs:
                break
            driver.find_element_by_xpath('//*[@id="selDate_PerBtn"]').click()
            time.sleep(10)


    elif choicemode=="4":
        pass

    driver.close()

if __name__ == '__main__':
    main()

