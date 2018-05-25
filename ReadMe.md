
# ReadMe
## Team name
### FAFAFA
## Team member
XIAOCHEN HAN

ZHENG LI

RONGFA CHEN

YISONG JIANG
## Project name
### THE WIND
Advanced financial portfolio management system
## Build

Version Control:
Python 2.7.13 (Python 2.X should be working)
Flask 0.12.2

Required Libraries:
json, urllib, config, render_template, request, url_for, redirect, session

## Setup

Download from master branch as COMP9900-master.zip

```
$ unzip COMP9900-master.zip
$ cd COMP9900-master/flaskImplementation/
$ python2 flaskImplementation.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 232-029-348
```
Visit http://127.0.0.1:5000/ in browser

You can decide to use “guest mode” or “log in mode” to use our project.

## Data Maintenance (local)

Environment: Python, firefox 4.8+
Required Libraries: splinter

### Run marketwatch.py to crawler the url of the news from marketwatch.com
1. You have to prepare a code list stored in ‘bigcompany.txt’ for example.
2. You can adjust SCROLL_TIMES and RUNNING_THREADS in the head of codes
 
### Run content _crawler.py to crawl the contents
1. You should run in the same file
2. It will read the csv files downloaded by news crawler
3. You can stop it any time and it can continue crawling in next time
4. You can adjust RUNNING_THREADS in the head

### Run sum.py to merge all the data and saved in news_fixed_date.csv
1. Upload it to api to prepare for next operation
2. In this step, you should comment ‘merge_marks()’ in the bottom
3. Run fix_date.py in the end because the change of website we have to fix the format
 
### Run the news_training.py to analyze the news
1. Just run it
2. After running, send it to remote api
 
### After uploading two files to remote, run stock_mark.py to get the stock marks into merged_json.csv
1. run sum.py in the end, comment ‘merge_news()’ at bottom
 
### Update merged_json.csv to remote
