from splinter import Browser
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import NoSuchElementException
import pandas
import time
import random
import threading
import os
import time

RUNNING_THREADS = 5
SLEEP_PERIOD = 0.3
BIG_500 = False

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
prof['browser.javascript.enabled']= False
prof['permissions.default.image']= 2
prof['dom.ipc.plugins.enabled.libflashplayer.so']= False
prof['webdriver.load.strategy'] =  'unstable'
prof['browser.load.strategy'] =  'unstable'

code_list = []
if (BIG_500==False):
    for csvs in (os.listdir('./')):
        if 'URL' not in csvs:
            continue
        if 'txt' in csvs:
            continue
        else:
            code_list.append(csvs)
else:
    with open('big_15.txt', 'r') as f:
        for i in f.readlines():
            code_list.append(i)
        f.close()

code_list.sort()
print(code_list)

with open('./404_URL_list.txt', 'r') as f:
    list_404 = f.readlines()
    f.close()
# print('not found list: ', list_404)
#
checked_list = []
with open('./checked_URL_list.txt', 'r') as f:
    for i in f.readlines():
        checked_ = i.replace('\n', '')
        checked_list.append(checked_)
    f.close()
print(checked_list)

def action(csv):
    urls = pandas.read_csv(csv)
    code_list = []
    title_list = []
    url_list = []
    date_list = []
    content_list = []
    listening_list = []
    print('start: ' + csv + ' ' + ' ' + 'len: ' + str(len(urls['code'])))
    check_points = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    start_time = time.clock()
    for i in range(0, len(urls['code'])):
        if check_points:
            ## progress bar
            print_progress = False
            while i/len(urls['code'])>check_points[0]:
                finished_ = check_points.pop(0)
                print_progress = True
            if print_progress:
                for pr in range(0, int(finished_*10)):
                    print('x', end='')
                for pr in range(0, int(10-finished_*10)):
                    print('-', end='')
                print(' | estimated resisting time: '+str((time.clock()-start_time)*(1-i/len(urls['code']))) )

        url = (urls['url'][i])
        with Browser('firefox', profile_preferences=prof) as new_browser:
            try:
                new_browser.visit(url)
            except:
                continue
            try:
                if new_browser.is_element_present_by_id('article-body'):
                    try:
                        body = str(new_browser.find_by_id('article-body').value)
                        body = body.replace('\n', ' ')
                    except NoSuchElementException:
                        body = 'N/A'
                else:
                    body = 'N/A'
            except NoSuchWindowException:
                body = 'N/A'
            if new_browser.is_element_present_by_id('published-timestamp'):
                date = new_browser.find_by_id('published-timestamp')
                try:
                    date = str(date.value).replace('Published: ', '')
                except:
                    date= 'N/A'
            else:
                date = 'N/A'
            # print('date:',date, 'body:',body)
            if new_browser.is_element_not_present_by_css('.fyre-livecount'):
                listening = 'N/A'
            else:
                if(new_browser.find_by_css('.fyre-livecount')):
                    listening = new_browser.find_by_css('.fyre-livecount')
                    listening = str(listening.value).split()[0]

                else:
                    listening = 'N/A'

            code_list.append(urls['code'][i])
            title_list.append(urls['title'][i])
            url_list.append(str(urls['url'][i]))
            date_list.append(date)
            listening_list.append(listening)
            content_list.append(body)


    code = str(csv).replace('URL', '')
    code = code.replace('.csv', '')
    pandas.DataFrame({'code': code_list, 'url': url_list, 'title': title_list, 'date':date_list, 'listening':listening_list, 'content': content_list}).to_csv(
        './marketwatch_content/' + 'content_' + code + ".csv", index=False, sep=',')
    print('|'+code+'|' + ' finish')
    with open('./checked_URL_list.txt', 'a') as f:
        f.writelines(csv+'\n')
        f.close()
#
#
#
#         print(code + 'finish')
#         print(len(code_index_list), len(url_list), len(title_list))
#
#         # print(len(url_list), len(title_list), len(date_list), len(context_list), len(listening_list))
#         # print((url_list), (title_list), (date_list), (context_list), (listening_list))
#         # pandas.DataFrame({'url': url_list, 'title': title_list, 'date': date_list, 'context': context_list, 'listening': listening_list}).to_csv('./marketwatch/'+code+".csv", index=False, sep=',')
#         # running_list.pop()
#
#
#
running_list = []



while code_list:
    # print('rest codes', len(codes_list))
    for threads in running_list:
        if threads.is_alive():
            pass
        else:
            running_list.remove(threads)
    while len(running_list) < RUNNING_THREADS:
        if not code_list:
            break
        csv = code_list.pop(0)
        if csv in checked_list:
            print('|'+csv+'| checked')
            # print('rest:', len(codes_list))
            continue
        if csv in list_404:
            print(csv+'not found')
            continue
        else:
            csv = str(csv).replace('\n', '')
            print('rest codes', len(code_list))
            t = threading.Thread(target=action, args=(csv,), name=csv)
            t.start()
            running_list.append(t)
            checked_list.append(csv)
            break
    time.sleep(3)

# l = []
# with open('big_companies.txt', 'r') as f:
#     for i in f.readlines():
#         codes = i.split()
#         num = codes[0]
#         csv = codes[1]
#         l.append(csv)
#         if int(num) < 500:
#             break
#     f.close()
#
#
# with open('big_500.txt', 'w') as f:
#     for i in l:
#         f.writelines(i+'\n')
#     f.close()
