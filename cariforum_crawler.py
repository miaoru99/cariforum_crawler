from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import more_itertools
import re
import time
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import csv

class crawler:
    def __init__(self, binary, exec_path, keyw):
        self.keyw = keyw
        options = Options()
        options.headless = False
        # options.headless = True #linux
        options.binary = binary
        cap = DesiredCapabilities().FIREFOX
        cap["marionette"] = True #optional
        self.driver = webdriver.Firefox(options=options, capabilities=cap, executable_path=exec_path)
    
    def close_driver(self):
        self.driver.close()
        self.driver.quit()
    
    def find_title_link_dt(cc):
        time1 = 0
        done = False
        curr_date = datetime.now()
        tdate = curr_date.strftime("%d-%m-%Y_%H:%M:%S") 
        while not done:
            try:
                title = cc.find_element_by_xpath('.//h3[@class="xs3"]')
                link = cc.find_element_by_xpath('.//h3[@class="xs3"]/a[@href]')
                datetime1 = cc.find_element_by_xpath('.//p[3]//span')
                s = datetime1.text
                dt = s.split(" ", 1)
                mth = re.search (r"\-([A-Za-z0-9_]+)\-", dt[0])
                return title.text, link.get_attribute("href"), dt[0],str(mth.group(1)),dt[1]
            except:
                if time1 == 10:
                    return ""
                    done = True
                else:
                    print("start date time 2:",tdate)           
                    time.sleep(10)
                    time1 += 10
                    done = False
                    
    def find_detail(cc,detailList):
        time1 = 0
        done = False
        curr_date = datetime.now()
        tdate = curr_date.strftime("%d-%m-%Y_%H:%M:%S") 
        while not done:
            try:
                detailList.append(cc.find_element_by_class_name("xg1").text)
                done = True
            except:
                if time1 == 180:
                    detailList.append("")
                    done = True
                else:
                    print("start date time 3:",tdate)           
                    time.sleep(60)
                    time1 += 60
                    done = False
            
            
    def find_author(cc,authorList):
        time1 = 0
        done = False
        curr_date = datetime.now()
        tdate = curr_date.strftime("%d-%m-%Y_%H:%M:%S") 
        while not done:
            try:
                author = cc.find_element_by_xpath('.//p[3]//span[2]')
                authorList.append(author.text)
                done = True
            except:
                if time1 == 180:
                    authorList.append("")
                    done = True
                else:
                    print("start date time 5:",tdate)           
                    time.sleep(60)
                    time1 += 60
                    done = False
    
    def find(driver):
        done = False
        time1 = 0
        curr_date = datetime.now()
        tdate = curr_date.strftime("%d-%m-%Y_%H:%M:%S") 
        while not done:
            try:
                content2 = driver.find_element_by_xpath(('//div[@id="threadlist" and @class="slst mtw"]'))
                return content2
                done = True
            except:
                if time1 == 20:
                    return ""
                else:
                    print("start date time 6:",tdate)           
                    time.sleep(20)
                    time1 += 20
                    done = False
    
    def find2(driver):
        done = False
        time1 = 0
        curr_date = datetime.now()
        tdate = curr_date.strftime("%d-%m-%Y_%H:%M:%S") 
        while not done:
            try:
                content2 = driver.find_element_by_xpath(('//div[@id="threadlist" and @class="slst mtw"]'))
                contents2 = content2.find_elements_by_xpath(('//li[@class="pbw"]'))
                return contents2
                done = True
            except:
                if time1 == 20:
                    return ""
                else:
                    print("start date time 7:",tdate)           
                    time.sleep(20)
                    time1 += 20
                    done = False
    
    def findPg1(driver):
        done = False
        curr_date = datetime.now()
        tdate = curr_date.strftime("%d-%m-%Y_%H:%M:%S") 
        while not done:
            try:
                writer2 = driver.find_elements_by_xpath(('//div[@class="authi"]//a[@class="xw1"]'))
                return writer2
                done = True
            except:
                print("start date time 8:",tdate)           
                time.sleep(60)
                done = False
    
    def findPg2(driver):
        done = False
        curr_date = datetime.now()
        tdate = curr_date.strftime("%d-%m-%Y_%H:%M:%S") 
        while not done:
            try:
                postTime2 = driver.find_elements_by_xpath(('//div[@class="authi"]//em'))
                return postTime2
                done = True
            except:
                print("start date time 9:",tdate)           
                time.sleep(60)
                done = False
    
    def findPg3(driver):
        sleep = 0
        done = False
        curr_date = datetime.now()
        tdate = curr_date.strftime("%d-%m-%Y_%H:%M:%S")  
        while not done:
            try:
                postContent2 = driver.find_elements_by_xpath(('//div[@class="t_fsz"]//table//tbody//tr//td'))
                return postContent2
                done = True
            except:
                print("start date time 11:",tdate)           
                time.sleep(60)
                sleep += 60
                if sleep <= 180:
                    done = True
                else:    
                    return []
                    done = False
    
    def findEdit(driver):
        try:
            postEdit = driver.find_elements_by_xpath(('//div[@class="t_fsz"]//table//tbody//tr//td//i'))
            return postEdit
        except:
            return []
            pass
        
    def findQuote(driver):
        try:
            postQuote = driver.find_elements_by_xpath(('//div[@class="t_fsz"]//table//tbody//tr//td//div[@class="quote"]'))
            return postQuote
        except:
            return []
            pass
                
    def find_searchbar(driver,keyword):
        done = False
        time1 = 0
        curr_date = datetime.now()
        tdate = curr_date.strftime("%d-%m-%Y_%H:%M:%S") 
        while not done:
            try:
                elem = driver.find_element_by_name("srchtxt")
                elem.clear()
                elem.send_keys(keyword)
                submit = driver.find_element_by_id('scform_submit')
                submit.click()
                done = True
            except:
                if time1 == 10:
                    driver.get("https://bm.cari.com.my/search.php?mod=forum")
                    elem = driver.find_element_by_name("srchtxt")
                    elem.clear()
                    elem.send_keys(keyword)
                    submit = driver.find_element_by_id('scform_submit')
                    submit.click()
                    done = True
                elif crawler.no_post(driver) == "":
                    print("start date time 12:",tdate)           
                    time.sleep(10)
                    time1 += 10
                    done = False
                    
    def find_searchbar_cn(driver,keyword):
        done = False
        time1 = 0
        curr_date = datetime.now()
        tdate = curr_date.strftime("%d-%m-%Y_%H:%M:%S") 
        while not done:
            try:
                elem = driver.find_element_by_name("srchtxt")
                elem.clear()
                elem.send_keys(keyword)
                submit = driver.find_element_by_id('scform_submit')
                submit.click()
                done = True
            except:
                if time1 == 180:
                    driver.get("https://cn.cari.com.my/search.php?mod=forum")
                    elem = driver.find_element_by_name("srchtxt")
                    elem.clear()
                    elem.send_keys(keyword)
                    submit = driver.find_element_by_id('scform_submit')
                    submit.click()
                    done = True
                elif crawler.no_post(driver) == "":
                    print("start date time 13:",tdate)           
                    time.sleep(60)
                    time1 += 60
                    done = False

    def no_post(driver):
        try:
            driver.find_element_by_xpath(('//div[@id="messagetext" and @class="alert_error"]//p')).text == "The post not found"
        except NoSuchElementException:
            return ""
        
    def get_link(driver,link):
        done = False
        time1 = 0
        curr_date = datetime.now()
        tdate = curr_date.strftime("%d-%m-%Y_%H:%M:%S") 
        while not done:
            try:
                driver.get(link)
                done = True
            except:
                if time1 == 180:
                    return ""
                    done = True
                else:
                    time.sleep(60)
                    time1 += 60
                    done = False
                    
    def crawler_CariBM(self, directory):
        now = datetime.now()
        csv_date = datetime.now().strftime("%Y%m%d_%H%M%S")
        text_file_name = 'CariBM_' + csv_date + '.txt'
        with open(text_file_name, 'w', newline = '', encoding = 'utf-8') as file:
            file.write('Link\tPost\tDetail\tDate\tTime\tAuthor\tContent\tComments\tComments2')
        
        foundrateList = []
        self.driver.get("https://bm.cari.com.my/search.php?mod=forum")
        
        for keyword in self.keyw:
            titleList = []
            linkList = []
            detailList = []
            dateList = []
            timeList = []
            authorList = []
            contentList = []
            replierList = []
            comments2 = []
            foundrate = 0
            crawler.find_searchbar(self.driver,keyword)
            time.sleep(10)
            
            if crawler.find(self.driver) == "" or crawler.find2(self.driver) == "":
                continue
            
            content = crawler.find(self.driver)
            contents = crawler.find2(self.driver)
            
            for bb in contents:
                if crawler.find_title_link_dt(bb) == "":
                    continue
                else:
                    title,link1,date1,mth1,time1 = crawler.find_title_link_dt(bb)
                
                if re.search(keyword.lower(),title.lower()) and date1[-4:] == str(now.year) and (mth1 == str(now.month) or mth1 == str(now.month-1)):
                    titleList.append(title)
                    linkList.append(link1)
                    crawler.find_detail(bb,detailList)
                    dateList.append(date1)
                    timeList.append(time1)
                    crawler.find_author(bb,authorList)
                    foundrate += 1
                else:
                    continue
            page_number = 2
            while True:
                try:
                    link = self.driver.find_element_by_link_text(str(page_number))
                except NoSuchElementException:
                    break
                link.click()
                
                content2 = crawler.find(self.driver)
                contents2 = crawler.find2(self.driver)
                
                for cc in contents2:
                    if crawler.find_title_link_dt(cc) == "":
                        continue
                    else:
                        title,link1,date1,mth1,time1 = crawler.find_title_link_dt(cc)
                    
                    if re.search(keyword.lower(),title.lower()) and date1[-4:] == str(now.year) and (mth1 == str(now.month) or mth1 == str(now.month-1)):
                        titleList.append(title)
                        linkList.append(link1)
                        crawler.find_detail(cc,detailList)
                        dateList.append(date1)
                        timeList.append(time1)
                        crawler.find_author(cc,authorList)
                        foundrate += 1
                    else:
                        continue
                page_number += 1
            
            foundrateList.append(foundrate)
            no = 0
            for olink in linkList:
                comm2 = ""
                replierList2 = []
                if crawler.get_link(self.driver,olink) == "":
                    continue
                else:
                    crawler.get_link(self.driver,olink)
                try:
                    time.sleep(10)
                    writer = self.driver.find_elements_by_xpath(('//div[@class="authi"]//a[@class="xw1"]'))
                    postTime = self.driver.find_elements_by_xpath(('//div[@class="authi"]//em'))
                    postContent = crawler.findPg3(self.driver)
                    postEdit = crawler.findEdit(self.driver)
                    postQuote = crawler.findQuote(self.driver)
                    unwantedInfo = postEdit + postQuote
                    if not postContent:
                        contentList.append("")
                    else:
                        mycontent = str(postContent[0].text)
                        contentList.append(mycontent.replace("\r", " ").replace("\n", " "))
                    replier = 1
                    replierno = len(writer) 
                    time.sleep(5)
                    while replier < replierno:
                        a_dictionary ={}
                        a_dictionary["Replier"] = str(writer[replier].text)
                        a_dictionary["Date_Time"] = str(postTime[replier].text)
                        if not postContent:
                            a_dictionary["Comment"] = ""
                        elif replier >= len(postContent):
                            a_dictionary["Comment"] = ""
                        else:
                            if str(postEdit[replier].text) in str(postContent[replier].text):
                                comm = str(postContent[replier].text).replace(str(postEdit[replier].text), '')
                                a_dictionary["Comment"] = comm
                                a_string = str(postContent[replier].text)
                                comm2 += a_string.replace("\r", " ").replace("\n", " ") 
                            elif str(postQuote[replier].text) in str(postContent[replier].text):
                                comm = str(postContent[replier].text).replace(str(postQuote[replier].text), '')
                                a_dictionary["Comment"] = comm
                                a_string = str(postContent[replier].text)
                                comm2 += a_string.replace("\r", " ").replace("\n", " ") 
                            elif not unwantedInfo:
                                a_dictionary["Comment"] = str(postContent[replier].text)
                                a_string = str(postContent[replier].text)
                                comm2 += a_string.replace("\r", " ").replace("\n", " ") 
                            else:
                                for elem in unwantedInfo:
                                    if str(elem.text) in str(postContent[replier].text):
                                        comm = str(postContent[replier].text).replace(str(elem.text), '')
                                        a_dictionary["Comment"] = comm
                                        a_string = comm
                                        comm2 += a_string.replace("\r", " ").replace("\n", " ")  
                        replierList2.append(a_dictionary.copy())
                        replier += 1
                        
                    postPages = 2
                    while True:
                        try:
                            link = self.driver.find_element_by_link_text(str(postPages))
                        except NoSuchElementException:
                            break
                        link.click()
                        postPages += 1
                
                        time.sleep(5)
                        writer2 = crawler.findPg1(self.driver)
                        postTime2 = crawler.findPg2(self.driver)
                        postContent2 = crawler.findPg3(self.driver)
                        postEdit2 = crawler.findEdit(self.driver)
                        postQuote2 = crawler.findQuote(self.driver)
                        unwantedInfo2 = postEdit2 + postQuote2
                        replier2 = 0
                        replierno2 = len(writer2) 
                        time.sleep(5)
                        while replier2 < replierno2:
                            a_dictionary ={}
                            a_dictionary["Replier"] = str(writer2[replier2].text)
                            a_dictionary["Date_Time"] = str(postTime2[replier2].text)
                            if not postContent2:
                                a_dictionary["Comment"] = ""
                            elif replier2 >= len(postContent2):
                                a_dictionary["Comment"] = ""
                            elif not unwantedInfo2:
                                a_dictionary["Comment"] = str(postContent2[replier2].text)
                                a_string = str(postContent2[replier2].text)
                                comm2 += a_string.replace("\r", " ").replace("\n", " ") 
                            else:
                                for elem in unwantedInfo2:
                                    if str(elem.text) in str(postContent2[replier2].text):
                                        comm = str(postContent2[replier2].text).replace(str(elem.text), '')
                                        a_dictionary["Comment"] = comm
                                        a_string = comm
                                        comm2 += a_string.replace("\r", " ").replace("\n", " ") 
                            replierList2.append(a_dictionary.copy())
                            
                            replier2 += 1
                    
                    str_rep = str(replierList2).replace("\r", " ").replace("\n", " ") 
                    replierList.append(str_rep)
                    comments2.append(comm2)
                    if not replierList:
                        replierList.append("")
                        comments2.append("")
                except:
                    contentList.append("")
                    replierList.append("")
                    comments2.append("")
                    pass
            
                with open(text_file_name, 'a', newline = '', encoding = 'utf-8') as file:
                    file.write('\n'+str(linkList[no])+'\t'+str(titleList[no])+'\t'+str(detailList[no])+'\t'+str(dateList[no])+'\t'+str(timeList[no])+'\t'+str(authorList[no])+'\t'+str(contentList[no])+'\t'+str(replierList[no])+'\t'+str(comments2[no]))
                no += 1
                
        return text_file_name

        
    def crawler_CariCN(self, directory):
        now = datetime.now()
     
        csv_date = datetime.now().strftime("%Y%m%d_%H%M%S")
        text_file_name = directory + '\\CariCN_' + csv_date + '.txt'
        with open(text_file_name, 'w', newline = '', encoding = 'utf-8') as file:
            file.write('Link\tPost\tDetail\tDate\tTime\tAuthor\tContent\tComments\tComments2')
        
        foundrateList = []
        
        self.driver.get("https://cn.cari.com.my/search.php?mod=forum")
        
        for keyword in self.keyw:
            titleList = []
            linkList = []
            detailList = []
            dateList = []
            timeList = []
            authorList = []
            contentList = []
            replierList = []
            comments2 = []
            foundrate = 0
            crawler.find_searchbar_cn(self.driver,keyword)
            time.sleep(5)
           
            content = crawler.find(self.driver)
            contents = crawler.find2(self.driver)
            
            for bb in contents:
                if crawler.find_title_link_dt(bb) == "":
                    continue
                else:
                    title,link1,date1,mth1,time1 = crawler.find_title_link_dt(bb)
                
                if date1[-4:] == str(now.year) and (mth1 == str(now.month) or mth1 == str(now.month-1)):
                    titleList.append(title)
                    linkList.append(link1)
                    crawler.find_detail(bb,detailList)
                    dateList.append(date1)
                    timeList.append(time1)
                    crawler.find_author(bb,authorList)
                    foundrate += 1
                else:
                    continue
            page_number = 2
            while True:
                try:
                    link = self.driver.find_element_by_link_text(str(page_number))
                except NoSuchElementException:
                    break
                link.click()
                
                content2 = crawler.find(self.driver)
                contents2 = crawler.find2(self.driver)
                
                for cc in contents2:
                    if crawler.find_title_link_dt(cc) == "":
                        continue
                    else:
                        title,link1,date1,mth1,time1 = crawler.find_title_link_dt(cc)
                    
                    if date1[-4:] == str(now.year) and (mth1 == str(now.month) or mth1 == str(now.month-1)):
                        titleList.append(title)
                        linkList.append(link1)
                        crawler.find_detail(cc,detailList)
                        dateList.append(date1)
                        timeList.append(time1)
                        crawler.find_author(cc,authorList)
                        foundrate += 1
                    else: 
                        continue
                page_number += 1
            
            foundrateList.append(foundrate)
            no = 0
            for olink in linkList:
                comm2 = ""
                replierList2 = []
                if crawler.get_link(self.driver,olink) == "":
                    continue
                else:
                    crawler.get_link(self.driver,olink)
                try:
                    writer = self.driver.find_elements_by_xpath(('//div[@class="authi"]//a[@class="xw1"]'))
                    postTime = self.driver.find_elements_by_xpath(('//div[@class="authi"]//em'))
                    postContent = crawler.findPg3(self.driver)
                    postEdit = crawler.findEdit(self.driver)
                    postQuote = crawler.findQuote(self.driver)
                    unwantedInfo = postEdit + postQuote
                    
                    if not postContent:
                        contentList.append("")
                    else:
                        mycontent = str(postContent[0].text)
                        contentList.append(mycontent.replace("\r", " ").replace("\n", " "))
                    
                    replier = 1
                    replierno = len(writer) 
                    time.sleep(5)
                    while replier < replierno:
                        a_dictionary ={}
                        a_dictionary["Replier"] = str(writer[replier].text)
                        a_dictionary["Date_Time"] = str(postTime[replier].text)
                        if not postContent:
                            a_dictionary["Comment"] = ""
                        elif replier >= len(postContent):
                            a_dictionary["Comment"] = ""
                        elif not unwantedInfo:
                            a_dictionary["Comment"] = str(postContent[replier].text)
                            a_string = str(postContent[replier].text)
                            comm2 += a_string.replace("\r", " ").replace("\n", " ") 
                        else:
                            for elem in unwantedInfo:
                                if str(elem.text) in str(postContent[replier].text):
                                    comm = str(postContent[replier].text).replace(str(elem.text), '')
                                    a_dictionary["Comment"] = comm
                                    a_string = comm
                                    comm2 += a_string.replace("\r", " ").replace("\n", " ")  
                        replierList2.append(a_dictionary.copy())
                        replier += 1
                        
                    postPages = 2
                    while True:
                        try:
                            link = self.driver.find_element_by_link_text(str(postPages))
                        except NoSuchElementException:
                            break
                        link.click()
                        postPages += 1
                        time.sleep(5)
                        writer2 = crawler.findPg1(self.driver)
                        postTime2 = crawler.findPg2(self.driver)
                        postContent2 = crawler.findPg3(self.driver)
                        postEdit2 = crawler.findEdit(self.driver)
                        postQuote2 = crawler.findQuote(self.driver)
                        unwantedInfo2 = postEdit2 + postQuote2
                        replier2 = 0
                        replierno2 = len(writer2) 
                        time.sleep(5)
                        while replier2 < replierno2:
                            a_dictionary ={}
                            a_dictionary["Replier"] = str(writer2[replier2].text)
                            a_dictionary["Date_Time"] = str(postTime2[replier2].text)
                            if not postContent2:
                                a_dictionary["Comment"] = ""
                            elif replier2 >= len(postContent2):
                                a_dictionary["Comment"] = ""
                            elif not unwantedInfo2:
                                a_dictionary["Comment"] = str(postContent2[replier2].text)
                                a_string = str(postContent2[replier2].text)
                                comm2 += a_string.replace("\r", " ").replace("\n", " ") 
                            else:
                                for elem in unwantedInfo2:
                                    if str(elem.text) in str(postContent2[replier2].text):
                                        comm = str(postContent2[replier2].text).replace(str(elem.text), '')
                                        a_dictionary["Comment"] = comm
                                        a_string = comm
                                        comm2 += a_string.replace("\r", " ").replace("\n", " ") 
                            replierList2.append(a_dictionary.copy())
                            
                            replier2 += 1
                    str_rep = str(replierList2).replace("\r", " ").replace("\n", " ") 
                    replierList.append(str_rep)
                    comments2.append(comm2)
                    if not replierList:
                        replierList.append("")
                except:
                    contentList.append("")
                    replierList.append("")
                    comments2.append("")
                    pass
                
                with open(text_file_name, 'a', newline = '', encoding = 'utf-8') as file:
                    file.write('\n'+str(linkList[no])+'\t'+str(titleList[no])+'\t'+str(detailList[no])+'\t'+str(dateList[no])+'\t'+str(timeList[no])+'\t'+str(authorList[no])+'\t'+str(contentList[no])+'\t'+str(replierList[no])+'\t'+str(comments2[no]))
                no += 1
            
        return text_file_name



kw = ['肺炎']
c_chi = crawler(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe', r'C:\ProgramData\Anaconda3\Lib\site-packages\selenium\webdriver\firefox\geckodriver.exe', kw)
file_name = c_chi.crawler_CariCN('C:\\Users\\Administrator\\Desktop\\')
print(file_name)

kw = ['covid']
c_mly = crawler(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe', r'C:\ProgramData\Anaconda3\Lib\site-packages\selenium\webdriver\firefox\geckodriver.exe', kw)
file_name = c_mly.crawler_CariBM('C:\\Users\\Administrator\\Desktop\\')
print(file_name)
