import pandas as pd
import numpy as np
import tensorflow as tf
import os
import spacy
import math
import requests
import json
import threading
import datetime
import pandas
import spacy

# T1GDZW9F96MTHJPK api key
header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

pv = []
nv = []
with open('positive_vocabulary.txt', 'r') as f:
    for lines in f.readlines():
        pv.append(lines.split("\n")[0])

with open('negative_vocabulary.txt', 'r') as f:
    for lines in f.readlines():
        nv.append(lines.split("\n")[0])


def action(csv, id_list):
    global  pv, nv
    print(pv, nv)
    urls = pandas.read_csv(csv, sep='\t')
    code = urls['code'][0]
    if(os.path.exists("content"+code)) :
        existing = pandas.read_csv("content"+code,sep="\t")
        code_list = existing['code'].tolist()
        title_list = existing['title'].tolist()
        url_list = existing['url'].tolist()
        date_list = existing['date'].tolist()
        content_list = existing['content'].tolist()
        listening_list = existing['listening'].tolist()
        relative_list = existing['relative'].tolist()
    new_code_list = []
    new_title_list = []
    new_url_list = []
    new_date_list = []
    new_content_list = []
    new_listening_list = []
    new_relative_list = []
    new_mark_list = []
    nlp = spacy.load('en_core_web_sm')
    pvl = []
    nvl = []

    for i in pv:
        pvl.append(nlp(i)[0])
    for i in nv:
        nvl.append(nlp(i)[0])

    i = 0
    while i < len(urls['code']):
        print('finished: ', i, 'remainning: ', len(urls['code']))
        if urls['title'][i] in new_title_list or urls['url'][i] in new_url_list:
            i+=1
            continue
        try:
            date_ = (urls['date'][i]).split(' ')
        except:
            i+=1
            continue
        if date_[0] == 'Jan':
            month = '01'
        elif date_[0] == 'Feb':
            month = '02'
        elif date_[0] == 'Mar':
            month = '03'
        elif date_[0] == 'Apr':
            month = '04'
        elif date_[0] == 'May':
            month = '05'
        elif date_[0] == 'June':
            month = '06'
        elif date_[0] == 'July':
            month = '07'
        elif date_[0] == 'Aug':
            month = '08'
        elif date_[0] == 'Sept':
            month = '09'
        elif date_[0] == 'Oct':
            month = '10'
        elif date_[0] == 'Nov':
            month = '11'
        elif date_[0] == 'Dec':
            month = '12'
        else:
            i+=1
            continue

        new_date = str(date_[2] + '-' + month + '-' + date_[1].split(',')[0])

        ymd = new_date.split('-')
        day = ymd[2]
        if len(day) < 2:
            new_day = '0' + day
            new_date = ymd[0] + '-' + ymd[1] + '-' + new_day

        content = (urls['content'][i])
        if (datetime.datetime.today() - datetime.datetime.strptime(new_date, '%Y-%m-%d')).days < 30:
            pl = 0
            nl = 0
            positive_sum = 0
            negative_sum = 0
            total_mark = 2
            for words in nlp(content):
                if (
                        words.pos_ == 'PUNCT' or words.pos_ == 'PROPN' or
                        words.pos_ == 'NUM' or words.pos_ == 'space'   or
                        words.pos_ == 'DET' or words.orth_ == '\n'     or
                        len(words.orth_) <= 2):
                    continue
                else:
                    pl = []
                    nl = []
                    for p in pvl:
                        pl.append(p.similarity(words))
                    for n in nvl:
                        nl.append(n.similarity(words))
                    positive_sum += sum(pl)
                    negative_sum += sum(nl)
            total = positive_sum + negative_sum

            if pl >= nl:
                final_mark = (positive_sum/total)**2 * 1
            else:
                final_mark = (negative_sum/total)**2 * 1 * (-1)
            print(final_mark, new_date)
        else:
            final_mark = 0

        new_relative = ''
        # print(urls['relative'][i])
        if str(urls['relative'][i]) == 'nan':
            new_relative = 'N/A'
        else:
            current_relative = (urls['relative'][i]).split(',')
            for re in current_relative[:-1]:
                if re in id_list:
                    new_relative += re + ','
            if new_relative == '':
                new_relative = 'N/A'


        new_code_list.append(urls['code'][i])
        new_title_list.append(urls['title'][i])
        new_url_list.append(urls['url'][i])
        new_date_list.append(new_date)
        # new_content_list.append(urls['content'][i])
        new_listening_list.append(urls['listening'][i])
        new_relative_list.append(new_relative)
        new_mark_list.append(final_mark)

        i += 1

    pandas.DataFrame(
        {'code': new_code_list, 'url': new_url_list, 'title': new_title_list, 'date': new_date_list,
         'relative': new_relative_list, 'mark':new_mark_list}).to_csv(
        './' + 'marked_' + code + ".csv", index=False, sep='\t')


