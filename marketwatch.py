from splinter import Browser
from selenium.webdriver.common.keys import Keys
import pandas
import time
import random
import threading

SCROLL_TIMES = 200
RUNNING_THREADS = 20

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


## delete previous csv
##for infile in glob.glob(os.path.join(path, '*.csv') ):
##    os.remove(infile)
codes_list = []
with open('US_codes.txt', 'r') as f:
    codes_list = f.readlines()
    f.close()
#
# with open('CNN_not_found.txt', 'r') as f:
#     list_404 = f.readlines()
#     f.close()
# print('not found list: ', list_404)
#
# with open('checked_list.txt', 'r') as f:
#     checked_list = f.readlines()
#     f.close()
# print('checked list: ', checked_list)
global running_list
running_list = []




def action(code):
    global running_list
    global date_list, context_list, url_list, title_list, listening_list
    global csv_dictionary
    csv_dictionary = {'url':'', 'date':'', 'context':'', 'title':'', 'listening':''}
    with Browser('firefox',profile_preferences=prof) as browser:
        # Visit URL

        # fast test
        # code = 'AA'

        url = 'https://www.marketwatch.com/investing/stock/'+code+'/news'
        browser.visit(url)
        if browser.is_element_not_present_by_css('.headlinewrapper') or browser.is_element_present_by_text('No News currently available for '):
            # running_list.pop()
            return
        element = browser.find_by_css('.headlinewrapper').first
        element.mouse_over()

        print(code+'crawling')
        scroll_times = SCROLL_TIMES
        try:
            while scroll_times > 0:
                for i in range(0, random.randint(30,50)):
                    element.type(Keys.DOWN)
                time.sleep(0.5)
                scroll_times -= 1
        except:
            pass

        url_list = []
        title_list = []
        date_list = []
        context_list = []
        listening_list = []
        if browser.is_element_present_by_css('.headlinewrapper>ol>li>div>p>a'):
            for hrefs in browser.find_by_css('.headlinewrapper>ol>li>div>p>a'):
                if hrefs['href'] in url_list:
                    continue

                if hrefs['href'] != None:
                    if 'marketwatch.' not in str(hrefs['href']):
                        print(hrefs['href'])
                        continue

                    if hrefs['text'] != None:
                        title = str(hrefs['text'])
                    else:
                        title = 'N/A'

                    with Browser('firefox', profile_preferences=prof) as new_browser:
                        new_browser.visit(str(hrefs['href']))
                        if new_browser.is_element_present_by_id('article-body'):
                            body = str(new_browser.find_by_id('article-body').value)
                            body = body.replace('\n', ' ')
                        else:
                            body = 'N/A'
                        if new_browser.is_element_present_by_id('published-timestamp'):
                            date = new_browser.find_by_id('published-timestamp')
                            date = str(date.value).replace('Published: ', '')
                        else:
                            date = 'N/A'
                        # print('date:',date, 'body:',body)
                        if(new_browser.find_by_css('.fyre-stream-livecount')):
                            listening = new_browser.find_by_css('.fyre-stream-livecount')
                            listening = str(listening.value).split()[0]

                        else:
                            listening = 'N/A'

                        url_list.append(str(hrefs['href']))
                        title_list.append(title)
                        date_list.append(date)
                        context_list.append(body)
                        listening_list.append(listening)

        print(code + 'finish')
        print(len(url_list), len(title_list), len(date_list), len(context_list), len(listening_list))
        # print((url_list), (title_list), (date_list), (context_list), (listening_list))
        pandas.DataFrame({'url': url_list, 'title': title_list, 'date': date_list, 'context': context_list, 'listening': listening_list}).to_csv('./marketwatch/'+code+".csv", index=False, sep=',')
        # running_list.pop()



while codes_list:


    print('rest codes', len(codes_list))
    for threads in running_list:
        if threads.is_alive():
            pass
        else:
            running_list.remove(threads)
    while len(running_list) < RUNNING_THREADS:
        if not codes_list:
            break
        code = codes_list.pop(0)
        t = threading.Thread(target=action, args=(code,), name=code)
        t.start()
        running_list.append(t)
    time.sleep(3)




