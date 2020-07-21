import requests
import streamlit as st
import bs4
from lxml import html
from bs4 import BeautifulSoup
from distutils.filelist import findall
import re
import pandas as pd
import functools
from urllib.request import urlopen
from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
import time
import datetime
import random
import os
def Search(dept,arrv,date,cur,ali):
    url = 'https://www.google.com/flights?hl=zh-CN#'
    df_record = pd.DataFrame(columns=['日期','始发机场','到达机场','航空公司' ,'航班号','票价','官网购票链接'])  
#     dept='LAX'
#     arrv='SFO'
#     date='2020-11-21'
#     cur='USD'
#     ali='UA'
    if date.month <10:
        mo='0'+str(date.month)
    else:
        mo=str(date.month)
    if date.day <10:
        da='0'+str(date.day)
    else:
        da=str(date.day)
    date1=str(date)
    date2=str(date.year)[:2]+str(mo)+str(da)
    date3=str(date.year)+str(mo)+str(da)

    #this part is use to optimize the server, if you run on your local computer, or if you got any problem from these part you can just delete some of them
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280x1696')
    chrome_options.add_argument('--user-data-dir=/tmp/user-data')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    chrome_options.add_argument('--v=99')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--data-path=/tmp/data-path')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--homedir=/tmp')
    chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    #chrome_options.binary_location = "/usr/bin/chromium-browser"  #if you are using google chrome, not chromium, you dont need this row


    driver = webdriver.Chrome(chrome_options=chrome_options)
    url1=url+'flt='+dept+'.'+arrv+'.'+date1+';c:'+cur+';e:1'+';s:0;a:'+ali+';sd:1;t:f;tt:o'
    driver.get(url1)
    #wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".gws-flights__flex-filler")))
    time.sleep(1)
    #results = driver.find_elements_by_class_name('LJTSM3-v-d')
    #search=driver.find_elements_by_xpath("//div[@class='gws-flights-results__carriers']")
    #print(driver.find_element_by_css_selector('.gws-flights-results__itinerary-price').text)
    elem = driver.find_element_by_xpath("//*")
    source_code = elem.get_attribute("outerHTML")
    driver.quit()
    bs = BeautifulSoup(source_code, 'html.parser')
    a = bs.find_all('div', class_='gws-flights-results__itinerary-card-summary')
    if a==[]:
        pass
    else:
        for tag in a: 
            fls = tag.findAll('div', class_='gws-flights-results__carriers')
            a1=str(a)
            #for i in range(1,12):
                #if i <= a1.count('gws-flights-results__carriers'):
            fl=fls[0].get_text()
            num = str(tag.find('div',class_="gws-flights-results__select-header gws-flights__flex-filler"))
            num1 = num[num.find(arrv):num.find('class')][4:9]
            price=tag.find('div', class_='gws-flights-results__itinerary-price').text
            global link
            if ali=='UA':
                link='https://www.united.com/ual/en/US/flight-search/book-a-flight/results/rev?f='+dept+'&t='+arrv+'&d='+date1+'&tt=1&sc=7&px=1&taxng=1&newHP=True&idx=1'
            elif ali=='MU':
                link='http://www.ceair.com/booking/'+dept+'-'+arrv+'-'+date2+'_CNY.html'
            elif ali=='CZ':
                link='https://oversea.csair.com/new/us/zh/flights?m=0&p=100&flex=1&t='+dept+'-'+arrv+'-'+date3
            elif ali=='MF':
                link='https://www.xiamenair.com/zh-cn/nticket.html?tripType=OW&orgCodeArr%5B0%5D='+dept+'&dstCodeArr%5B0%5D='+arrv+'&orgDateArr%5B0%5D='+date1+'&dstDate=&isInter=true&adtNum=1&chdNum=0&JFCabinFirst=false&acntCd=&mode=Money&partner=false&jcgm=false' 
            elif ali=='HU':
                link='https://new.hnair.com/hainanair/ibe/deeplink/ancillary.do?DD1='+date1+'&DD2=&TA=1&TC=0&TI=0&TM=&TP=&ORI='+dept+'&DES='+arrv+'&SC=A&ICS=F&PT=F&FLC=1&CKT=&DF=&NOR=&PACK=T&HC1=&HC2=&NA1=&NA2=&NA3=&NA4=&NA5=&NC1=&NC2=&NC3=&NC4='
            elif ali=='3U':
                link='http://www.sichuanair.com/'
            elif ali=='JD':
                link='https://new.jdair.net/jdair/?tripType=OW&originCode='+dept+'&destCode='+arrv+'&departureDate='+date1+'&returnDate=&cabinType=ECONOMY&adtNum=1&chdNum=0&const_id=5f0a8017p2ZZg9hvG7URRHemkpAMhpvwRfIFTPm1&token=#/ticket/tripList'
            elif ali=='LH':
                link='https://www.lufthansa.com/cn/zh/homepage'
            elif ali=='TK':
                link='https://www.turkishairlines.com/zh-cn/index.html'
            elif ali=='CA':
                link='http://et.airchina.com.cn/InternetBooking/AirLowFareSearchExternal.do?&tripType=OW&searchType=FARE&flexibleSearch=false&directFlightsOnly=false&fareOptions=1.FAR.X&outboundOption.originLocationCode='+dept+'&outboundOption.destinationLocationCode='+arrv+'&outboundOption.departureDay='+str(da)+'&outboundOption.departureMonth='+str(mo)+'&outboundOption.departureYear='+str(date.year)+'&outboundOption.departureTime=NA&guestTypes%5B0%5D.type=ADT&guestTypes%5B0%5D.amount=1&guestTypes%5B1%5D.type=CNN&guestTypes%5B1%5D.amount=0&guestTypes%5B3%5D.type=MWD&guestTypes%5B3%5D.amount=0&guestTypes%5B4%5D.type=PWD&guestTypes%5B4%5D.amount=0&pos=AIRCHINA_CN&lang=zh_CN&guestTypes%5B2%5D.type=INF&guestTypes%5B2%5D.amount=0'
            else:
                link=url1
            df_record = df_record.append({'日期':date1, '始发机场':dept,'到达机场':arrv,'航空公司':fl, '航班号':num1, '票价':price, '官网购票链接':link}, ignore_index=True)
    df_record['官网购票链接'] = df_record['官网购票链接'].apply(make_clickable, args = ('点击前往',))
    return df_record