def del_content_and_fileter_relative(csv, id_list):
    urls = pandas.read_csv(csv, sep='\t')
    code = urls['code'][0]
    if(os.path.exists(csv)) :
        existing = pandas.read_csv(csv,sep="\t")
        code_list = existing['code'].tolist()
        title_list = existing['title'].tolist()
        url_list = existing['url'].tolist()
        date_list = existing['date'].tolist()
        content_list = existing['content'].tolist()
        listening_list = existing['listening'].tolist()
        relative_list = existing['relative'].tolist()
        mark_list = existing['mark'].tolist()
    new_code_list = []
    new_title_list = []
    new_url_list = []
    new_date_list = []
    new_content_list = []
    new_listening_list = []
    new_relative_list = []
    new_mark_list = []

    i = 0
    while i < len(urls['code']):
        if urls['title'][i] in new_title_list or urls['url'][i] in new_url_list:
            i += 1
            continue
        try:
            date_ = (urls['date'][i]).split(' ')
        except:
            i += 1
            continue
        if date_[0] == 'Jan':
            month = '01'
        elif date_[0] == 'Feb':
            month = '02'
        elif date_[0] == 'Mar':
            month = '03'
        elif date_[0] == 'Apr':
            month = '04'
        elif date_[0] == 'May':
            month = '05'
        elif date_[0] == 'June':
            month = '06'
        elif date_[0] == 'July':
            month = '07'
        elif date_[0] == 'Aug':
            month = '08'
        elif date_[0] == 'Sept':
            month = '09'
        elif date_[0] == 'Oct':
            month = '10'
        elif date_[0] == 'Nov':
            month = '11'
        elif date_[0] == 'Dec':
            month = '12'
        else:
            i += 1
            continue

        new_date = str(date_[2] + '-' + month + '-' + date_[1].split(',')[0])

        new_relative = ''
        # print(urls['relative'][i])
        if str(urls['relative'][i]) == 'nan':
            new_relative = 'N/A'
        else:
            current_relative = (urls['relative'][i]).split(',')
            for re in current_relative[:-1]:
                if re in id_list:
                    new_relative += re+','
            if new_relative == '':
                new_relative = 'N/A'

        print(new_relative)

        new_code_list.append(urls['code'][i])
        new_title_list.append(urls['title'][i])
        new_url_list.append(urls['url'][i])
        new_date_list.append(new_date)
        new_listening_list.append(urls['listening'][i])
        new_relative_list.append(new_relative)
        new_mark_list.append(urls['mark'][i])

        i += 1

    pandas.DataFrame(
        {'code': new_code_list, 'url': new_url_list, 'title': new_title_list, 'date': new_date_list,
         'relative': new_relative_list, 'mark': new_mark_list}).to_csv(
        './' + 'marked_no_content_' + code + ".csv", index=False, sep='\t')
    print(code+' finished')



id_list = []
with open('US_codes.txt', 'r') as f:
    for codes in f.readlines():
        codes = codes.replace('\n', '')
        id_list.append(codes)

for csvs in os.listdir('./'):
    if 'content_' in csvs and '.csv' in csvs:
        print(csvs)
        action(csvs, id_list)
    # if 'marked_' in csvs and '.csv' in csvs and '_no_content' not in csvs:
    #     filename = csvs.replace('marked_', '')
    #     filename = filename.replace('.csv', '')

        # if 'marked_'+filename+'.csv' in os.listdir('./'):
        #     print(filename+' checked!')
        #     continue
        # del_content_and_fileter_relative('./'+csvs, id_list)