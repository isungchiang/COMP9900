import pandas



existing = pandas.read_csv("news_sum.csv",sep="\t")
code_list = existing['code'].tolist()
title_list = existing['title'].tolist()
url_list = existing['url'].tolist()
date_list = existing['date'].tolist()
relative_list = existing['relative'].tolist()
mark_list = existing['mark'].tolist()

new_relative_list = []
fixed_date_list = []
for i in date_list:
    ymd = i.split('-')
    day = ymd[2]
    if len(day)<2:
        new_day = '0'+day
        fixed_date_list.append(ymd[0]+'-'+ymd[1]+'-'+new_day)
    else:
        fixed_date_list.append(i)

for i in relative_list:
    # print(i)
    if str(i) != 'nan':
        new_relative_list.append(i)
    else:
        new_relative_list.append('N/A')

for i in new_relative_list:
    print(i)

pandas.DataFrame({'code': code_list, 'url': url_list, 'title': title_list, 'date':fixed_date_list,
                  'relative':new_relative_list, 'mark':mark_list}).to_csv(
        './' + 'news_fixed_date'+ ".csv", index=False, sep='\t')