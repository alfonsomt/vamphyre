# VAMPhyRE: Virtual Analysis Method for Phylogenomic fingeRprint Estimation
## Installation

Execute the next comands

```
chmod +x VAMPhyRE_install.sh
sudo ./VAMPhyRE_install.sh
export PATH=$HOME/bin:$PATH
```

## Uninstalling

```
sudo .~/VAMPhRE_test/uninstall.sh
```

## Usage
### Show Help

```
VAMPhy.py -h
VAMPhy.py --help
```

### Usage
```
VAMPhy.py -p vps8 -t 8 -leftext 5 -rightext 5 -threshold 16 -g example_dataset
```
options
-p name of the file that contains the VPS, present in ~/VAMPhyRE/VPS/ path. You can add a file with user kmers as well. 


-t # number of threads.

-leftext value of left extension.

-rightext value of right extension.

-threshold value of threshold.

-g Directory with genome files, must be in individual files in fasta format. Other formats are not allowed.