def NA(start,end,cur):
    date=start
    df1 = pd.DataFrame(columns=['日期','始发机场','到达机场','航空公司' ,'航班号','票价','官网购票链接']) 
    while date <= end:
        if date.weekday()==0:
            df1=df1.append(Search('LAX','XMN',date,cur,'MF'))
            date=date+datetime.timedelta(days=1)
            time.sleep(random.randint(0,10)/10)
        elif date.weekday()==1:
            date=date+datetime.timedelta(days=1)
        elif date.weekday()==2:
            df1=df1.append(Search('JFK','PVG',date,cur,'MU'))
            time.sleep(random.randint(0,10)/10)
            df1=df1.append(Search('SFO','PVG',date,cur,'UA'))
            time.sleep(random.randint(0,10)/10)
            df1=df1.append(Search('YYZ','PEK',date,cur,'HU'))
            time.sleep(random.randint(0,10)/10)
            df1=df1.append(Search('YVR','CAN',date,cur,'CZ'))
            time.sleep(random.randint(0,10)/10)
            df1=df1.append(Search('YVR','CTU',date,cur,'3U'))
            time.sleep(random.randint(0,10)/10)
            date=date+datetime.timedelta(days=1)
        elif date.weekday()==3:
            df1=df1.append(Search('SEA','PVG',date,cur,'DL'))
            date=date+datetime.timedelta(days=1)
            time.sleep(random.randint(0,10)/10)
        elif date.weekday()==4:
            df1=df1.append(Search('DTW','PVG',date,cur,'DL'))
            time.sleep(random.randint(0,10)/10)
            df1=df1.append(Search('YVR','XMN',date,cur,'MF'))
            time.sleep(random.randint(0,10)/10)
            date=date+datetime.timedelta(days=1)
        elif date.weekday()==5:
            df1=df1.append(Search('YYZ','PVG',date,cur,'MU'))
            time.sleep(random.randint(0,10)/10)
            df1=df1.append(Search('SFO','PVG',date,cur,'UA'))
            date=date+datetime.timedelta(days=1)
            time.sleep(random.randint(0,10)/10)
        else:
            df1=df1.append(Search('YVR','PEK',date,cur,'CA'))
            time.sleep(random.randint(0,10)/10)
            df1=df1.append(Search('LAX','PEK',date,cur,'CA'))
            time.sleep(random.randint(0,10)/10)
            df1=df1.append(Search('LAX','CAN',date,cur,'CZ'))
            time.sleep(random.randint(0,10)/10)
            date=date+datetime.timedelta(days=1)
    return df1