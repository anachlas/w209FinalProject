# w209FinalProject
Final Project for w209 Spring 2016


## GDELT Docs

[Data Format Codebook](http://data.gdeltproject.org/documentation/GDELT-Data_Format_Codebook.pdf)


## Instructions to Setup

  Copy Repo to computer
  Run grab\_yesterdays\_data.sh - This will download about 10mb zip of GDELT event data and extract to raw file (~100mb)
  Run extract_locations.py - This will scan over the raw CSV file and extract data for the map viz and save as JSON
  Setup a webserver in the main folder /w209FinalProject/ and use it to open index.html

