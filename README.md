# VAMPhyRE: Virtual Analysis Method for Phylogenomic fingeRprint Estimation
### Virtual Analysis Method for Phylogenomic fingeRprint Estimation

Repository for the VAMPhyRE Lazarus/Free pascal project

The Virtual Analysis Method for Phylogenomic fingeRprint Estimation (VAMPhyRE) is a bioinformatics technique aimed for whole-genome comparisons and phylogenomic analysis using Virtual Genomic Fingerprints (VGFs). VGFs are calculated by Virtual Hybridization (VH), which is a computational method that searches potential hybridization sites for short probes on genomic sequences.

This search locates potential hybridization sites between genome sequences and the probes in a defined set (The VAMPhyRE probe set), based on the number of complementary bases allowing a defined number of mismatches. Additionally, the program can perform a thermodynamic analysis for predicting the thermal stability of the duplexes formed between probes and potential hybridization sites, which can be used for the development of microarray devices.

The VAMPhyRE probe sets (VPS) were designed using special criteria to maximize the variability of the genomic sequences that can be analyzed and for producing specific hybridization patterns even for closely related genome sequences. The collection of potential hybridization sites in the targets constitutes a hybridization pattern called Virtual Genomic Fingerprint (VGF).

In order to produce highly specific and informative VGFs, the probe set is selected according to the length of the target genome to produce a fingerprint where is expected the hybridization of approximately 50-60% of the probes in the set, while covering most of the target genome.

Genome similarity is then estimated by pairwise comparison of their VGFs, by counting the number of shared homologous hybridization sites. VGFs similarity is reported as distance tables that can be used for calculating phylogenomic trees.

## Installation

First, download the repository
```
git clone https://github.com/alfonsomt/vamphyre_tests.git
```


Execute the next comands
```
cd vamphyre_test/
chmod +x Install_VAMPhyRE_test.sh
```
You will need to select LINUX or MACOSX option, depending on your operative system
```
sudo ./Install_VAMPhyRE_test.sh [LINUX|MACOSX]
export PATH=$HOME/bin:$PATH
```

## Uninstalling

You must go to VAMPhyRE path "~/VAMPhyRE_test/" and execute the following comand:

```
sudo ./uninstall.sh
```

## Usage
### Show Help

```
VAMPhy.py -h
VAMPhy.py --help
```

### Usage
```
VAMPhy.py -p vps8 -t 8 -l 5 -r 5 -d 16 -g genome_dir
```
options
**-p** name of the file that contains the VPS, present in ~/VAMPhyRE/VPS/ path. You can add a file with user kmers as well. 

**-t**, # number of threads.

**-l**, value of left extension.

**-r**, value of right extension.

**-d**, value of threshold.

**-g**, Directory with genome files, must be in individual files in fasta format. Other formats are not allowed.


