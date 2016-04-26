#!/bin/bash
y=`date --date="yesterday" --iso | sed 's/-//g'`
cd data
wget "http://data.gdeltproject.org/events/$y.export.CSV.zip"
unzip -o "$y.export.CSV.zip"
