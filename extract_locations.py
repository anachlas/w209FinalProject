#!/usr/bin/python
import json
import datetime
import numpy as np

yesterday = datetime.date.fromordinal(datetime.date.today().toordinal()-1)
filename = yesterday.strftime('data/%Y%m%d.export.CSV')

f = open(filename)

locations = {}

print 'processing CSV'
for l in f:
	data = l.split('\t')
	loc = data[15][:3]
	url = data[57].strip()
	if len(loc) !=3:
		continue
	if loc in locations.keys():
		count = locations[loc][0]+1
		v = locations[loc][1]
		locations[loc] = [count,v]
	else:
		locations[loc] = [1,url]

loc_list = []
for l in locations.keys():
	loc_list.append([l,np.log(locations[l][0]),locations[l][1]])


print 'writing JSON'
with open(yesterday.strftime('location_json/%Y%m%d.locations.json'), 'w') as fp:
    json.dump(loc_list, fp)

print 'finished'
