#!/bin/bash
# Yesterday's data posts by 6am EST every day.
datestring=`date --date="yesterday" --iso | sed 's/-//g'`
csvfilename="data/$datestring.export.CSV"

# Grab data
echo "Downloading yesterday's data...................."
wget -P data "http://data.gdeltproject.org/events/$datestring.export.CSV.zip"
echo "Unzipping......................"
unzip -d data "data/$datestring.export.CSV.zip"

# Extract urls and lat/lon from data
echo "Extracting urls and latlon......................"
urlsjsonfile=data/$datestring.urlsAndLatLon.json
echo "$csvfilename to $urlsjsonfile"
cat $csvfilename | ./extract-urls.py > $urlsjsonfile

# Fetch content from web
echo "Splitting $urlsjsonfile.............."
split -l 1000 $urlsjsonfile --additional-suffix=.json data/$datestring.urlsAndLatLon.split.
echo "Downloading content from web................"
parallel -P 10 ./grab-content.py ::: data/$datestring.urlsAndLatLon.split.*

# Extract entities
echo "Extracting Entities.................."
parallel -P 7 ./extract-entities.py ::: data/$datestring.urlsAndLatLon.split.withText.*
cat data/$datestring.urlsAndLatLon.entities* > data/$datestring.allents.json
