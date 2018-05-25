
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

## Notice：We use free account of Microsoft Auzre, the service will be stoped after 2018/06/01. If you run this porject after that date, please contact any of us to renew the account!!!

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



## Optional Part:
The project do not need the following configuration to run. Read it if you are interested in our methods to build database and web apis.

### Data Maintenance (local)

Environment: Python, firefox 4.8+
Required Libraries: splinter

#### Run marketwatch.py to crawler the url of the news from marketwatch.com
1. You have to prepare a code list stored in ‘bigcompany.txt’ for example.
2. You can adjust SCROLL_TIMES and RUNNING_THREADS in the head of codes
 
#### Run content _crawler.py to crawl the contents
1. You should run in the same file directory
2. It will read the csv files downloaded by news crawler
3. You can stop it any time and it can continue crawling in next time
4. You can adjust RUNNING_THREADS in the head

#### Run sum.py to merge all the data and saved in news_fixed_date.csv
1. Upload it to api to prepare for next operation
2. In this step, you should comment ‘merge_marks()’ in the bottom
3. Run fix_date.py in the end because the change of website we have to fix the format
 
#### Run the news_training.py to analyze the news
1. Just run it
2. After running, send it to remote api
 
#### After uploading two files to remote, run stock_mark.py to get the stock marks into merged_json.csv
1. Run sum.py in the end, comment ‘merge_news()’ at bottom
 
#### Update merged_json.csv to remote

### Build and import data to a Neo4j database:
Required: python3, neo4j-v1,  Microsoft Azure Account

File: neo4j/import.py

After crawling data from different web site, save them in a csv file(with \t as separation mark). Upload all csv files to a remote storage. Since we deployed it in Azure, an account is required. Create a Neo4j cluster at Azure Portal, then get the remote address of database.
Usage:

Set the data urls, database address, passwords in the front of import.py

Run python3 import.py (Please do not run with our url, or the current database will be modified)
### Publish Web Api:
Required: Windows 10, Visual Studio 2015 or higher, .Net Frame module, Azure module, neo4j module

File: Neo4jGraphApi

Usage:

Open the project sln file by visual studio(VS is the best ide to publish something to Azure). Use NuGet to install required module. Set up the neo4j database address, password in Helper/GraphDriver.cs

The main content of api is 3 cs file in Controllers

Right click the project solution, choose publish. Use you Azure account to set up it. Follow the instruction from VS, it should be very easy.

If you want to replace our api with yours, please modified the url in the main flask project.
