#!/bin/bash

path=~/VAMPhyre_test/
mkdir -p $path

sudo mv scripts/VAMPhy.py /usr/local/bin/
sudo mv scripts/prepare_contigs.py /usr/local/bin/
sudo mv scripts/ML_analysis_CVA.py /usr/local/bin/
sudo mv bin/Treerename /usr/local/bin/

mv bin $path
mv VPS $path
mv scripts $path
mv uninstall.sh $path

echo "Instalación completada en $path"

export PATH=$HOME/bin:$PATH