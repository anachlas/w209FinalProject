#!/usr/bin/python
import folium
import csv
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

infile = "../data/20160413.export.CSV"

events = []

with open(infile, 'rb') as csvfile:
     data = csv.reader(csvfile, delimiter='\t')
     for row in data:
         url = row[57]
         lat = row[39]
         lon = row[40]
         lname = row[50].encode('utf-8')
         popup = "<a target='_parent' href='" + url + "'>" + lname + "</a>"
         event = {"url": url, "lat": lat, "lon": lon, "popup": popup}
         events.append(event)

emap = folium.Map(location=[40.75007, -73.9794], zoom_start=2)
for event in events[:300]:
    print json.dumps(event)
    iframe = folium.element.IFrame(html=event["popup"], width=500, height=300)
    popup = folium.Popup(iframe, max_width=2650)
    folium.Marker([event["lat"], event["lon"]], popup=popup).add_to(emap)
emap.create_map(path="map.html")
