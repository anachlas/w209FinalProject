#!/bin/bash
y=`date -v -1d '+%Y%m%d'`
cd data
wget "http://data.gdeltproject.org/events/$y.export.CSV.zip"
unzip "$y.export.CSV.zip"
