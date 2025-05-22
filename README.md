<div align="center">
<img src="Media/Logo.png" alt="Imagen" />
</div>

# VAMPhyRE: Virtual Analysis Method for Phylogenomic fingeRprint Estimation
### Virtual Analysis Method for Phylogenomic fingeRprint Estimation
Repository for the VAMPhyRE suite software distribution

<div align="justify">
The Virtual Analysis Method for Phylogenomic fingeRprint Estimation (VAMPhyRE) is a bioinformatics technique aimed for whole-genome comparisons and phylogenomic analysis using Virtual Genomic Fingerprints (VGFs). VGFs are calculated by Virtual Hybridization (VH), which is a computational method that searches potential hybridization sites for short probes on genomic sequences.

This search locates potential hybridization sites between genome sequences and the probes in a defined set (The VAMPhyRE probe set), based on the number of complementary bases allowing a defined number of mismatches. Additionally, the program can perform a thermodynamic analysis to predict the thermal stability of the duplexes formed between probes and potential hybridization sites, which can be used for the development of microarray devices.

The VAMPhyRE probe sets (VPS) were designed using special criteria to maximize the variability of the genomic sequences that can be analyzed and to produce specific hybridization patterns even for closely related genome sequences. The collection of potential hybridization sites in the targets constitutes a hybridization pattern called Virtual Genomic Fingerprint (VGF).

In order to produce highly specific and informative VGFs, the probe set is selected according to the length of the target genome to produce a fingerprint where is expected the hybridization of approximately 50-60% of the probes in the set, while covering most of the target genome.

Genome similarity is then estimated by pairwise comparison of their VGFs, by counting the number of shared homologous hybridization sites. VGFs similarity is reported as distance tables that can be used for calculating phylogenomic trees.
</div>

## Installation
### First steps
The scripts to VAMPhyRE execution are currently in Python language, so we highly recommend installing Python 3, language by Python official repository, or installing Anaconda/Miniconda; we recommend updating the following packages.
```
pip install numpy --upgrade
```
```
pip install biopython
```
```
pip install scikit-learn
```
```
pip install gensim --upgrade
```
```
pip install --upgrade bottleneck
```

### Installation of stand-alone VAMPhyRE

First, download the repository
```
git clone https://github.com/alfonsomt/vamphyre_tests.git
```

Next, execute the next commands
```
cd vamphyre_tests/
```
```
chmod +x Install_VAMPhyRE_test.sh
```
```
./Install_VAMPhyRE_test.sh
```

Now restart the terminal.

## Uninstalling VAMPhyRE

You must go to VAMPhyRE path "~/VAMPhyRE_test/" and execute the following comand:

```
~/VAMPhyRE_test/uninstall.sh
```

## Usage
### Show Help

```
VAMPhyRE.py -h
VAMPhyRE.py --help
```

### Test data

In "~/VAMPhyRE_test/" path you will find a directory called "datasets" which is used as test dataset. You can use the following commands to generate test results.

### Running VAMPhyRE optimization
```
VAMPhyRE-opt.py -p vps8 -s1 ~/VAMPhyRE/datasets/hpv/hpv1.fasta -s2 ~/VAMPhyRE/datasets/hpv/hpv2.fasta 
```
This script will create a directory with variuos files used in the optimization, the "nslog.txt" file cotain the optimization results. 

### Running VAMPhyRE
```
VAMPhyRE.py -p vps8 -t 8 -l 5 -r 5 -d 16 -g ~/VAMPhyRE/datasets/hpv

```
This script perform the VAMPhyRE metodology.

### VAMPhyRE-opt.py options
**-p** name of the file that contains the VPS, present in ~/VAMPhyRE/VPS/ path. You can add a file with user-defined kmers as well. (mandatory)

**-s1** path of genome#1 that must be used to optimization (mandatory)

**-s2** path of genome#2 that must be used to optimization (mandatory)

**-m** number of optimization mismatch (default = 1) 


### VAMPhyRE.py options
**-p** name of the file that contains the VPS, present in ~/VAMPhyRE/VPS/ path. You can add a file with user-defined kmers as well. 

**-t**, # number of threads.

**-l**, value of left extension, calculated with VAMPhyRE-opt.py

**-r**, value of right extension, calculated with VAMPhyRE-opt.py

**-d**, value of threshold, calculated with VAMPhyRE-opt.py

**-g**, Directory with genome files, must be in individual files in fasta format. Other formats are not allowed.

### Genomes with contigs
In case that your genomes contain contigs you must run the following script, before run any other script.

```
prepare_contigs.py -g Genome_dir
```
**-g** Genomes directory (default = Genomes)

**-e** Rile extension of genomes (default = fasta)
