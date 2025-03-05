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
# Author:      Mario Angel Lopez-Luis and Emanuel Canizal
#
# Created:     18/02/2025
# Copyright:   Alfonso Mendez-Tenorio 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import multiprocessing
import subprocess
import os
import threading
import argparse
import re 
import time 
import sys
from tqdm import tqdm
from Bio import SeqIO
import pandas as pd

VAMPhyRE_path = '~/VAMPhyRE/'

inicio = time.time()
parser = argparse.ArgumentParser()
print('Minimal use:' + '\n' + 
      'VAMPhyRE.py -p vps8 -t 8 -l 5 -r 5 -d 16 -g Genome_dir' +
      '\n\n')
parser.add_argument("-p", "--PROBEFILE", type = str, default = "vps8", metavar = "",
                    help = 'VPS file (default = vps8)')

parser.add_argument("-t", "--T", type = int, metavar = "", default = 1,
                    help = '# Threads (default = 1)')

parser.add_argument("-l", "--LEFTEXT", type = int, metavar = "", default = 0,
                    help = 'Left Extention  (default = 0)')

parser.add_argument("-r" ,"--RIGHTEXT", type = int, metavar = "", default = 0,
                    help = 'right Extention  (default = 0)')

parser.add_argument("-d" ,"--THRESHOLD", type = int, metavar = "", default = -1,
                    help = 'Threshold (default = -1)')

parser.add_argument("-g", "--GENOMES", type = str, metavar = "",
                    help = 'Genomes directory (mandatory)')
                    
parser.add_argument("-fasta-ext", "--FASTA_EXT", type = str, metavar = "", default = 'fasta',
                    help = 'fasta genomes file extention  (default = fasta)')

parser.add_argument("-list", "--TARGETLIST", type = str,default = "genome_list.txt", metavar = "",
                    help = ('Filters for the report of sites:' + '\n' +
                  '\t' +'allowed : Only sites with the allowed number of mismatches' + '\n' +
                  '\t' +'atmost  : Sites with less or at most the allowed number of ' +
                            'mismatches' + '\n' +
                  '\t' +'more    : Include some more sites with more mismatches than' + 
                            'the allowed but with stability inside the Gcutoff' + '\n'))

parser.add_argument("-outfile" ,"--OUTFILE", type = str, default = 'vh5_out_global.txt', metavar = "",
                    help = 'File to store the results (default = vh5_out_global.txt)')

parser.add_argument("-strand", "--STRAND", type = str, default= "both", metavar = "",
                    help = 'Strad used as target [direct/comple/both]  (default = both)')

parser.add_argument("-sites-filtering","--SITESFILTERING", type = str, default= "atmost", metavar = "",
                    help = 'Filters for the report of sites:' + '\n' + 
                  'allowed : Only sites with the allowed number of mismatches' + '\n' +
                  'atmost  : Sites with less or at most the allowed number of' + '\n' +   
                            'mismatches (default);' + '\n' +
                  'more    : Include some more sites with more mismatches than ' + '\n' +
                            'the allowed but with stability inside the Gcutoff (default = atmost)')

parser.add_argument("-sites-ambig" ,"--SITESAMBIG", type = str, default = "all", metavar = "",
                    help = 'Number of hybridization sites reported for probe:' + '\n' +
                  'all       : All the sites found by probe (default = all)')

parser.add_argument("-vh-format", "--RESULTSFORMAT", type = str, default = "reduced", metavar = "",
                    help = 'reduced : Use recent more compact format of results' + '\n' +
                  'original: Original format of VH results (default = reduced)')

parser.add_argument("-gc-cutoff","--GCUTOFF", type = int, default = 0, metavar = "",
                    help = 'Free energy cut off (Kcal/mol) (default = 0)')

parser.add_argument("-m" ,"--MISMATCHES", type = int, default = 0, metavar = "",
                    help = 'Number of allowed mismatches (0 - probe length) (default = 0)')

parser.add_argument("-b", "--BATCH", type = int, metavar = "", default = 1,
                    help = 'Number of batch (default = 1), in case of very old computers, use of 2 or more')

parser.add_argument("-o" ,"--VFATOUTFILE", type = str, default = 'vfat_outfile', metavar = "",
                    help = 'File to store the results of phylogeny (default = vfat_outfile)')

