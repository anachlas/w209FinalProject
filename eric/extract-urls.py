#!/usr/bin/python
import csv
import json
import fileinput
import sys
reload(sys)
sys.setdefaultencoding('utf8')

events = dict()

# read csv from std-in
data = csv.reader(fileinput.input(), delimiter='\t')

for row in data:
    url = row[57]
    lat = row[39]
    lon = row[40]
    if lat != "0" and lon != "0": # filter events without geo
        events[url] = {"url":url, "lat": lat, "lon": lon}
        
#infilename = fileinput.filename()

for url in events.keys():
    print json.dumps(events[url])
