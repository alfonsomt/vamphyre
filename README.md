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
 -h, --help            show this help message and exit
  -p , --PROBEFILE      VPS file (default = vps8)
  -t , --T              # Threads (default = 1)
  -leftext , --LEFTEXT 
                        Left Extention (default = 0)
  -rightext , --RIGHTEXT 
                        right Extention (default = 0)
  -threshold , --THRESHOLD 
                        Threshold (default = -1)
  -g , --GENOMES        Genomes directory (default = Genomes)
  -fasta-ext , --FASTA_EXT 
                        fasta genomes file extention (default = fasta)
  -list , --TARGETLIST 
                        Filters for the report of sites: allowed : Only sites with the allowed
                        number of mismatches atmost : Sites with less or at most the allowed
                        number of mismatches more : Include some more sites with more mismatches
                        thanthe allowed but with stability inside the Gcutoff
  -outfile , --OUTFILE 
                        File to store the results (default = vh5_out_global.txt)
  -strand , --STRAND    Strad used as target [direct/comple/both] (default = both)
  -sites-filtering , --SITESFILTERING 
                        Filters for the report of sites: allowed : Only sites with the allowed
                        number of mismatches atmost : Sites with less or at most the allowed
                        number of mismatches (default); more : Include some more sites with more
                        mismatches than the allowed but with stability inside the Gcutoff (default
                        = atmost)
  -sites-ambig , --SITESAMBIG 
                        Number of hybridization sites reported for probe: all : All the sites
                        found by probe (default = all)
  -vh-format , --RESULTSFORMAT 
                        reduced : Use recent more compact format of results original: Original
                        format of VH results (default = reduced)
  -gc-cutoff , --GCUTOFF 
                        Free energy cut off (Kcal/mol) (default = 0)
  -m , --MISMATCHES     Number of allowed mismatches (0 - probe length) (default = 0)
  -b , --BATCH          Number of batch (default = 1), in case of very old computers, use of 2 or
                        more
  -o , --VFATOUTFILE    File to store the results of phylogeny (default = vfat_outfile)
  -format , --VFATFORMAT 
                        Format of the distance table [MEGA/PHYLIP/NEXUS] (default = MEGA)
  -mode , --MODE        Comparison mode [CHAR/DISTANCE/BOOTSTRAP] (default = DISTANCE)
  -model , --MODEL      Model for distance calculation [NEI/BROWN] (default = NEI)
  -counts , --COUNTS    Sites counting mode [SINGLE/DEGENERATED] (default = DEGENERATED)
  -tracking , --TRACKING 
                        Track pairs of extended probes [YES/NO] (default = NO)
  -tracking-file , --TRACKFILE 
                        Tracking file name (default = track.txt)
  -trackext , --TRACKEXT 
                        Track extended segments [YES/NO] (default = NO)
  -replicates , --REPLICATES 
                        Number of bootstrap replicates (default = 1)

