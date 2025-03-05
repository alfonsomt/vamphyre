#!/bin/bash
path=~/VAMPhyRE/
OS=$(uname -s)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'
PROGRAM_NAME="VAMPhyRE"

if [ "$OS" == "Darwin" ]; then
	
    mkdir -p $path
	
	sudo chmod +x scripts/*
	sudo mv scripts/VAMPhyRE.py /usr/local/bin/
	sudo mv scripts/prepare_contigs.py /usr/local/bin/
	sudo mv scripts/ML-VAMPhyRE.py /usr/local/bin/
	sudo mv scripts/VAMPhyRE-opt.py /usr/local/bin/
	
	mv bin_MACOSX bin
	sudo chmod +x bin/*
	sudo xattr -rd com.apple.quarantine bin/*
	sudo mv bin/Treerename /usr/local/bin/
	sudo mv bin/Characters /usr/local/bin/
	sudo mv bin/Dotfinger /usr/local/bin/
	mv bin $path
	mv VPS $path
	mv scripts $path
	mv uninstall.sh $path
	mv datasets $path
	source ~/.bash* 

    rm -r *
    
    print_box() {
    local text="$1"
    local color="$2"
    local length=${#text}
    local border=$(printf '%0.s═' $(seq 1 $((length + 4))))

    echo -e "${color}╔${border}╗${NC}"
    echo -e "${color}║  ${text}  ║${NC}"
    echo -e "${color}╚${border}╝${NC}"
	}
	echo "########################################################################################"
	print_box "VAMPhyRE Installer" "${CYAN}"
	echo -e "${GREEN}Thank you for installing ${YELLOW}VAMPhyRE${GREEN}!${NC}"
	echo ""
	echo -e "${MAGENTA}Remember to install biopython, by using 'pip install biopython'${NC}"
	echo ""
	echo -e "${GREEN}The following tools were installer as well"
	echo -e "${CYAN}  - Dotfinger - Tool to compare genome fingerprints"
	echo -e "${CYAN}  - Characters - Tool to make distance matrix from frequency matrix"
	echo -e "${CYAN}  - Treerename - Tool to change names of nwk files"
	echo -e "${CYAN}  - VAMPhyRE.py - Main VAMPhyRE script"
    echo -e "${CYAN}  - VAMPhyRE-opt.py - Optimization script for VAMPhyRE"
    echo -e "${CYAN}  - prepare-contigs.py - Processing tool for contigs genomes"
    echo -e "${CYAN}  - ML-VAMPhyRE.py - Supervised Machine Learnig script"

	echo -e "${NC}########################################################################################"
    
elif [ "$OS" == "Linux" ]; then 

	mkdir $path
	
	sudo chmod +x scripts/*
	sudo mv scripts/VAMPhyRE.py /usr/local/bin/
	sudo mv scripts/prepare_contigs.py /usr/local/bin/
	sudo mv scripts/ML-VAMPhyRE.py /usr/local/bin/
	sudo mv scripts/VAMPhyRE-opt.py /usr/local/bin/
	
	mv bin_LINUX bin
	sudo chmod +x bin/*
	sudo mv bin/Treerename /usr/local/bin/
	sudo mv bin/Characters /usr/local/bin/
	sudo mv bin/Dotfinger /usr/local/bin/
	mv bin $path 
	mv VPS $path
	mv scripts $path
	mv uninstall.sh $path
	mv datasets $path
	source ~/.bash* 

    rm -r *
    
    print_box() {
    local text="$1"
    local color="$2"
    local length=${#text}
    local border=$(printf '%0.s═' $(seq 1 $((length + 4))))

    echo -e "${color}╔${border}╗${NC}"
    echo -e "${color}║  ${text}  ║${NC}"
    echo -e "${color}╚${border}╝${NC}"
	}
	echo "########################################################################################"
	print_box "VAMPhyRE Installer" "${CYAN}"
	echo -e "${GREEN}Thank you for installing ${YELLOW}VAMPhyRE${GREEN}!${NC}"
	echo ""
	echo -e "${MAGENTA}Remember to install biopython, by using 'pip install biopython'${NC}"
	echo ""
	echo -e "${GREEN}The following tools were installer as well"
	echo -e "${CYAN}  - Dotfinger - Tool to compare genome fingerprints"
	echo -e "${CYAN}  - Characters - Tool to make distance matrix from frequency matrix"
	echo -e "${CYAN}  - Treerename - Tool to change names of nwk files"
	echo -e "${CYAN}  - VAMPhyRE.py - Main VAMPhyRE script"
    echo -e "${CYAN}  - VAMPhyRE-opt.py - Optimization script for VAMPhyRE"
    echo -e "${CYAN}  - prepare-contigs.py - Processing tool for contigs genomes"
    echo -e "${CYAN}  - ML-VAMPhyRE.py - Supervised Machine Learnig script"
	echo -e "${NC}########################################################################################"
    
fi
