#!/bin/bash

path=~/VAMPhyRE_test/
mac=MACOSX
linux=LINUX
OS=$(uname -s)

if [ "$OS" == "Darwin" ]; then
	
    mkdir -p $path
	
	sudo chmod +x scripts/*
	sudo mv scripts/VAMPhyRE.py /usr/local/bin/
	sudo mv scripts/prepare_contigs.py /usr/local/bin/
	sudo mv scripts/ML-VAMPhyRE.py /usr/local/bin/
	sudo mv bin_MACOSX/Treerename /usr/local/bin/
	
	mv $"bin_${mac}" bin
	sudo chmod +x bin/*
	sudo xattr -rd com.apple.quarantine bin/*
	mv bin $path
	mv VPS $path
	mv scripts $path
	mv uninstall.sh $path
	mv datasets $path

	
    rm -r *
    
    echo "VAMPhyRE was installed succesfully"
    
elif [ "$OS" == "Linux" ]; then 

	mkdir $path
	
	sudo chmod +x scripts/*
	sudo mv scripts/VAMPhyRE.py /usr/local/bin/
	sudo mv scripts/prepare_contigs.py /usr/local/bin/
	sudo mv scripts/ML-VAMPhyRE.py /usr/local/bin/
	sudo mv $"bin_${linux}/Treerename" /usr/local/bin/
	
	mv $"bin_${linux}" bin
	sudo chmod +x bin/*
	mv bin $path 
	mv VPS $path
	mv scripts $path
	mv uninstall.sh $path
	mv datasets $path

    rm -r *
    
    echo "VAMPhyRE was installed succesfully"
    
fi
