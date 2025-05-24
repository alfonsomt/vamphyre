#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Prepare contigs
# Purpose:     Detection of contigs presence within fasta genome files
#
# Author:       Mario Angel Lopez-Luis
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
                    help = 'Genomes directory (default = Genomes)')
args = parser.parse_args()
 
if args.GENOMES == None:
    parser.print_help()
    sys.exit(1)

cmd = os.getcwd()
listfiles = os.listdir(os.path.join(cmd, args.GENOMES))
        
contigs = []
for g in listfiles:
    fasta = list(SeqIO.parse(os.path.join(cmd, 
                                          args.GENOMES, 
                                          g), 
                             'fasta'))
    if len(fasta) > 1:
        contigs.append(g)
        
    elif len(fasta) == 0:
    	print('Check your genome directory, there are files that is not genomes!!!')
    	sys.exit(1)

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
    
    print('Your contigs were processed!!!')

else:
    print('There is no contigs in your genome files!!!')

