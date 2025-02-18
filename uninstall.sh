#!/bin/bash

path=~/VAMPhyre_test/

sudo rm /usr/local/bin/VAMPhy.py
sudo rm /usr/local/bin/prepare_contigs.py
sudo mv /usr/local/bin/ML_analysis_CVA.py
sudo mv /usr/local/bin/Treerename

rm -r $path