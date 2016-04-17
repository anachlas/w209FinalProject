#!/bin/bash
wget -P data "https://github.com/mit-nlp/MITIE/releases/download/v0.4/MITIE-models-v0.2.tar.bz2"
cd data
bunzip2 MITIE-models-v0.2.tar.bz2
tar -xf MITIE-models-v0.2.tar
