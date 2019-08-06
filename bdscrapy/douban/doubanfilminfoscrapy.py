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
    arrayfilminfo = ['' for col in range(0, 20)]
    arraydirector = [['' for col in range(0, 2)] for row in range(0, 10)]
    # page_results = [['' for col in range(0,1)] for row in range(0,20)]
    arrayscriptwriter = [['' for col in range(0, 2)] for row in range(0, 20)]
    arrayactor = [['' for col in range(0, 2)] for row in range(0, 100)]

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
    #global array1
    # for i in (1,20):
    #     array1.append(0)
    #     i+=1
    temp0=driver.title #webpage title
    if temp0.find('豆瓣')<0:
        driver.refresh()
    arrayfilminfo[0]=re.search(r'(.+?)(?=\(豆瓣\))',temp0).group() #film chinese simple name
    print("电影名称是：%s" %arrayfilminfo[0])
    temp1 = getelementvalue("//DIV[@class='related-info']/H2[1]/I[1]|//DIV[@id='content']/H1[1]/SPAN[1]",driver)
    arrayfilminfo[1] =temp1.replace(arrayfilminfo[0],'') #film original language filmname
    temp2=getelementvalue("//SPAN[@class='year']",driver)
    if temp2!='':
        temp20=re.search(r'\d{4}',temp2).group()
        arrayfilminfo[2] = int(temp20)  # film first release year
    #else: temp20=''

    arrayfilminfo[3]=getelementvalue("//DIV[@id='info']/SPAN[1]/SPAN[1][contains(text(),'导演')]/following-sibling::span[1]",driver) #director //DIV[@id='info']/SPAN[1]/SPAN[2]
    arrayfilminfo[4]=getelementvalue("//span[contains(text(),'编剧')]/following-sibling::span[1]",driver) #screenplay
    arrayfilminfo[5]=getelementvalue("//SPAN[@class='actor']/SPAN[2]",driver) #actor
    temp6=getelementvalue("//DIV[@id='info']",driver) #film type
    #print("temp6 is: %s" %temp6)
    #print("type of temp6 is %s" %type(temp6))
    if temp6.find('类型:')>-1:
        arrayfilminfo[6]=re.search(r'(?<=类型:)(.+)\b',temp6).group()
    else:arrayfilminfo[6]=''
    if temp6.find('制片国家/地区:')>-1:
        arrayfilminfo[7]=re.search(r'(?<=制片国家/地区:)(.+)\b',temp6).group()
        #print("which country:%s" %arrayfilminfo[7])
    else:arrayfilminfo[7]=''
    if temp6.find('语言:')>-1:
        arrayfilminfo[8]=re.search(r'(?<=语言:)(.+)\b',temp6).group()
    else:arrayfilminfo[8]=''
    if temp6.find('上映日期:')>-1:
        arrayfilminfo[9]=re.search(r'(?<=上映日期:)(.+)',temp6).group()
    else:arrayfilminfo[9]=''
    if temp6.find('片长:')>-1:
        arrayfilminfo[10]=re.search(r'(?<=片长:)(.+)',temp6).group()
    else:arrayfilminfo[10]=''
    if temp6.find('又名:')>-1:
        arrayfilminfo[11]=re.search(r'(?<=又名:)(.+)',temp6).group()
    else:arrayfilminfo[11]=''
    arrayfilminfo[12]=getelementvalue("//span[text()='IMDb链接:']/following-sibling::a[1]",driver) #IMDB链接
    temp13=getelementvalue("//STRONG[@class='ll rating_num']",driver) #豆瓣评分
    if temp13!='':
        arrayfilminfo[13]=float(temp13)
    temp14=getelementvalue("//A[@class='rating_people']/SPAN[1]",driver) #评分人数
    if temp14!='':
        arrayfilminfo[14]=int(temp14)
    arrayfilminfo[15]=weblink


    if temp6.find('导演:')>-1:
        #//DIV[@id='info']/SPAN[1]/SPAN[1][contains(text(),'导演')]//following-sibling::span[1]/a
        elements = driver.find_elements_by_xpath("//DIV[@id='info']/SPAN/SPAN[contains(text(),'导演')]//following-sibling::span[1]/a")
        #print("导演内容是：%s" %elements)
        elementcounts = elements.__len__()
        #print("总共有 %d 位导演。" % elementcounts)
        #page_results = [['' for col in range(excelcolunm)] for row in range(elementcounts)]

        for i in range(1, elementcounts+1):
            arraydirector[i-1][0]=driver.find_element_by_xpath("//DIV[@id='info']/SPAN/SPAN[contains(text(),'导演')]//following-sibling::span[1]/a[%d]" % i).text #导演名字
            print("导演名字是: %s" % arraydirector[i-1][0])
            arraydirector[i-1][1]=driver.find_element_by_xpath("//DIV[@id='info']/SPAN/SPAN[contains(text(),'导演')]//following-sibling::span[1]/a[%d]" %i).get_attribute('href') #导演链接
            print("导演链接是: %s" %arraydirector[i-1][1])

    if temp6.find('编剧:')>-1:
        #//DIV[@id='info']/SPAN[2]/SPAN[1][contains(text(),'编剧:')]//following-sibling::span[1]/a
        elements1 = driver.find_elements_by_xpath("//DIV[@id='info']/SPAN/SPAN[contains(text(),'编剧')]//following-sibling::span[1]/a")
        #print("编剧内容是：%s" %elements1)
        element1counts = elements1.__len__()
        #print("总共有 %d 位编剧。" %element1counts)
        #page_results = [['' for col in range(excelcolunm)] for row in range(elementcounts)]

        for i in range(1, element1counts+1):
            arrayscriptwriter[i-1][0]=driver.find_element_by_xpath("//DIV[@id='info']/SPAN/SPAN[contains(text(),'编剧')]//following-sibling::span[1]/a[%d]" % i).text #导演名字
            #print("编剧名字是: %s" % arrayscriptwriter[i-1][0])
            arrayscriptwriter[i-1][1]=driver.find_element_by_xpath("//DIV[@id='info']/SPAN/SPAN[contains(text(),'编剧')]//following-sibling::span[1]/a[%d]" %i).get_attribute('href') #导演链接
            #print("编剧链接是: %s" %arrayscriptwriter[i-1][1])

    if temp6.find('主演:')>-1:
        #//DIV[@id='info']/SPAN[3]/SPAN[1][contains(text(),'主演:')]//following-sibling::span[1]/span
        elements2 = driver.find_elements_by_xpath("//DIV[@id='info']/SPAN/SPAN[contains(text(),'主演')]//following-sibling::span[1]/span")
        #print("主演内容是：%s" %elements2)
        element2counts = elements2.__len__()
        #print("总共有 %d 位主演。" %element2counts)
        #page_results = [['' for col in range(excelcolunm)] for row in range(elementcounts)]

        for i in range(1, element2counts+1):
            arrayactor[i-1][0]=driver.find_element_by_xpath("//DIV[@id='info']/SPAN/SPAN[contains(text(),'主演')]//following-sibling::span[1]/span[%d]/a" % i).get_attribute('textContent') #导演名字
            #print("演员名字是: %s" % arrayactorinfo[i-1][0])
            arrayactor[i-1][1]=driver.find_element_by_xpath("//DIV[@id='info']/SPAN/SPAN[contains(text(),'主演')]//following-sibling::span[1]/span[%d]/a" %i).get_attribute('href') #导演链接
            #print("演员链接是: %s" %arrayactorinfo[i-1][1])



    return arrayfilminfo,arraydirector,arrayscriptwriter,arrayactor




    #driver.close()

