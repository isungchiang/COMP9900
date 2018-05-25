import os
import pandas as pd
import numpy as np
import json
import requests

file_list = []
def merge_news():
	for i in os.listdir('./'):
		if 'marked_' in i and '.csv' in i:
			file_list.append(i)

	# for i in code_list:
	#     csv = str(i).replace('URL', 'content_')
	#     csv = csv.replace('\n', '')
	#     if not len(csv):
	#         break
	#     csv = './marketwatch_content/'+csv
	#     with open(csv, 'r') as f:
	#         print(csv)
	#         for j in f.readlines()[0:1]:
	#             print(j)
	#         f.close()
	#
	print(file_list)

	sum_ = []
	# for csv in file_list:
	#     csv_ = 'marketwatch_content/'+csv+'.csv'
	#     print(csv_)
	#     ind = pd.read_csv(csv_)
	#     ind_ = np.array(ind)
	#     np.append(sum_, ind_[1:])
	#     col = ind.columns
	for csv in file_list:
		csv_ = csv
		# csv_ = 'marketwatch_content/' + csv + '.csv'
		with open(csv_, 'r') as f:
			content = f.readlines()
			columns = content[0]
			for i in content[1:]:
				sum_.append(i)
			f.close()

	with open('news_sum.csv', 'w') as f:
		f.writelines(['code\tdate\tmark\trelative\ttitle\turl\n'])
		f.writelines(sum_)
		f.close()

def merge_marks():
	code_list = []
	json_list = []

	for json_file in os.listdir('./'):
		if '.json' not in json_file:
			continue
		with open('./'+json_file, 'r') as f:
			code_list.append(json_file.replace('.json', ''))
			json_list.append(json.loads(f.readline()))
			f.close()
	pd.DataFrame(
		{'code': code_list, 'json': json_list}).to_csv(
		'./' + 'merged_json' + '.csv', index=False, sep='\t')


def read_jsons():
	jsons = pd.read_csv('./merged_json.csv', sep='\t')
	for json_ in jsons['json']:
		line = str(json_).replace('\'', '\"')
		line = line.replace('None', 'null')
		print(line)

		print(json.loads( line ) )

merge_news()
# merge_marks()