parser.add_argument("-format", "--VFATFORMAT", type = str, metavar = "", default = "MEGA",
                    help = 'Format of the distance table [MEGA/PHYLIP/NEXUS] (default = MEGA)')

parser.add_argument("-mode","--MODE", type = str, metavar = "", default = "DISTANCE",
                    help = 'Comparison mode [CHAR/DISTANCE/BOOTSTRAP] (default = DISTANCE)')

parser.add_argument("-model","--MODEL", type = str, metavar = "", default = "NEI",
                    help = 'Model for distance calculation [NEI/BROWN] (default = NEI)')

parser.add_argument("-counts","--COUNTS", type = str, metavar = "", default = "DEGENERATED",
                    help = 'Sites counting mode [SINGLE/DEGENERATED] (default = DEGENERATED)')

parser.add_argument("-tracking","--TRACKING", type = str, metavar = "" , default = "NO",
                    help = 'Track pairs of extended probes [YES/NO] (default = NO)')

parser.add_argument("-tracking-file","--TRACKFILE", type = str, metavar = "",default = "track.txt",
                    help = 'Tracking file name (default = track.txt)')

parser.add_argument("-trackext","--TRACKEXT", type = str, metavar = "", default = "NO",
                    help = 'Track extended segments [YES/NO] (default = NO)')
parser.add_argument("-replicates","--REPLICATES", type = int, metavar = "", default = 1,
                    help = 'Number of bootstrap replicates (default = 1)')
args = parser.parse_args()

if args.GENOMES == None:
    parser.print_help()
    sys.exit(1)

if args.PROBEFILE + '.txt' not in os.listdir(os.path.join(os.path.abspath(os.path.expanduser(VAMPhyRE_path)), 'VPS/')):
    print(f"Error: PROBEFILE '{args.PROBEFILE}' is not a valid option" + 
          "\n" + "Please Check VPS/ directory for valid VPS option")
    sys.exit(1)

if args.T > os.cpu_count():
    print("Error: Threads exceed" + 
          "\n" + "Please Check -T option")
    sys.exit(1)
    
def leer_txt(file):
    kmers = []
    with open(file) as archivo:
        for linea in archivo:
            kmers.append(str(linea).replace('\n',''))
    return(kmers)

def prepocesamiento(directorio_de_genomas):
    lists = f'ls -1 {directorio_de_genomas}/* > {args.TARGETLIST}'
    subprocess.run(lists, shell = True)
    fi = leer_txt(f'{args.TARGETLIST}')
    nombres_reales = []
    file = open('names.txt', 'w')
    for n, i in enumerate(fi):
        seq = list(SeqIO.parse(i, args.FASTA_EXT))
        nombres_reales.append(seq[0].id)
        file.write('temp_' + str("%05d" % n) + ';' + str(seq[0].id) + '\n')
    file.close()
    
    for n, i in enumerate(fi):
        seq = list(SeqIO.parse(i, args.FASTA_EXT))
        fasta = open(i, 'w')
        fasta.write('>' + 'temp_' + str("%05d" % n) + '\n' +
                    str(seq[0].seq) + '\n')
        fasta.close()
    return(nombres_reales)
    
def worker(outfile, tarlist):
    cmd = os.path.abspath(os.path.expanduser(VAMPhyRE_path))
    vh5path = os.path.join(cmd, 'bin/VH5cmdl')    
    comando = [vh5path, f"-PROBEFILE {vps_path} -TARGETLIST {tarlist} -OUTFILE vh5_out_{outfile}.txt -MISMATCHES {args.MISMATCHES} -STRAND {args.STRAND} -SITESFILTERING {args.SITESFILTERING} -SITESAMBIG {args.SITESAMBIG} -RESULTSFORMAT {args.RESULTSFORMAT} -GCUTOFF {args.GCUTOFF}"]
    
    try:
        subprocess.run(comando, stdout = subprocess.PIPE)
        
    except subprocess.CalledProcessError as e:
        print(f"Error en VH5: {e}")
	
