from selenium.webdriver.chrome.options import Options
from splinter import Browser
from selenium import webdriver
import os
import glob
import sys
import csv
import time
import random
##options = Options()
##options.add_argument('"excludeSwitches", ["ignore-certificate-errors"]')

##fp.set_preference("browser.download.dir","C:\Users\Oscar\Desktop\stock")


##with Browser('firefox', profile="C:\\Users\Oscar\AppData\Local\Mozilla\Firefox\Profiles") as browser:

##os.rmdir("C:\\Users\Oscar\Desktop\stockdata")
prof = {}
prof['browser.download.manager.showWhenStarting'] = 'false'
prof['browser.helperApps.alwaysAsk.force'] = 'false'
prof['browser.download.dir'] = "/home/ohan/Desktop/stockdata"
prof['browser.download.folderList'] = 2
prof['browser.helperApps.neverAsk.saveToDisk'] = 'text/csv, application/csv, text/html,application/xhtml+xml,application/xml, application/octet-stream, application/pdf, application/x-msexcel,application/excel,application/x-excel,application/excel,application/x-excel,application/excel, application/vnd.ms- excel,application/x-excel,application/x-msexcel,image/png,image/jpeg,text/html,text/plain,application/msword,application/xml,application/excel,text/x-c'
prof['browser.download.manager.useWindow'] = 'false'
prof['browser.helperApps.useWindow'] = 'false'
prof['browser.helperApps.showAlertonComplete'] = 'false'
prof['browser.helperApps.alertOnEXEOpen'] = 'false'
prof['browser.download.manager.focusWhenStarting']= 'false'


skip_dict = {}

## delete previous csv
##for infile in glob.glob(os.path.join(path, '*.csv') ):
##    os.remove(infile)
codes_list = []
with open('US_codes.txt', 'r') as f:
    codes_list = f.readlines()
    f.close()

with open('CNN_not_found.txt', 'r') as f:
    list_404 = f.readlines()
    f.close()
print('not found list: ', list_404)

with open('checked_list.txt', 'r') as f:
    checked_list = f.readlines()
    f.close()
print('checked list: ', checked_list)


with Browser('firefox',profile_preferences=prof) as browser:

    while(codes_list):
        # Visit URL
        code = codes_list.pop(0)[:-1]
        print(code)
        if code+'\n' in list_404:
            print('in 404 list!')
            continue

        if code+'\n' in checked_list:
            print('checked')
            continue

        # fast test
        # code = 'AAPL'


        url = 'http://money.cnn.com/quote/news/news.html?symb='+code
        browser.visit(url)
        time.sleep(random.randint(4, 5))

        checked_list.append(code+'\n')
        with open('checked_list.txt', 'w') as f:
            f.writelines(checked_list)
            f.close()


        if browser.is_text_present('Symbol not found'):
            print('not found')
            list_404.append(code+'\n')
            with open('CNN_not_found.txt', 'w') as f:
                f.writelines(list_404)
                f.close()

            continue
        elif browser.is_text_present('No recent news for'):
            print('skip')
            continue

        # if browser.is_element_present_by_css('.firstCol'):
        #     print('gotta')
        #     for hrefs in browser.find_by_css('.firstCol'):
        #         print(hrefs.text)
        url_list = []
        title_list = []
        data_list = []
        if browser.is_element_present_by_css('.wsod_newsTable>tbody>tr>td'):
            print('right!')
            for hrefs in browser.find_by_css('.wsod_newsTable>tbody>tr>td>a'):
                url_list.append("'"+hrefs['href']+"'"+' ')
                title_list.append(hrefs['text']+' ')
            for hrefs in browser.find_by_css('.wsod_newsTable>tbody>tr>td>div'):
                data_list.append("'"+hrefs.text+"'"+' ')


        with open('cnn_money.txt', 'a') as f:
            f.writelines(code)
            f.writelines('\n')
            f.writelines(url_list)
            f.writelines('\n')
            f.writelines(title_list)
            f.writelines('\n')
            f.writelines(data_list)
            f.writelines('\n')
            f.close()

        print(len(url_list), len(title_list), len(data_list))


        print('done')

        #     print(l.first.text)





