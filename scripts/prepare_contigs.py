#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        VAMPhyRE launcher
# Purpose:     Automate the pipeline for calculating Virtual Genomic Finger-
#              prints (VH5cmdl), counts the number of processing cores and 
#              creates a subprocess for each core, followed by parsing results
#              and calculation of a global table of hybridization (VHRP) and
#              comparison of fingerprints for calculation of distances/similarities.
#
# Author:      Mario Angel Lopez-Luis
#
# Created:     18/02/2025
# Copyright:   Alfonso Mendez-Tenorio 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from Bio import SeqIO
import os
import shutil
import argparse
import sys

parser = argparse.ArgumentParser()
print('minimal use: ' + '\n' +
      'prepare_contigs -g Genomes')
parser.add_argument("-g", "--GENOMES", type = str, metavar = "", 
                    default = 'example_dataset/',
                    help = 'Genomes directory (default = Genomes)')
parser.add_argument("-e", "--EXT", type = str, metavar = "", 
                    default = 'fasta',
                    help = 'file extension of genomes (default = fasta)')
args = parser.parse_args()
cmd = os.getcwd()
listfiles = os.listdir(os.path.join(cmd, args.GENOMES))

genomes = []
for l in listfiles:
    if l.endswith(args.EXT):
        genomes.append(l)
        
contigs = []
for g in genomes:
    fasta = list(SeqIO.parse(os.path.join(cmd, 
                                          args.GENOMES, 
                                          g), 
                             'fasta'))
    if len(fasta) > 1:
        contigs.append(g)

if len(contigs) > 0:
    for c in contigs:
        file = open(os.path.join(args.GENOMES + '/') + 'contig_' + c, 'w')
        fasta = list(SeqIO.parse(os.path.join(cmd, args.GENOMES, c), 'fasta'))
        file.write('>' + fasta[0].id + '\n')
        for s in fasta:
            file.write(str(s.seq) + 'X')
        file.close()

    try:
        os.makedirs('genomes_with_contigs')
        
    except FileExistsError:
        print("This program has been executed!, don't even try it!")

    for c in contigs:
        if os.path.exists('genomes_with_contigs' + c):
            print("This program has been executed!, don't even try it!", file = sys.stderr)
            sys.exit(1)
            
        ruta_origen = os.path.join(cmd, args.GENOMES, c)
        ruta_destino = os.path.join(cmd, 'genomes_with_contigs/')
        shutil.move(ruta_origen, ruta_destino)
    
    print('Your contigs were terminated!!!')

else:
    print('There is no contigs in your genome files!!!')