def vhrp_worker():
    cmd = os.path.abspath(os.path.expanduser(VAMPhyRE_path))
    vhrp = os.path.join(cmd, "bin/VHRP")
    comando = [vhrp, '-VHDATAFILE', args.OUTFILE, '-PROBEFILE', vps_path, '-TARGETLIST', args.TARGETLIST, 
               '-GLOBALFILE', 'vh_global.csv', '-SITESGLOBAL', 'sites']
    try:
        subprocess.run(comando, stdout = subprocess.PIPE )

    except subprocess.CalledProcessError as e:
        print(f"Error en VHRP: {e}")

def worker_vfat():
    cmd = os.path.abspath(os.path.expanduser(VAMPhyRE_path))
    vfatpath = os.path.join(cmd, "bin/VFAT")
    comando = [vfatpath ,"-VHFILE", args.OUTFILE,
                         "-TARGETLIST",args.TARGETLIST,
                         "-OUTFILE",args.VFATOUTFILE,
                         "-MODE",args.MODE,"-LEFTEXT",str(args.LEFTEXT),
                         "-RIGHTEXT",str(args.RIGHTEXT),
                         "-THRESHOLD",str(args.THRESHOLD),
                         "-FORMAT",args.VFATFORMAT,
                         "-MODEL",args.MODEL,"-COUNTS",args.COUNTS,
                         "-TRACKING",args.TRACKING,
                         "-TRACKFILE",args.TRACKFILE,
                         "-TRACKEXT",args.TRACKEXT,
                         "-REPLICATES",str(args.REPLICATES)]
    
    try:
        subprocess.run(comando, stdout = subprocess.PIPE )

    except subprocess.CalledProcessError as e:
        print(f"Error en VFAT: {e}")
        
def regresar_nombres(nombres):
    fi = leer_txt(f'{args.TARGETLIST}')
    for i, n in zip(fi, nombres):
        seq = list(SeqIO.parse(i, 'fasta'))
        fasta = open(i, 'w')
        fasta.write('>' + n + '\n' +
                    str(seq[0].seq) + '\n')
        fasta.close()
#-----------
#-----------
#-----------
print('argumentos -PROBEFILE : ' + str(os.path.join(os.path.abspath(os.path.expanduser(VAMPhyRE_path)), 'VPS/', args.PROBEFILE + '.txt')))
print('argumentos -T: ' + str(args.T))
print('argumentos -LEFTEXT: ' + str(args.LEFTEXT))
print('argumentos -RIGHTEXT: ' + str(args.RIGHTEXT))
print('argumentos -THRESHOLD: ' + str(args.THRESHOLD))
print('argumentos -TARGETLIST: ' + args.TARGETLIST)
print('argumentos -OUTFILE: ' + args.OUTFILE)
print('argumentos -STRAND: ' + args.STRAND)
print('argumentos -SITESFILTERING: ' + args.SITESFILTERING)
print('argumentos -SITESAMBIG: ' + args.SITESAMBIG)
print('argumentos -RESULTSFORMAT: ' + args.RESULTSFORMAT)
print('argumentos -GCUTOFF: ' + str(args.GCUTOFF))
print('argumentos -MISMATCHES: ' + str(args.MISMATCHES))
print('argumentos -BATCH: ' + str(args.BATCH))
print('argumentos -VFATOUTFILE: ' + args.VFATOUTFILE)
print('argumentos -VFATFORMAT: ' + args.VFATFORMAT)
print('argumentos -MODE: ' + args.MODE)
print('argumentos -MODEL: ' + args.MODEL)
print('argumentos -COUNTS: ' + str(args.COUNTS))
print('argumentos -TRACKING: ' + args.TRACKING)
print('argumentos -TRACKFILE: ' + args.TRACKFILE)
print('argumentos -TRACKEXT: ' + args.TRACKEXT)
print('argumentos -REPLICATES: ' + str(args.REPLICATES))
print('PLEASE DO NOT KILL THE EXECUTION MAY CAUSE LOSS GENOME NAMES')


real_names = prepocesamiento(args.GENOMES)
f = open(args.TARGETLIST).readlines()

#-----------
#-----------
path_tar = os.path.join(os.getcwd(), args.TARGETLIST)
vps_path = os.path.join(os.path.abspath(os.path.expanduser(VAMPhyRE_path)), 'VPS/', args.PROBEFILE + '.txt')
#-----------
#-----------

