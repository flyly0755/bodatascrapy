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

excelcolunm=10
excelfilepath='C:/Users/dell/PycharmProjects/project-scrapy/doubanfilmlist.xls'

def isElementExist(element,driver):
    flag = True
    #self.driver = driver
    try:
        #driver =webdriver.Firefox()
        driver.find_element_by_xpath(element)
        return flag
    except:
        flag = False
        return flag

def scrapydbdata(driver,filepath):
    workbookrd = xlrd.open_workbook(filepath)  # 打开excel文件
    worksheetrd = workbookrd.sheet_by_index(0)  # 获取工作簿中所有表格中的的第一个表格
    worksheetrd1 = workbookrd.sheet_by_index(1) #获取工作簿中所有表格中的的第二个表格
    workbookwt = copy(workbookrd)  # 将xlrd对象拷贝转化为xlwt可写对象
    worksheetwt = workbookwt.get_sheet(0)
    worksheetwt1=workbookwt.get_sheet(1)
    s1rows_old = worksheetrd1.nrows
    #print("rows_old is %d" % s1rows_old)

    for r in range(1, worksheetrd.nrows):
        dict1 = {}
        if worksheetrd.cell(r, 6).value != "Y":
            # temp0 = worksheet.cell(r, 0).ctype
            dict1["filmname"] = worksheetrd.cell(r, 0).value
            dict1["filmnamewosc"] = worksheetrd.cell(r, 1).value
            dict1["releaseyear"] = worksheetrd.cell(r, 3).value
            dict1["director"] = worksheetrd.cell(r, 4).value
            dict1["timelength"] = worksheetrd.cell(r, 5).value

            driver.find_element_by_xpath("//*[@id='inp-query']").clear()
            driver.find_element_by_xpath("//*[@id='inp-query']").send_keys(dict1["filmname"])
            time.sleep(1)
            driver.find_element_by_xpath("//*[@id='db-nav-movie']/div[1]/div/div[2]/form/fieldset/div[2]/input").click()
            time.sleep(10)
            elements = driver.find_elements_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div[1]/div')
            # print("elements内容是：%s" %elements)
            elementcounts = elements.__len__()
            print("总共有 %d 条纪录。" % elementcounts)
            page_results = [['' for col in range(excelcolunm)] for row in range(elementcounts)]



            for i in range(1, 5):
                try:
                    temp4 = driver.find_element_by_xpath(
                        '//*[@id="root"]/div/div[2]/div[1]/div[1]/div[%d]/div/div/div[1]/a' % i).get_attribute('href')
                    if temp4.find("subject") == -1:
                        continue
                    print("电影链接是：%s" % temp4)
                    # 第一行信息，包含中英文片名以及首映年份
                    temp0 = driver.find_element_by_xpath(
                        '//*[@id="root"]/div/div[2]/div[1]/div[1]/div[%d]/div/div/div[1]' % i).text
                    print("片名信息是：%s" % temp0)
                    # 剧集说明是电视剧，该记录排除
                    if temp0.find("[剧集]") == 1:
                        continue
                    if re.search(r'(?<=\()\d{4}(?=\))', temp0) == None:
                        temp01=''
                    else: temp01 = re.search(r'(?<=\()\d{4}(?=\))', temp0).group()
                    print("首映年份是%s" % temp01)
                    # 中文片名
                    temp02 = re.search(r'(.+?)(?= )', temp0).group()

                    # 导演名字
                    temp1 = driver.find_element_by_xpath(
                        '//*[@id="root"]/div/div[2]/div[1]/div[1]/div[%d]/div/div/div[4]' % i).text
                    if re.match(r'^[A-Za-z0-9\u4e00-\u9fa5· ]+(?= /)', temp1) == None:
                        temp11 = ''
                    else:
                        temp11 = re.match(r'^[A-Za-z0-9\u4e00-\u9fa5· ]+(?= /)', temp1).group()
                    print("导演是%s" % temp11)
                    # 片长
                    temp2 = driver.find_element_by_xpath(
                        '//*[@id="root"]/div/div[2]/div[1]/div[1]/div[%d]/div/div/div[3]' % i).text
                    print("电影信息：%s" % temp2)
                    if re.search(r'\d{2,3}(?=分钟)', temp2) == None:
                        temp20 = ''
                    else:
                        temp20 = re.search(r'\d{2,3}(?=分钟)', temp2).group()
                        temp21=int(temp20)
                    print("片长是%s" % temp21)
                    #print("type of temp21 is %s" %type(temp21))
                    #print("type of temp22 is %s" % type(temp22))
                    # if temp0.find(strin1)==1:
                    print("type of dict1[\"timelength\"] is: %s:" %dict1["timelength"])
                    print("type of dict1[\"releaseyear\"] is: %s " % dict1["releaseyear"])
                    if dict1["timelength"] =='':
                        inputtl=0
                    else: inputtl=int(dict1["timelength"])
                    if dict1["releaseyear"] =='':
                        inputry=0
                    else: inputry=int(dict1["releaseyear"])
                    if dict1["director"] == temp11 and inputtl == temp21:
                        worksheetwt1.write(s1rows_old, 0, dict1["filmname"])
                        worksheetwt1.write(s1rows_old, 1, inputtl)
                        worksheetwt1.write(s1rows_old, 2, inputry)
                        worksheetwt1.write(s1rows_old, 3, temp02)  # douban chinese filmname
                        worksheetwt1.write(s1rows_old, 4, temp01)  # douban first releaseyear
                        worksheetwt1.write(s1rows_old, 5, temp4)  # douban filmlink
                        worksheetwt1.write(s1rows_old, 6, temp11)  # douban film director
                        print("-------------1------------")
                        workbookwt.save(filepath)
                        s1rows_old+=1
                        break
                    if dict1["filmname"] == temp02 and inputtl == temp21:
                        worksheetwt1.write(s1rows_old, 0, dict1["filmname"])
                        worksheetwt1.write(s1rows_old, 1, inputtl)
                        worksheetwt1.write(s1rows_old, 2, inputry)
                        worksheetwt1.write(s1rows_old, 3, temp02)  # douban chinese filmname
                        worksheetwt1.write(s1rows_old, 4, temp01)  # douban first releaseyear
                        worksheetwt1.write(s1rows_old, 5, temp4)  # douban filmlink
                        worksheetwt1.write(s1rows_old, 6, temp11)  # douban film director
                        print("-------------2------------")
                        workbookwt.save(filepath)
                        s1rows_old += 1
                        break
                    if dict1["director"] == temp11 and dict1["filmname"] == temp02:
                        worksheetwt1.write(s1rows_old, 0, dict1["filmname"])
                        worksheetwt1.write(s1rows_old, 1, inputtl)
                        worksheetwt1.write(s1rows_old, 2, inputry)
                        worksheetwt1.write(s1rows_old, 3, temp02)  # douban chinese filmname
                        worksheetwt1.write(s1rows_old, 4, temp01)  # douban first releaseyear
                        worksheetwt1.write(s1rows_old, 5, temp4)  # douban filmlink
                        worksheetwt1.write(s1rows_old, 6, temp11)  # douban film director
                        print("-------------3------------")
                        workbookwt.save(filepath)
                        s1rows_old += 1
                        break

                    else:
                        worksheetwt1.write(s1rows_old, 0, dict1["filmname"])
                        worksheetwt1.write(s1rows_old, 1, inputtl)
                        worksheetwt1.write(s1rows_old, 2, inputry)
                        worksheetwt1.write(s1rows_old, 3, temp02)  # douban chinese filmname
                        worksheetwt1.write(s1rows_old, 4, temp01)  # douban first releaseyear
                        worksheetwt1.write(s1rows_old, 5, temp4)  # douban filmlink
                        worksheetwt1.write(s1rows_old, 6, temp11)
                        worksheetwt1.write(s1rows_old, 7, "待筛查")
                        workbookwt.save(filepath)
                        s1rows_old += 1
                        # temp0=driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div[1]/div[%d]/div/div/div[1]' % i).text
                        # print("片名信息是：%s" %temp0)
                        # if temp0.find("[剧集]")<0:
                        #     continue
                        # else:
                        #     page_results[i-][0]



                except NoSuchElementException as msg:
                    continue

            worksheetwt.write(r,6,"Y")
            workbookwt.save(filepath)

def getexceldate(driver,filepath):
    pass





def main(dated=None):


    print('***********************Open Page********************************')
    driver = webdriver.Firefox()
    url = 'https://movie.douban.com/'
    # 清除浏览器cookies
    cookies = driver.get_cookies()
    print(f"main: cookies = {cookies}")
    driver.delete_all_cookies()
    driver.get(url)
    time.sleep(10)
    driver.maximize_window() #页面窗口最大化

    scrapydbdata(driver,excelfilepath)

    driver.close()

if __name__ == '__main__':
    main()

