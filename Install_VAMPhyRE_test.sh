#!/bin/bash

path=~/VAMPhyRE_test/
mac=MACOSX
linux=LINUX
# Verificar que se haya pasado un argumento valido
if [ $# -eq 0 ]; then
    echo "Error: Must use one of following options."
    echo "[${mac}|${linux}]"
    exit 1
fi

# Asignar el valor pasado como argumento a una variable
value=$1

# Tomar la decisión basada en el valor
if [ "$value" == "MACOSX" ]; then
	
    echo "${mac} selected, this option is only for MAC users."
    
    mkdir -p $path

	sudo mv scripts/VAMPhy.py /usr/local/bin/
	sudo mv scripts/prepare_contigs.py /usr/local/bin/
	sudo mv scripts/ML_analysis_CVA.py /usr/local/bin/
	sudo mv bin_MACOSX/Treerename /usr/local/bin/
	
	mv $"bin_${mac}" bin
	mv bin $path
	echo "${path}bin/*" 
	chmod +x $"${path}bin/*" 
	mv VPS $path
	chmod +x scripts/*
	mv scripts $path
	mv uninstall.sh $path
	
    rm -r *
    
elif [ "$value" == "LINUX" ]; then
    echo "${linux} selected, this option is only for any Linux distro users."
    
    mkdir -p $path

	sudo mv scripts/VAMPhy.py /usr/local/bin/
	sudo mv scripts/prepare_contigs.py /usr/local/bin/
	sudo mv scripts/ML_analysis_CVA.py /usr/local/bin/
	sudo mv bin_LINUX/Treerename /usr/local/bin/
	
	
	mv $"bin_${linux}" bin
	mv bin $path
	chmod +x $"${path}bin/*"
	mv VPS $path
	chmod +x scripts/*
	mv scripts $path
	mv uninstall.sh $path
	
    rm -r *
else
    echo "Error: only valid optios are: 'MACOSX' y 'LINUX'."
    exit 1
fi