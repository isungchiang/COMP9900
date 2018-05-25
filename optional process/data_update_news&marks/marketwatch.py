from splinter import Browser
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
import pandas
import time
import random
import threading

SCROLL_TIMES = 300
RUNNING_THREADS = 1
SLEEP_PERIOD = 0.3

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
prof['browser.headless'] = 'true'


## delete previous csv
##for infile in glob.glob(os.path.join(path, '*.csv') ):
##    os.remove(infile)
codes_list = []
if '404_list.txt' not in file_list:
    with open('404_list.txt', 'w') as f:
        f.write('\n')

if 'checked_list.txt' not in file_list:
    with open('checked_list.txt', 'w') as f:
        f.write('\n')

with open('./bigcompany.txt', 'r') as f:
    codes_list = f.readlines()
    f.close()
print(codes_list)
#
with open('./404_list.txt', 'r') as f:
    list_404 = f.readlines()
    f.close()
# print('not found list: ', list_404)
#
with open('./checked_list.txt', 'r') as f:
    checked_list = f.readlines()
    f.close()

print('checked list: ', checked_list)
global running_list
running_list = []


def action(code):
    with Browser('firefox', profile_preferences=prof)as browser:
        url = 'https://www.marketwatch.com/investing/stock/'+code+'/news'
        try:
            browser.visit(url)
        except WebDriverException:
            print(code+': visit failed')
            with open('./404_list.txt', 'a') as f:
                f.writelines(code+'\n')
                f.close()
            return
        if browser.is_element_not_present_by_css('.headlinewrapper') or browser.is_element_present_by_text('No News currently available for '):
            # running_list.pop()
            with open('./checked_list.txt', 'a') as f:
                f.writelines(code+'\n')
                f.close()
            return
        element = browser.find_by_css('.headlinewrapper').first
        # element.mouse_over()

        print(code+'crawling')
        scroll_times = SCROLL_TIMES
        try:
            while scroll_times > 0:
                for i in range(0, random.randint(30,50)):
                    element.type(Keys.DOWN)
                time.sleep(SLEEP_PERIOD)
                scroll_times -= 1
        except:
            pass

        code_index_list = []
        url_list = []
        title_list = []

        if browser.is_element_present_by_css('.headlinewrapper>ol>li>div>p>a'):

            for hrefs in browser.find_by_css('.headlinewrapper>ol>li>div>p>a'):
                if hrefs['href'] in url_list:
                    continue

                if hrefs['href'] != None:
                    if 'marketwatch.' not in str(hrefs['href']):
                        # print(hrefs['href'])
                        continue
                    # print(hrefs['href'])
                    if hrefs['text'] != None:
                        title = str(hrefs['text'])
                    else:
                        title = 'N/A'

                    code_index_list.append(code)
                    url_list.append(hrefs['href'])
                    title_list.append(title)

        print(code + 'finish')
        print(len(code_index_list), len(url_list), len(title_list))
        pandas.DataFrame({'code': code_index_list, 'url': url_list, 'title': title_list}).to_csv('./'+ 'URL_' + code + ".csv", index=False, sep=',')

    with open('./checked_list.txt', 'a') as f:
        f.writelines(code+'\n')
        f.close()


while codes_list:


    # print('rest codes', len(codes_list))
    for threads in running_list:
        if threads.is_alive():
            pass
        else:
            running_list.remove(threads)
    while len(running_list) < RUNNING_THREADS:
        if not codes_list:
            break
        code = codes_list.pop(0)
        if code in checked_list:
            print(code+'checked')
            # print('rest:', len(codes_list))
            continue
        if code in list_404:
            print(code+'not found')
            continue
        else:
            code = str(code).replace('\n', '')
            print('rest codes', len(codes_list))
            t = threading.Thread(target=action, args=(code,), name=code)
            t.start()
            running_list.append(t)
            checked_list.append(code)
    time.sleep(3)





