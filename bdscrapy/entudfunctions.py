# coding=utf-8
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
import time
import xlrd
from xlutils.copy import copy
from datetime import datetime
import re

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

def dayscrapy(driver,excelcolunm):
    #global excelcolunm
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
    page_results = [['' for col in range(excelcolunm)] for row in range(elementcounts)]
    #print("page_results是%s"%page_results)
    workbook = xlrd.open_workbook('C:/Users/dell/PycharmProjects/project-scrapy/dayboscrapy.xls')  # 打开excel文件
    #sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    #worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    worksheet =workbook.sheet_by_index(0) # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt可写对象
    new_worksheet = new_workbook.get_sheet(0)
    row=0
    dateymd1 = driver.find_element_by_xpath('//*[@id="selDate_Btn"]/label/span').text  # 日期年月日
    daytbostring= driver.find_element_by_xpath('//*[@id="Info_SummaryNum"]').text #日总票房'
    daytbo=''
    if "万" in daytbostring:
        daytbo=int(re.sub(r'[,.万]','',daytbostring,0))*1000
    elif "亿" in daytbostring:
        daytbo = int(re.sub(r'[,.亿]', '', daytbostring, 0)) * 1000000
    print("daytbo值是：%s" %daytbo)
    for i in range(1, elementcounts+1):
        page_results[i-1][0]=datetime.strptime(dateymd1 , "%Y-%m-%d")
        page_results[i-1][1]=daytbo
    for i in range(1, elementcounts+1):
        #page_results[i-1] =[]
        #print("i-1得值为",i-1)
        try:
            temp0=driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div/ul[%d]' % i).get_attribute('data-ent') #电影编号
            page_results[i-1][2]="http://www.cbooo.cn/m/"+temp0
            #print("电影编号是：%s" %page_results[i-1][1])
            temp1=driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div/ul[%d]/li[1]/div/p[1]' % i).text #电影片名
            #page_results[i-1][3]=temp1.replace("","")
            page_results[i-1][3] = re.sub(r' (点|首)映$','',temp1,1,flags=re.I )
            #print("电影片名是：%s" %page_results[i-1][2])
            xpathifee='//*[@id="TableWrap"]/div[1]/div/ul['+str(i)+']/li[1]/div/p[1]/i'
            #print(xpathifee)
            ifee=isElementExist(xpathifee, driver)
            if ifee:
                page_results[i-1][4]=driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div/ul[%d]/li[1]/div/p[1]/i' % i).text #首映点映flag
                #print("首映点映flag是：%s" %page_results[i-1][3])
            temp2=driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div[2]/ul[%d]/li[1]/div/p[2]/span[1]' % i).text #上映天数

            if "-" in temp2:
                page_results[i-1][5] = 5000
                page_results[i-1][6]=datetime.strptime(temp2 , "%Y-%m-%d")  #上映日期
            elif "首映" in temp1:
                page_results[i-1][5]=1
            elif "点映" in temp1:
                page_results[i-1][5] = -2000
            else:
                page_results[i-1][5]=temp2
            #print("上映天数是：%s" % page_results[i-1][4])
            page_results[i-1][7]=driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div[2]/ul[%d]/li[1]/div/p[2]' % i).text #上映信息（总票房，上映天数）
            #print("上映总票房(亿万)是：%s" % page_results[i-1][5])
            temp3=driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div[2]/ul[%d]/li[2]/div' % i).get_attribute('textContent') #当日票房
            temp3=re.sub(r',','',temp3,0)
            page_results[i-1][8]=float(temp3)*10000
            #print("当日票房是：%d"%page_results[i-1][8])
            #print("当日票房是：%s" % page_results[i-1][6])
            temp7=driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div[2]/ul[%d]/li[3]' % i).get_attribute('textContent') #当日场次
            page_results[i-1][9]= int(re.sub(r',', '', temp7, 0))
            temp8=driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div[2]/ul[%d]/li[4]' %i).get_attribute('textContent') #当日排座
            page_results[i-1][10]=int(re.sub(r',', '', temp8, 0))
            temp9=driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div[2]/ul[%d]/li[5]' %i).get_attribute('textContent') #当日人次
            page_results[i-1][11] = int(re.sub(r',', '', temp9, 0))
            temp4=driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div[2]/ul[%d]/li[6]' %i).get_attribute('textContent') #累计票房（万）
            temp4 = re.sub(r',', '', temp4, 0)
            page_results[i-1][12]=float(temp4)*10000
            page_results[i-1][13]=driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div[2]/ul[%d]/li[7]' %i).get_attribute('textContent') #当日票房占比
            page_results[i-1][14] = driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div[2]/ul[%d]/li[8]' % i).get_attribute('textContent')  # 当日场次占比
            temp5 = driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div[2]/ul[%d]/li[9]' % i).get_attribute('textContent')  # 上座率
            page_results[i-1][15]=temp5.replace('%','')
            temp6 = driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div[2]/ul[%d]/li[10]' % i).get_attribute('textContent')  # 当日排座占比
            page_results[i - 1][16] = temp6.replace('%', '')
            page_results[i-1][17] = driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div[2]/ul[%d]/li[11]' % i).get_attribute('textContent')  # 平均票价
            page_results[i-1][18] = driver.find_element_by_xpath('//*[@id="TableWrap"]/div[1]/div[2]/ul[%d]/li[12]' % i).get_attribute('textContent')  # 场均人次
            page_results[i-1][19]=datetime.now()
            page_results[i-1][20]=i

            for index in range(excelcolunm):  # 依次写入每一行
                new_worksheet.write(row+rows_old, index, page_results[i-1][index])
            row +=1

        except NoSuchElementException as msg:
            continue

        while True:
            try:
                new_workbook.save('C:/Users/dell/PycharmProjects/project-scrapy/dayboscrapy.xls')
                break
            except  PermissionError as msg:
                print("dayboscrapy.xls已被打开，影响追加数据的保存，请关闭文件")
                time.sleep(10)
                continue
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
    driver.find_element_by_xpath('//*[@id="selFilmIndex_List_Movie_Index_Day_"]/div/ul/li[12]').click()
    time.sleep(1)
    # 点击确定
    driver.find_element_by_xpath('//*[@id="selFilmIndex_YesBtn"]').click()
    time.sleep(10)