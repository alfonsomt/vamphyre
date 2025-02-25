#!/bin/bash

path=~/VAMPhyRE_test/

sudo rm /usr/local/bin/VAMPhyRE.py
sudo rm /usr/local/bin/VAMPhyRE-opt.py
sudo rm /usr/local/bin/prepare_contigs.py
sudo rm /usr/local/bin/ML-VAMPhyRE.py
sudo rm /usr/local/bin/Treerename
sudo rm /usr/local/bin/Characters
sudo rm /usr/local/bin/Dotfinger

source ~/.bashrc  

rm -r $path
