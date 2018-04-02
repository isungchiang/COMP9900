import json

d = {'nodes':[],'edges':[]}
d['nodes'].append({'StockId':'AAPL','Corporation':'Apple Inc. (AAPL)','Market':'NasdaqGS - NasdaqGS Delayed Price. Currency in USD',
                   'Address':'1 Infinite Loop-Cupertino, CA 95014-United States','Contact':'tel:408-996-1010'})
d['nodes'].append({'Name':'Robert Bremner','Age':'77','Since':'2012','Position':'Independent Chairman of the Board of Trustees'})
d['nodes'].append({'Name':'Gifford Zimmerman','Age':'62','Since':'2015','Position':'Chief Administrative Officer'})
d['edges'].append({'StartId':'APPL','EndId':'21d371a8-d33a-f204-560c-13a6b0b4d52e'})
d['edges'].append({'StartId':'21d371a8-d33a-f204-560c-13a6b0b4d52e','EndId':'APPL'})
d['edges'].append({'StartId':'APPL','EndId':'5ba6d9a2-e40b-6d31-30b0-05ce2ab54569'})
d['edges'].append({'StartId':'5ba6d9a2-e40b-6d31-30b0-05ce2ab54569','EndId':'APPL'})
output = json.dumps(d)
print(output)