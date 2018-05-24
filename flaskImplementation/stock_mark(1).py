import requests
import json
import datetime
import threading
import time

# T1GDZW9F96MTHJPK api key
header={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

class MyThread(threading.Thread):
	def __init__(self, target, args, name=''):
		threading.Thread.__init__(self)
		self.name = name
		self.target = target
		self.args = args
		self.result = self.target(*self.args)

	def get_result(self):
		try:
			return self.result
		except:
			return None


# return total mark, labels, rsi json, willr json, dailyprice json.
def stock_mark(stockid, date_=datetime.date.today(), sensitivity='normal'):
	# rsi, bolling, will%r, news?
	SEVEN_DAYS = 7
	FIFTEEN_DAYS = 15
	MONTHLY = 30


	if sensitivity == 'strong':
		period = SEVEN_DAYS
	elif sensitivity == 'normal':
		period = FIFTEEN_DAYS
	elif sensitivity == 'soft':
		period = MONTHLY

	stockid = stockid.upper()

	threads = []
	daily_price_thread = MyThread(target=get_time_series, args=(stockid,))
	rsi_thread         = MyThread(target=get_rsi, args=(stockid,period))
	willr_thread       = MyThread(target=get_willr, args=(stockid,period))
	bolling_thread     = MyThread(target=get_boll, args=(stockid,period))
	threads.append(daily_price_thread)
	threads.append(rsi_thread)
	threads.append(willr_thread)
	threads.append(bolling_thread)

	for i in threads:
		i.start()
	all_live = True
	while all_live:
		all_live = False
		for i in threads:
			if i.is_alive():
				all_live = True
				time.sleep(0.01)
				break

	daily_price = daily_price_thread.get_result()
	rsi = rsi_thread.get_result()
	willr = willr_thread.get_result()
	bolling = bolling_thread.get_result()

	# daily_price = get_time_series(stockid)
	# rsi = get_rsi(stockid, period)
	# willr = get_willr(stockid, period)
	# bolling = get_boll(stockid, period)

	date_series = []

	# 1: up, 0: down
	result_labels = {'rsi':{}, 'rsi_band':{}, 'bolling':{}, 'bolling_bands':{}, 'willr':{}}

	for i in range(0,20):
		date = str(date_ - datetime.timedelta(days=i))
		date_series.append(date)


	rsi_mark     = 0.0
	willr_mark   = 0.0
	bolling_mark = 0.0

	temp_ = []

	i = 0
	for dates in date_series:
		print(dates)
		if dates not in daily_price["Time Series (Daily)"] or dates not in rsi["Technical Analysis: RSI"]:
			continue
		i += 1
		if i > 3:
			break
		temp_.append(dates)

	# latest date_1
	date_1 = temp_[0]
	date_2 = temp_[1]
	date_3 = temp_[2]
	# print(date_1)

	# daily_price_ = abs(float(daily_price["Time Series (Daily)"][dates]["1. open"]) + float(
	#		daily_price["Time Series (Daily)"][date]["4. close"])) / 2.0

#############################
	# rsi buy
	if (float(rsi["Technical Analysis: RSI"][date_1]['RSI']) >
			float(rsi["Technical Analysis: RSI"][date_2]['RSI']) and
			float(rsi["Technical Analysis: RSI"][date_2]['RSI']) >
			float(rsi["Technical Analysis: RSI"][date_3]['RSI']) and
			float(rsi["Technical Analysis: RSI"][date_1]['RSI']) < 80 and
			float(rsi["Technical Analysis: RSI"][date_3]['RSI']) > 40):
		rsi_mark += 1.6
		result_labels['rsi']['content'] = 'RSI is increasing'
		result_labels['rsi']['labels'] = 1
	elif (float(rsi["Technical Analysis: RSI"][date_1]['RSI']) >
		  float(rsi["Technical Analysis: RSI"][date_2]['RSI']) and
		  float(rsi["Technical Analysis: RSI"][date_2]['RSI']) >
		  float(rsi["Technical Analysis: RSI"][date_3]['RSI']) and
		(float(rsi["Technical Analysis: RSI"][date_1]['RSI']) < 80 or
		 float(rsi["Technical Analysis: RSI"][date_3]['RSI']) > 40)):
		rsi_mark += 1.0
		result_labels['rsi']['content'] = 'RSI is increasing'
		result_labels['rsi']['labels'] = 1

	elif (float(rsi["Technical Analysis: RSI"][date_1]['RSI']) >
		  float(rsi["Technical Analysis: RSI"][date_2]['RSI']) and
		  float(rsi["Technical Analysis: RSI"][date_2]['RSI']) >
		  float(rsi["Technical Analysis: RSI"][date_3]['RSI']) ):
		rsi_mark += 0.6
		result_labels['rsi']['content'] = 'RSI is increasing'
		result_labels['rsi']['labels'] = 1

	if float(rsi["Technical Analysis: RSI"][date_1]['RSI']) < 5:
		rsi_mark += 0.8
		result_labels['rsi_bands']['content'] = 'RSI is at bottom'
		result_labels['rsi_bands']['labels'] = 1
	elif float(rsi["Technical Analysis: RSI"][date_1]['RSI']) < 10:
		rsi_mark += 0.4
		result_labels['rsi_bands']['content'] = 'RSI is at bottom'
		result_labels['rsi_bands']['labels'] = 1
	elif float(rsi["Technical Analysis: RSI"][date_1]['RSI']) < 15:
		rsi_mark += 0.2
		result_labels['rsi_bands']['content'] = 'RSI is at bottom'
		result_labels['rsi_bands']['labels'] = 1

	# rsi sell
	if (float(rsi["Technical Analysis: RSI"][date_1]['RSI']) <
		float(rsi["Technical Analysis: RSI"][date_2]['RSI']) and
		float(rsi["Technical Analysis: RSI"][date_2]['RSI']) <
		float(rsi["Technical Analysis: RSI"][date_3]['RSI']) and
		float(rsi["Technical Analysis: RSI"][date_1]['RSI']) > 60 and
		float(rsi["Technical Analysis: RSI"][date_3]['RSI']) < 80):
		rsi_mark -= 1.6
		result_labels['rsi']['content'] = 'RSI is decreasing'
		result_labels['rsi']['labels'] = 0

	elif (float(rsi["Technical Analysis: RSI"][date_1]['RSI']) <
		  float(rsi["Technical Analysis: RSI"][date_2]['RSI']) and
		  float(rsi["Technical Analysis: RSI"][date_2]['RSI']) <
		  float(rsi["Technical Analysis: RSI"][date_3]['RSI']) and
		(float(rsi["Technical Analysis: RSI"][date_1]['RSI']) > 60 or
		 float(rsi["Technical Analysis: RSI"][date_3]['RSI']) < 80)):
		rsi_mark -= 1.0
		result_labels['rsi']['content'] = 'RSI is decreasing'
		result_labels['rsi']['labels'] = 0

	elif (float(rsi["Technical Analysis: RSI"][date_1]['RSI']) <
		  float(rsi["Technical Analysis: RSI"][date_2]['RSI']) and
		  float(rsi["Technical Analysis: RSI"][date_2]['RSI']) <
		  float(rsi["Technical Analysis: RSI"][date_3]['RSI']) ):
		rsi_mark -= 0.6
		result_labels['rsi']['content'] = 'RSI is decreasing'
		result_labels['rsi']['labels'] = 0

	if float(rsi["Technical Analysis: RSI"][date_1]['RSI']) > 85:
		rsi_mark -= 0.2
		result_labels['rsi_bands']['content'] = 'RSI is at top'
		result_labels['rsi_bands']['labels'] = 0
	elif float(rsi["Technical Analysis: RSI"][date_1]['RSI']) > 90:
		rsi_mark -= 0.4
		result_labels['rsi_bands']['content'] = 'RSI is at top'
		result_labels['rsi_bands']['labels'] = 0
	elif float(rsi["Technical Analysis: RSI"][date_1]['RSI']) > 95:
		rsi_mark -= 0.8
		result_labels['rsi_bands']['content'] = 'RSI is at top'
		result_labels['rsi_bands']['labels'] = 0

	# print('rsi mark: ', rsi_mark)

#############################
	# bolling
	date_1_bolling = bolling['Technical Analysis: BBANDS'][date_1]
	date_2_bolling = bolling['Technical Analysis: BBANDS'][date_2]
	date_3_bolling = bolling['Technical Analysis: BBANDS'][date_3]

	date_1_price = abs(float(daily_price["Time Series (Daily)"][date_1]["1. open"]) + float(
			daily_price["Time Series (Daily)"][date_1]["4. close"])) / 2.0
	date_2_price = abs(float(daily_price["Time Series (Daily)"][date_2]["1. open"]) + float(
		daily_price["Time Series (Daily)"][date_2]["4. close"])) / 2.0
	date_3_price = abs(float(daily_price["Time Series (Daily)"][date_3]["1. open"]) + float(
		daily_price["Time Series (Daily)"][date_3]["4. close"])) / 2.0

	# upper tunnel
	if(float(date_1_bolling['Real Upper Band']) >=
			float(date_2_bolling['Real Upper Band']) and
			float(date_2_bolling['Real Upper Band']) >=
			float(date_3_bolling['Real Upper Band']) and
			float(date_1_bolling['Real Middle Band']) >=
			float(date_2_bolling['Real Middle Band']) and
			float(date_2_bolling['Real Middle Band']) >=
			float(date_3_bolling['Real Middle Band']) and
			float(date_1_bolling['Real Lower Band']) >=
			float(date_2_bolling['Real Lower Band']) and
			float(date_2_bolling['Real Lower Band']) >=
			float(date_3_bolling['Real Lower Band'])):
		result_labels['bolling_bands']['content'] = 'at raising tunnel!'
		result_labels['bolling_bands']['labels']  = 1
		bolling_mark += 2.0

	# lower tunnel
	if (float(date_1_bolling['Real Upper Band']) <=
			float(date_2_bolling['Real Upper Band']) and
			float(date_2_bolling['Real Upper Band']) <=
			float(date_3_bolling['Real Upper Band']) and
			float(date_1_bolling['Real Middle Band']) <=
			float(date_2_bolling['Real Middle Band']) and
			float(date_2_bolling['Real Middle Band']) <=
			float(date_3_bolling['Real Middle Band']) and
			float(date_1_bolling['Real Lower Band']) <=
			float(date_2_bolling['Real Lower Band']) and
			float(date_2_bolling['Real Lower Band']) <=
			float(date_3_bolling['Real Lower Band'])):
		result_labels['bolling_bands']['content'] = 'at decling tunnel!'
		result_labels['bolling_bands']['labels']  = 0
		bolling_mark -= 2.0


	# > upper band
	if date_1_price >= float(date_1_bolling['Real Upper Band']):
		bolling_mark -= 0.4
	if date_2_price >= float(date_2_bolling['Real Upper Band']):
		bolling_mark -= 0.2
	if date_3_price >= float(date_3_bolling['Real Upper Band']):
		bolling_mark -= 0.2

	to_upper = abs(date_1_price - float(date_1_bolling['Real Upper Band']))
	to_middle = abs(date_1_price - float(date_1_bolling['Real Middle Band']))
	to_lower = abs(date_1_price - float(date_1_bolling['Real Lower Band']))

	# > middle band & < upper band
	if(date_1_price < float(date_1_bolling['Real Upper Band']) and
		date_1_price > float(date_1_bolling['Real Upper Band'])):
		# close to middle band
		if to_middle <= to_upper:
			if (to_middle)/(to_upper+to_middle) <= 0.1:
				bolling_mark += 0.6
				result_labels['bolling']['content'] = 'close to middle brand'
				result_labels['bolling']['labels'] = 1
			elif (to_middle)/(to_upper+to_middle) <= 0.2:
				bolling_mark += 0.4
				result_labels['bolling']['content'] = 'close to middle brand'
				result_labels['bolling']['labels'] = 1
			else :
				bolling_mark += 0.2


		# close to upper band
		elif to_middle > to_upper:
			if (to_upper) / (to_upper + to_middle) <= 0.1:
				bolling_mark -= 0.6
				result_labels['bolling']['content'] = 'close to upper brand'
				result_labels['bolling']['labels'] = 0
			elif (to_upper) / (to_upper + to_middle) <= 0.2:
				bolling_mark -= 0.4
				result_labels['bolling']['content'] = 'close to upper brand'
				result_labels['bolling']['labels'] = 0


	# > lower band & < middle band
	elif (date_1_price < float(date_1_bolling['Real Middle Band']) and
			date_1_price > float(date_1_bolling['Real Lower Band'])):
		# close to middle band
		if to_middle <= to_lower:
			if (to_middle) / (to_lower + to_middle) <= 0.1:
				bolling_mark += 0.4
				result_labels['bolling']['content'] = 'close to middle brand'
				result_labels['bolling']['labels'] = 1

		# close to lower band
		elif to_middle > to_lower:
			if (to_lower) / (to_lower + to_middle) <= 0.1:
				bolling_mark -= 0.6
				result_labels['bolling']['content'] = 'close to lower brand'
				result_labels['bolling']['labels'] = 0
			elif (to_lower) / (to_lower + to_middle) <= 0.2:
				bolling_mark -= 0.4
				result_labels['bolling']['content'] = 'close to lower brand'
				result_labels['bolling']['labels'] = 0

	# < lower band
	if date_1_price <= float(date_1_bolling['Real Lower Band']):
		bolling_mark -= 0.4
	if date_2_price <= float(date_2_bolling['Real Lower Band']):
		bolling_mark -= 0.2
	if date_3_price <= float(date_3_bolling['Real Lower Band']):
		bolling_mark += 0.2

	# print('bolling mark: ', bolling_mark)

#############################
	# will%r sell
	if abs(float(willr['Technical Analysis: WILLR'][date_1]['WILLR'])) >= 90:
		willr_mark -= 1.2
		result_labels['willr']['content'] = 'WILL%R close to top'
		result_labels['willr']['labels'] = 0
	elif abs(float(willr['Technical Analysis: WILLR'][date_1]['WILLR'])) >= 85:
		willr_mark -= 0.8
		result_labels['willr']['content'] = 'WILL%R close to top'
		result_labels['willr']['labels'] = 0
	elif abs(float(willr['Technical Analysis: WILLR'][date_1]['WILLR'])) >= 80:
		willr_mark -= 0.4

	# will%r buy
	if abs(float(willr['Technical Analysis: WILLR'][date_1]['WILLR'])) <= 20:
		willr_mark += 0.2
	elif abs(float(willr['Technical Analysis: WILLR'][date_1]['WILLR'])) <= 15:
		willr_mark += 0.4
		result_labels['willr']['content'] = 'WILL%R close to bottom'
		result_labels['willr']['labels'] = 1
	elif abs(float(willr['Technical Analysis: WILLR'][date_1]['WILLR'])) <= 10:
		willr_mark += 0.8
		result_labels['willr']['content'] = 'WILL%R close to bottom'
		result_labels['willr']['labels'] = 1

	# print('will%r mark: ', willr_mark)
	# print(result_labels)
	daily_price_ = abs(float(daily_price["Time Series (Daily)"][date_1]["1. open"]) + float(
			daily_price["Time Series (Daily)"][date_1]["4. close"])) / 2.0
	daily_price__ = abs(float(daily_price["Time Series (Daily)"][date_2]["1. open"]) + float(
			daily_price["Time Series (Daily)"][date_2]["4. close"])) / 2.0
	# print((daily_price_-daily_price__), (daily_price_-daily_price__)/daily_price__)
	result_labels_ = {}
	for i in result_labels:
		if result_labels[i]:
			result_labels_[i] = result_labels[i]
	# print(result_labels)
	print(5.0+rsi_mark+bolling_mark+willr_mark)
	print(result_labels_)
	return 5.0+rsi_mark+bolling_mark+willr_mark, json.dumps(result_labels_), (rsi), json.dumps(willr), json.dumps(daily_price)

def get_time_series(CODE):
	time_series_url="https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+CODE+"&outputsize=compact&apikey=T1GDZW9F96MTHJPK"
	r=requests.get(time_series_url,headers=header)
	time_series=json.loads(r.content.decode('utf-8'))
	return time_series

# RSI
def get_rsi(CODE, TIME_PERIOD):
	rsi_url = "https://www.alphavantage.co/query?function=RSI&symbol="+CODE+"&interval=daily&time_period="+str(TIME_PERIOD)+"&series_type=close&apikey=T1GDZW9F96MTHJPK"
	r=requests.get(rsi_url,headers=header)
	rsi=json.loads(r.content.decode('utf-8'))
	return rsi

# WILL%R
def get_willr(CODE, TIME_PERIOD):
	willr_url = "https://www.alphavantage.co/query?function=WILLR&symbol="+CODE+"&inzterval=daily&time_period="+str(TIME_PERIOD)+"&apikey=T1GDZW9F96MTHJPK"
	r=requests.get(willr_url,headers=header)
	willr=json.loads(r.content.decode('utf-8'))
	return willr

# BOLLING
def get_boll(CODE, TIME_PERIOD):
	boll_url = "https://www.alphavantage.co/query?function=BBANDS&symbol="+CODE+"&interval=daily&time_period="+str(TIME_PERIOD)+"&series_type=close&nbdevup=3&nbdevdn=3&apikey=T1GDZW9F96MTHJPK"
	r=requests.get(boll_url,headers=header)
	boll=json.loads(r.content.decode('utf-8'))
	return boll


stock_mark('MSFT')