<div align="center">
<img src="Media/Logo_final.png" alt="Imagen" />
</div>

# VAMPhyRE: Virtual Analysis Method for Phylogenomic fingeRprint Estimation
### Virtual Analysis Method for Phylogenomic fingeRprint Estimation

Repository for the VAMPhyRE Lazarus/Free pascal project

<div align="justify">
The Virtual Analysis Method for Phylogenomic fingeRprint Estimation (VAMPhyRE) is a bioinformatics technique aimed for whole-genome comparisons and phylogenomic analysis using Virtual Genomic Fingerprints (VGFs). VGFs are calculated by Virtual Hybridization (VH), which is a computational method that searches potential hybridization sites for short probes on genomic sequences.


This search locates potential hybridization sites between genome sequences and the probes in a defined set (The VAMPhyRE probe set), based on the number of complementary bases allowing a defined number of mismatches. Additionally, the program can perform a thermodynamic analysis for predicting the thermal stability of the duplexes formed between probes and potential hybridization sites, which can be used for the development of microarray devices.

The VAMPhyRE probe sets (VPS) were designed using special criteria to maximize the variability of the genomic sequences that can be analyzed and for producing specific hybridization patterns even for closely related genome sequences. The collection of potential hybridization sites in the targets constitutes a hybridization pattern called Virtual Genomic Fingerprint (VGF).

In order to produce highly specific and informative VGFs, the probe set is selected according to the length of the target genome to produce a fingerprint where is expected the hybridization of approximately 50-60% of the probes in the set, while covering most of the target genome.

Genome similarity is then estimated by pairwise comparison of their VGFs, by counting the number of shared homologous hybridization sites. VGFs similarity is reported as distance tables that can be used for calculating phylogenomic trees.
</div>

## What is VAMPhyRE?

The Virtual Analysis Method for Phylogenomic fingeRprint Estimation (VAMPhyRE) is a bioinformatics technique aimed for whole-genome comparisons and phylogenomic analysis using Virtual Genomic Fingerprints (VGFs). VGFs are calculated by Virtual Hybridization (VH), which is a computational method that searches potential hybridization sites for short probes on genomic sequences. The collection of potential hybridization sites in a target genome constitutes a hybridization pattern called Virtual Genomic Fingerprint (VGF).

VGFs can be used to estimate genome similarity between pairs of genomes. Pairwise genome distances are calculated from the number of homologous sites shared between the VGFs of two genomes to be compared.  Then, a table of distances between pairs of genomes can be used for calculating phylogenomic trees.

</div>

<div align="center">
<img src="Media/Genomica_VAMPhyRE.png" alt="Imagen" />
</div>

## External dependencies 
You must intall python and biopython library with
```
pip install biopython
```

## Installation

First, download the repository
```
git clone https://github.com/alfonsomt/vamphyre_tests.git
```


Execute the next comands
```
cd vamphyre_tests/
```
```
chmod +x Install_VAMPhyRE_test.sh
```
```
./Install_VAMPhyRE_test.sh
```

## Uninstalling VAMPhyRE

You must go to VAMPhyRE path "~/VAMPhyRE_test/" and execute the following comand:

```
sudo ~/VAMPhyRE_test/uninstall.sh
```

## Usage
### Show Help

```
VAMPhyRE.py -h
VAMPhyRE.py --help
```

### Test data

In "~/VAMPhyRE_test/" path you will find a directory called "datasets" which is used as test dataset. You can use the following comands to make a test results.

### Runing VAMPhyRE optimization
```
VAMPhyRE-opt.py -p vps8 -s1 ~/VAMPhyRE_test/datasets/hpv/hpv1.fasta -s2 ~/VAMPhyRE_test/datasets/hpv/hpv2.fasta 
```
This script will create a directory with variuos files used in the optimization, the "nslog.txt" file cotain the optimization results. 

### Runing VAMPhyRE
```
VAMPhyRE.py -p vps8 -t 8 -l 5 -r 5 -d 16 -g ~/VAMPhyRE_test/datasets/hpv

```
This script perform the VAMPhyRE metodology.

### VAMPhyRE-opt.py options
**-p** name of the file that contains the VPS, present in ~/VAMPhyRE/VPS/ path. You can add a file with user kmers as well. (mandatory)

**-s1** path of genome#1 that must be used to optimization (mandatory)

**-s2** path of genome#2 that must be used to optimization (mandatory)

**-m** number of optimization mismatch (default = 1) 


### VAMPhyRE.py options
**-p** name of the file that contains the VPS, present in ~/VAMPhyRE/VPS/ path. You can add a file with user kmers as well. 

**-t**, # number of threads.

**-l**, value of left extension, calculated with VAMPhyRE-opt.py

**-r**, value of right extension, calculated with VAMPhyRE-opt.py

**-d**, value of threshold, calculated with VAMPhyRE-opt.py

**-g**, Directory with genome files, must be in individual files in fasta format. Other formats are not allowed.

### Genomes with contigs
In case that your genomes contains contigs you must run the following script, before run any other script.

```
prepare_contigs.py -g Genome_dir
```
**-g** Genomes directory (default = Genomes)

**-e** Rile extension of genomes (default = fasta)
