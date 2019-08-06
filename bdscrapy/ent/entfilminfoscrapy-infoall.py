# coding=utf-8

from selenium import webdriver

import time
import random
import re
import pymysql

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
    time.sleep(10)
    #driver.maximize_window()  # 页面窗口最大化
    #temp01=driver.title
    #print("页面标题是：%s" %temp01)
    global array1
    # for i in (1,20):
    #     array1.append(0)
    #     i+=1
    temp0=driver.title #webpage title
    array1[0]=re.search(r'(.+?)(?=_电影详情)',temp0).group() #filmname

    array1[11]=weblink

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
    count=cur.execute("select entlink from entfilminfo where (infoall is null or infoall='') \
     and entlink not in (select entlink from entinfoalltbs) and entlink not like '%?%'")
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
            openpageandscrapydata(everydata[0],driver)
            #print("是否是剧集: %s" %array1[17])
            #tvplayflag                                         filmengname
        insertdata = """INSERT INTO entinfoalltbs (filmname,entlink,infoall,tvplayflag) 
        VALUES (%s, %s, %s, %s)"""

        values = (array1[0], array1[11],array1[16],array1[17])
        time.sleep(random.randint(5, 30))
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