def main():
    conn = pymysql.connect(host="localhost", user="root", passwd="123456", db="body")
    cur = conn.cursor()
    # cur.execute("INSERT INTO table VALUE something")
    count=cur.execute("select dbflink from doubanfilmtbs \
where dbflink not in(select DISTINCT doubanlink from doubanfilmdirectorinfo) \
and dbflink not in (select doubanlink from doubanfilminfo)")
    print("总共有%d条纪录" %count)
    allinfo=cur.fetchmany(count)
    print('***********************Open Page********************************')
    driver = webdriver.Chrome()
    for everydata in allinfo:
        # print(everydata)
        # print(type(everydata))
        # print(everydata[0])
        # print(type(everydata[0]))
        if everydata[0].find("?")<0:
            (arrayfilminfo,arraydirector,arrayscriptwriter,arrayactor)=openpageandscrapydata(everydata[0],driver)
            #print("是否是剧集: %s" %array1[17])
            #tvplayflag                                         filmengname
        insertfilminfodata = """INSERT INTO doubanfilminfo (doubanfilmname,director,screenplayer,actor,category,region,language,releasedate,timelength,alternatename,
                doubanscore,doubanscorenum,doubanlink,imdblink,remark) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"""
        values1 = (
        arrayfilminfo[0], arrayfilminfo[3], arrayfilminfo[4], arrayfilminfo[5], arrayfilminfo[6], arrayfilminfo[7],
        arrayfilminfo[8], arrayfilminfo[9], arrayfilminfo[10],
        arrayfilminfo[11], arrayfilminfo[13], arrayfilminfo[14], arrayfilminfo[15], arrayfilminfo[12],'0423pythonscrapy')
        cur.execute(insertfilminfodata, values1)

        index1=0
        while(arraydirector[index1][0]!=''):
            insertdirectordata = """INSERT INTO doubanfilmdirectorinfo (doubanfilmname,doubanlink,directorname,peoplelink)VALUES (%s, %s, %s, %s)"""
            values2=(arrayfilminfo[0],arrayfilminfo[15],arraydirector[index1][0],arraydirector[index1][1])
            cur.execute(insertdirectordata, values2)
            index1+=1

        index2 = 0
        while (arrayscriptwriter[index2][0] != ''):
            inserscriptwriterdata = """INSERT INTO doubanfilmscriptwriterinfo (doubanfilmname,doubanlink,scriptwritername,peoplelink) 
                                    VALUES (%s, %s, %s, %s)"""
            values3 = (arrayfilminfo[0], arrayfilminfo[15], arrayscriptwriter[index2][0], arrayscriptwriter[index2][1])
            cur.execute(inserscriptwriterdata, values3)
            index2 += 1

        index3 = 0
        while (arrayactor[index3][0] != ''):
            inseractordata = """INSERT INTO doubanfilmactorinfo (doubanfilmname,doubanlink,actorname,peoplelink) 
                                            VALUES (%s, %s, %s, %s)"""
            values4 = (arrayfilminfo[0], arrayfilminfo[15], arrayactor[index3][0], arrayactor[index3][1])
            cur.execute(inseractordata, values4)
            index3 += 1
    # 执行sql语句

        conn.commit()

    cur.close()
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
