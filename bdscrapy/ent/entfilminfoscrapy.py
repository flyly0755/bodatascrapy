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
import pymysql
import random

array1 = ['' for col in range(0,20)]

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

def getelementvalue(element,driver):
    if isElementExist(element,driver) ==True:
        return driver.find_element_by_xpath(element).text
    else:return ''


def openpageandscrapydata(weblink,driver):

    #url = 'https://movie.douban.com/'
    # 清除浏览器cookies
    #cookies = driver.get_cookies()
    #print(f"main: cookies = {cookies}")
    driver.delete_all_cookies()
    driver.get(weblink)
    time.sleep(random.randint(10, 30))
    #driver.maximize_window()  # 页面窗口最大化
    #temp01=driver.title
    #print("页面标题是：%s" %temp01)
    global array1
    # for i in (1,20):
    #     array1.append(0)
    #     i+=1
    temp0=driver.title #webpage title
    array1[0]=re.search(r'(.+?)(?=_电影详情)',temp0).group() #filmname
    print("电影名称是：%s" %array1[0])
    array1[1]=getelementvalue("//DIV[@class='cont']/H2[1]/P[1]",driver) #filmengname
    print("英文名称是：%s" % array1[1])
    temp2=getelementvalue("//SPAN[@class='m-span']",driver) #tbo
    if temp2 != '':
        temp20=re.search(r'(?<=\n)(.+?)(?=万)',temp2).group()
        temp20=float(temp20)
    else: temp20=''
    array1[2]=temp20
    print("tbo是：%s" %array1[2])
    temp3=getelementvalue("//DIV[@class='cont']/P[2]",driver) #film type
    array1[3]=temp3.replace('类型：','')
    print("film type是：%s" %array1[3])
    temp4=getelementvalue("//DIV[@class='cont']/P[3][contains(text(),'片长')]",driver) #timelength
    if temp4!=''and len(temp4)>6:
        temp40 =re.search(r'(?<=：)(.+?)(?=min|分钟)',temp4).group()
        if len(temp40)<4:
            temp40=int(temp40)
        else: temp40=''
    else: temp40=''
    array1[4]=temp40
    print("film timelength is %s" %array1[4])
    temp5=getelementvalue("//DIV[@class='cont']/P[contains(text(),'制式')]",driver)
    array1[5]=temp5.replace('制式：','')
    print("制式是 %s" %array1[5])
    temp6=getelementvalue("//DIV[@class='cont']/P[contains(text(),'国家及地区')]",driver)
    array1[6] = temp6.replace('国家及地区：', '')
    print("国家和地区是：%s" %array1[6])
    array1[7]=getelementvalue("//DL[@class='dltext']/DD[1]",driver)
    print("导演是：%s" %array1[7])
    array1[8]=getelementvalue("//DL[@class='dltext']/DD[2]",driver)
    print("演员是%s" %array1[8])
    array1[9]=getelementvalue("//DL[@class='dltext']/Dt[contains(text(),'制作公司')]/following-sibling::dd[1]",driver)
    print("制作公司是: %s"%array1[9])
    array1[10]=getelementvalue("//DL[@class='dltext']/Dt[contains(text(),'发行公司')]/following-sibling::dd[1]",driver)
    print("发行公司是：%s" %array1[10])
    array1[11]=weblink
    temp12=getelementvalue("//DIV[@class='cont']/P[4][contains(text(),'上映时间')]",driver)
    temp120=temp12.replace('上映时间：', '').replace('（中国）','')
    if temp120!=''and len(temp120)>=8:
        temp120=datetime.strptime(temp120, "%Y-%m-%d")
    else: temp120=''
    array1[12]=temp120
    print("上映日期是：%s"%array1[12])

    array1[13]=getelementvalue("//DIV[@class='cont']/P[contains(text(),'发行公司')]/A[1]",driver)
    print("全部发行公司是：%s" %array1[13])

    array1[14]=getelementvalue("//DIV[@class='cont']/P[7]/A[1]",driver)
    print("中国发行公司网址是：%s" %array1[14])
    array1[15]=getelementvalue("//DIV[@class='imgfl']/IMG[1]",driver)
    print("电影海报网址是：%s" %array1[15])
    array1[16]=getelementvalue("//DIV[@class='cont']",driver)
    #print("电影信息是：%s" %temp16)
    if array1[16].find("集数")>0:
        array1[17]='Y'
    else:  array1[17]='N'
    return array1




    #driver.close()

def main():
    conn = pymysql.connect(host="localhost", user="root", passwd="123456", db="body")
    cur = conn.cursor()
    # cur.execute("INSERT INTO table VALUE something")
    count=cur.execute("select filmentlink from entfilminfotba where filmentlink not in(select entlink from entfilminfotbs)")
    print("总共有%d条纪录" %count)
    allinfo=cur.fetchmany(count)
    print('***********************Open Page********************************')
    driver = webdriver.Firefox()
    for everydata in allinfo:
        # print(everydata)
        # print(type(everydata))
        # print(everydata[0])
        # print(type(everydata[0]))
        if everydata[0].find("?")<0:
            openpageandscrapydata(everydata[0],driver)
            #print("是否是剧集: %s" %array1[17])
            #tvplayflag                                         filmengname
        insertdata = """INSERT INTO entfilminfotbs (filmname,filmengname,entlink,tbo,releasedateinchina,
        type,timelength,standard,region,director,actor,productioncompany,issuingcompany,productioncompanyinchina,
        pcicweblink,picweblink,infoall,tvplayflag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)"""

        values = (array1[0], array1[1], array1[11], array1[2], array1[12], array1[3], array1[4],
                  array1[5], array1[6], array1[7], array1[8], array1[9], array1[10], array1[13], array1[14],
                  array1[15], array1[16],array1[17])

        # 执行sql语句
        cur.execute(insertdata, values)
        conn.commit()

    cur.close()
    conn.commit()
    conn.close()
    #datatestone = cur.fetchone()
    # #不能使用%datatestone,会报错TypeError: not all arguments converted during string formatting
    # #需要改成%(%datatestone,)
    # #print("datatest is %s" %datatestone)
    # print("datatest is %s"%(datatestone,))
    # print("-------------------------------")
    # dataall = cur.fetchall()
    # for dataoneline in dataall:
    #     print(dataoneline)


if __name__ == '__main__':
    main()
