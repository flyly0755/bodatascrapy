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

def dayscrapy(driver):
    # print()
    iflast=isElementExist('//*[@id="minirefresh"]/div[2]/div[6]/p[2][contains(text(),"没有更多数据了")]',driver)

    while not iflast:
        target = driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div/ul[last()]')
        driver.execute_script("arguments[0].scrollIntoView();", target)
        time.sleep(2)
        iflast = isElementExist('//*[@id="minirefresh"]/div[2]/div[6]/p[2][contains(text(),"没有更多数据了")]', driver)
    time.sleep(2)
    elements = driver.find_elements_by_xpath('//*[@id="TableWrap"]/div[1]/div/ul')
    #print("elements内容是：%s" %elements)
    elementcounts =elements.__len__()
    print("总共有 %d 条纪录。" %elementcounts)
    page_results = [[0 for col in range(17)] for row in range(300)]
    #print("page_results是%s"%page_results)
    workbook = xlrd.open_workbook('C:/Users/dell/PycharmProjects/project-scrapy/test1.xls')  # 打开excel文件
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    #worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    worksheet =workbook.sheet_by_index(0) # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)
    row=0
    dateymd1 = driver.find_element_by_xpath('//*[@id="selDate_Btn"]/label/span').text  # 日期年月日
    for i in range(1, elementcounts+1):
        page_results[i-1][0]=datetime.strptime(dateymd1 , "%Y-%m-%d")
    for i in range(1, elementcounts+1):
        #page_results[i-1] =[]
        #print("i-1得值为",i-1)
        try:
            page_results[i-1][1]=driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div/ul[%d]' % i).get_attribute('data-ent') #电影编号
            #print("电影编号是：%s" %page_results[i-1][1])
            page_results[i-1][2]=driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div/ul[%d]/li[1]/div/p[1]' % i).text #电影片名
            #print("电影片名是：%s" %page_results[i-1][2])
            xpathifee='//*[@id="TableWrap"]/div[1]/div/ul['+str(i)+']/li[1]/div/p[1]/i'
            #print(xpathifee)
            ifee=isElementExist(xpathifee, driver)
            if ifee:
                page_results[i-1][3]=driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div/ul[%d]/li[1]/div/p[1]/i' % i).text #首映点映flag
                #print("首映点映flag是：%s" %page_results[i-1][3])
            page_results[i-1][4]=driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div[2]/ul[%d]/li[1]/div/p[2]/span[1]' % i).text #上映天数
            #print("上映天数是：%s" % page_results[i-1][4])
            page_results[i-1][5]=driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div[2]/ul[%d]/li[1]/div/p[2]' % i).text #上映总票房(亿万)
            #print("上映总票房(亿万)是：%s" % page_results[i-1][5])
            page_results[i-1][6]=driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div[2]/ul[%d]/li[2]/div' % i).get_attribute('textContent') #当日票房
            #print("当日票房是：%s" % page_results[i-1][6])
            page_results[i-1][7]=driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div[2]/ul[%d]/li[3]' % i).get_attribute('textContent') #当日场次
            #print("当日场次是：%s" % page_results[i-1][7])
            page_results[i-1][8]=driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div[2]/ul[%d]/li[4]' %i).get_attribute('textContent') #当日排座
            #print("当日排座是：%s" % page_results[i-1][8])
            page_results[i-1][9]=driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div[2]/ul[%d]/li[5]' %i).get_attribute('textContent') #当日人次
            page_results[i-1][10]=driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div[2]/ul[%d]/li[6]' %i).get_attribute('textContent') #累计票房（万）
            page_results[i-1][11]=driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div[2]/ul[%d]/li[7]' %i).get_attribute('textContent') #当日票房占比
            page_results[i-1][12] = driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div[2]/ul[%d]/li[8]' % i).get_attribute('textContent')  # 当日场次占比
            page_results[i-1][13] = driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div[2]/ul[%d]/li[9]' % i).get_attribute('textContent')  # 上座率
            page_results[i-1][14] = driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div[2]/ul[%d]/li[10]' % i).get_attribute('textContent')  # 当日排座占比
            page_results[i-1][15] = driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div[2]/ul[%d]/li[11]' % i).get_attribute('textContent')  # 平均票价
            page_results[i-1][16] = driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div[2]/ul[%d]/li[12]' % i).get_attribute('textContent')  # 场均人次
            #driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div/ul[%d]' % i).get_attribute('data-ent')
                # print('%d. ' % i + driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div/ul[%d]' % i).get_attribute('data-ent'))  # 获取电影编号
                # print('%d. ' % i + driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div/ul[%d]/li[1]/div/p[1]' % i).text)

            for index in range(17):  # 依次写入每一行
                new_worksheet.write(row+rows_old, index, page_results[i-1][index])
            row +=1

        except NoSuchElementException as msg:
            continue

        new_workbook.save('C:/Users/dell/PycharmProjects/project-scrapy/test1.xls')
    print("共有行数据：%d" % (row + rows_old))


def moreindex(driver):
    # 点击更多指标
    driver.find_element_by_xpath('//*[@id="selIndex_Btn"]').click()
    time.sleep(2)
    # 点击排座
    driver.find_element_by_xpath('//*[@id="selFilmIndex_List_Movie_Index_Day_"]/div/ul/li[4]').click()
    time.sleep(1)
    # 点击人次
    driver.find_element_by_xpath('//*[@id="selFilmIndex_List_Movie_Index_Day_"]/div/ul/li[5]').click()
    time.sleep(1)
    # 点击累计票房
    driver.find_element_by_xpath('//*[@id="selFilmIndex_List_Movie_Index_Day_"]/div/ul/li[6]').click()
    time.sleep(1)
    # 点击票房占比
    driver.find_element_by_xpath('//*[@id="selFilmIndex_List_Movie_Index_Day_"]/div/ul/li[7]').click()
    time.sleep(1)
    # 点击场次占比
    driver.find_element_by_xpath('//*[@id="selFilmIndex_List_Movie_Index_Day_"]/div/ul/li[8]').click()
    time.sleep(1)
    # 点击平均票价
    driver.find_element_by_xpath('//*[@id="selFilmIndex_List_Movie_Index_Day_"]/div/ul/li[11]').click()
    time.sleep(1)
    # 点击场均人次
    driver.find_element_by_xpath('//*[@id="selFilmIndex_List_Movie_Index_Day_"]/div/ul/li[13]').click()
    time.sleep(1)
    # 点击确定
    driver.find_element_by_xpath('//*[@id="selFilmIndex_YesBtn"]').click()
    time.sleep(10)

def main():
    print('***********************Open Page********************************')
    driver = webdriver.Firefox()
    url = 'http://ebotapp.entgroup.cn/DataBox/Film/Movie/Index'
    driver.get(url)
    time.sleep(10)
    moreindex(driver)
    dateymd = driver.find_element_by_xpath('//*[@id="selDate_Btn"]/label/span').text  # 日期年月日
    while dateymd  != '2018-12-31':
        driver.find_element_by_xpath('//*[@id="selDate_PerBtn"]').click()
        time.sleep(10)
        dayscrapy(driver)
        dateymd = driver.find_element_by_xpath('//*[@id="selDate_Btn"]/label/span').text


    #driver.close()

if __name__ == '__main__':
    main()

