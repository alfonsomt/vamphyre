# VAMPhyRE: Virtual Analysis Method for Phylogenomic fingeRprint Estimation
### Virtual Analysis Method for Phylogenomic fingeRprint Estimation

Repository for the VAMPhyRE Lazarus/Free pascal project

The Virtual Analysis Method for Phylogenomic fingeRprint Estimation (VAMPhyRE) is a bioinformatics technique aimed for whole-genome comparisons and phylogenomic analysis using Virtual Genomic Fingerprints (VGFs). VGFs are calculated by Virtual Hybridization (VH), which is a computational method that searches potential hybridization sites for short probes on genomic sequences.

This search locates potential hybridization sites between genome sequences and the probes in a defined set (The VAMPhyRE probe set), based on the number of complementary bases allowing a defined number of mismatches. Additionally, the program can perform a thermodynamic analysis for predicting the thermal stability of the duplexes formed between probes and potential hybridization sites, which can be used for the development of microarray devices.

The VAMPhyRE probe sets (VPS) were designed using special criteria to maximize the variability of the genomic sequences that can be analyzed and for producing specific hybridization patterns even for closely related genome sequences. The collection of potential hybridization sites in the targets constitutes a hybridization pattern called Virtual Genomic Fingerprint (VGF).

In order to produce highly specific and informative VGFs, the probe set is selected according to the length of the target genome to produce a fingerprint where is expected the hybridization of approximately 50-60% of the probes in the set, while covering most of the target genome.

Genome similarity is then estimated by pairwise comparison of their VGFs, by counting the number of shared homologous hybridization sites. VGFs similarity is reported as distance tables that can be used for calculating phylogenomic trees.

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
**-p** name of the file that contains the VPS, present in ~/VAMPhyRE/VPS/ path. You can add a file with user kmers as well. 


**-t**, # number of threads.

**-leftext**, value of left extension.

**-rightext**, value of right extension.

**-threshold**, value of threshold.

**-g**, Directory with genome files, must be in individual files in fasta format. Other formats are not allowed.