t = time.strftime("%I:%M:%S")
print("[%s] " %t + "Launching...")

number_list = 0
list_of_list = []
while args.T > number_list:
	list_of_list.append([])
	number_list = number_list + 1

lls = 0
for i in list_of_list:
	if len(f)%args.T > 0 and lls < len(f)%args.T :
			i.append(len(f)//args.T + 1)
			lls = lls + 1
	else:
		i.append(len(f)//args.T)

lls = 0 
for i in list_of_list:
	list_temp = []
	for t in range(i[0]//args.BATCH):
		list_temp.append(args.BATCH)
	if i[0]%args.BATCH > 0:
		list_temp.append(i[0]%args.BATCH)
	list_of_list[lls]= list_temp
	lls = lls + 1 

cont = 0
cont_text = 0 
list_of_list_tag = []
for i in list_of_list:
	for t in i:
		l_grab = open(f"{cont_text}_genomes.txt", "w")
		to_write = f[cont:(t+cont)]
		for l in to_write:
			l_grab.write(l)
		l_grab.close()
		list_of_list_tag.append(f"{cont_text}_genomes.txt")
		cont = cont + t
		cont_text = cont_text + 1 
		
l1 = 0
l2 = 0
l3 = 0
for i in list_of_list:
	l3 = 0
	for t in i:
		list_of_list[l2][l3] = list_of_list_tag[l1]
		l1 = l1 +1
		l3 = l3 + 1 
	l2 = l2 + 1

t = time.strftime("%I:%M:%S")
print("[%s] " %t + "Starting VAMPhyRE")
threads = []
var_cut = len(list_of_list_tag)
pbar = tqdm(total = len(list_of_list_tag), desc = "Progreso")
while var_cut > 0:
	for i in list_of_list: 
		if var_cut == 0:
			break
		w = (re.search("[0-9]*",i[0])).group(0)
		k = threading.Thread(target=worker, args= (str(w), i[0]))  
		k.start()
		threads.append(k)
		var_cut = var_cut - 1
		i.remove(i[0])
	for r in threads:
		r.join()
		pbar.update(1)
	threads = []
pbar.close()

t = time.strftime("%I:%M:%S")
print("[%s] " %t + "Gathering data")
vh_global = []
aux_14 = True
for i in range(len(list_of_list_tag)):
	vh = open(f"vh5_out_{i}.txt","r")
	vh_1 = vh.readlines()
	vh.close
	if aux_14 == True:
		for t in vh_1:
			if t.startswith("# Number of sequences ="):
				t_aux = f"# Number of sequences = {len(f)}\n"
				index_t = vh_1.index(t)
				vh_1.remove(t)
				vh_1.insert(index_t,t_aux)
				break
			else:
				pass
		aux_14 = False
	else:
		aux_var = 0
		for t in vh_1:
			if t.startswith(">") == True:
				for i in range(aux_var):
					vh_1.remove(vh_1[0])
				break
			else:
				aux_var = aux_var + 1
	vh_global.append(vh_1)
	vh_1 = []

r = open(f"{args.OUTFILE}","w")
for i in vh_global:
	for t in i:
		r.write(t)
r.close()

for i, c in zip(list_of_list_tag, range(len(list_of_list_tag))):
	os.remove(f"vh5_out_{c}.txt")
	os.remove(f"{c}_genomes.txt")

t = time.strftime("%I:%M:%S")
print("[%s] " %t + "Starting VHRP")
vhrp_worker()
t = time.strftime("%I:%M:%S")
print("[%s] " %t + "VHRP Finished!!")

t = time.strftime("%I:%M:%S")
print("[%s] " %t + "Starting VFAT")
worker_vfat()
t = time.strftime("%I:%M:%S")
print("[%s] " %t + "VFAT Finished!!")

regresar_nombres(real_names)

vh_global = pd.read_csv('vh_global.csv', index_col = 0)
vh_global = vh_global.drop(columns = [vh_global.columns[-1]])
vh_global.columns = real_names
vh_global.to_csv('vh_global.csv')

final = time.time()
t = time.strftime("%I:%M:%S")
print("[%s] " %t , f"Execution time: {final-inicio} s")
print('Thanks for using VAMPhyRE!!!!!')
print("Don't Forget to cite us")
