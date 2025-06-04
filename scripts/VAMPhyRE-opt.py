#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:         VAMPhyRE launcher
# Purpose:      By providing two loosely related sequences, generates a random 
#               sequence with the randomseq program and compares pairs of sequences 
#               (original vs. original) and (original vs. randomized), using different 
#               combinations of extension-threshold with the programs VH5cmdl and VFAT, 
#               to estimate the best parameters that produce the optimal signal/noise 
#               ratio (s/n). These are the recommended parameters to maximize both the 
#               sensitivity and specificity when comparing more related genomes.
#
#
# Author:       Mario Angel Lopez-Luis
# Contributors: Emmanuel Canizal-Ramos
#               Francisco Federico Guevara-Roman
#               José MarÌa Rojas-Calvo
#
#	Definition: A contributor typically provides specific inputs or expertise,
#	while a collaborator actively works alongside others toward a common goal.
#	A contributor might be an individual who provides resources or knowledge,
#	like a writer for a publication, while a collaborator participates in a
#	team or project and contributes to its success.
#-------------------------------------------------------------------------------

import os
import subprocess
import math
from tqdm import tqdm
import argparse
import time 
import shutil
import sys

vamphyrepath = "~/VAMPhyRE/bin"

parser = argparse.ArgumentParser()
print('minimal use:\n' +
      'VAMPhyRE-opt.py -p vps8 -s1 path_to_sequence_1 -s2 -s1 path_to_sequence_1 \n')    
parser.add_argument("-p", "--PROBEFILE", type = str, 
                    default = "vps13", metavar = "",
                    help = 'VPS file (default = vps8')
parser.add_argument("-s1", "--SEQUENCE1", type = str, metavar = "",
                    help = 'set the path to sequence 1 (mandatory)')
parser.add_argument("-s2", "--SEQUENCE2", type = str, metavar = "",
                    help = 'set the path to sequence 2 (mandatory)')
parser.add_argument("-m" ,"--MISMATCHES", type = int, 
                    default = 0, metavar = "",
                    help = 'Number of allowed mismatches (default = 1)')
args = parser.parse_args()

if args.SEQUENCE1 == None:
    parser.print_help()
    sys.exit(1)

probefile = os.path.join(os.path.abspath(os.path.expanduser(vamphyrepath[:-3])), 'VPS/', args.PROBEFILE + '.txt')
with open(probefile, 'r') as file:
    lineas = list(file.readlines())
    probesize = int(len(lineas[0][:-1]))
sequence1 = args.SEQUENCE1
sequence2 = args.SEQUENCE2
mismatches = args.MISMATCHES
print('selected options:')
print('GENOME 1: ' + sequence1)
print('GENOME 2: ' + sequence2)
print('MISMATCHES: ' + str(mismatches))
print('PROBEFILE: ' + args.PROBEFILE + '.txt')
print('PROBESIZE: ' + str(probesize) + '\n')
#------------------------------
#------------------------------
#------------------------------
#------------------------------
strand = 'both'
format = 'NEXUS'
mode = 'DISTANCE'
tracking = 'YES'
trackext = 'NO'
list_signal = "Optimization_results/list_signal.txt"
list_noise = "Optimization_results/list_noise.txt"
lognsfile = "Optimization_results/nslog.txt"
globalfile = "Optimization_results/vhglobal_noise.txt"
logfile = "Optimization_results/vhlog_noise.txt"
vhout_signals = "Optimization_results/vhsignals.txt"
globalfile = "Optimization_results/vhglobal_signal.txt"
logfile = "Optimization_results/vhlog_signal.txt"
random_seq = 'Optimization_results/randomseq.fasta'
max_total_extension = 20
total_allowed_mismatches = 2
#------------------------------
#------------------------------
#------------------------------
#------------------------------

if os.path.exists('Optimization_results'):
    shutil.rmtree('Optimization_results')

os.makedirs('Optimization_results')

t = time.strftime("%I:%M:%S")
print('[%s] ' %t + 'Starting optimization')

if max_total_extension % total_allowed_mismatches != 0:
    print("The max extension value is not correct. Must be even")
    exit()

def worker(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    process.wait()

cmd = f"{vamphyrepath}/RandomSeq {sequence2} {random_seq}"
worker(cmd)

with open(list_signal, "w") as arch:
    arch.write(f"{sequence1}\n{sequence2}\n")

with open(list_noise, "w") as arch:
    arch.write(f"{sequence1}\n{random_seq}\n")

t = time.strftime("%I:%M:%S")
print('[%s] ' %t + 'Calculating signals of VH5')
cmd = f"{vamphyrepath}/VH5cmdl -probefile {probefile} -TARGETLIST {list_signal} -OUTFILE {vhout_signals} -MISMATCHES {mismatches} -STRAND {strand}"
worker(cmd)
    
t = time.strftime("%I:%M:%S")
print('[%s] ' %t + 'Calculating noise of VH5')
vhout_noise = "Optimization_results/vhnoise.txt"
cmd = f"{vamphyrepath}/VH5cmdl -probefile {probefile} -TARGETLIST {list_noise} -OUTFILE {vhout_noise} -MISMATCHES {mismatches} -STRAND {strand}"
random_cmd = f"{vamphyrepath}/RandomSeq {sequence2} {random_seq}"
worker(random_cmd)
worker(cmd)

t = time.strftime("%I:%M:%S")
print('[%s] ' %t + 'Calculating signals of VHRP')
cmd = f"{vamphyrepath}/VHRP -VHDATAFILE {vhout_signals} -PROBEFILE {probefile} -TARGETLIST {list_signal} -GLOBALFILE {globalfile} -SITESGLOBAL sites"
worker(cmd)

with open(logfile, "w") as arch:
    arch.write(cmd)

t = time.strftime("%I:%M:%S")
print('[%s] ' %t + 'Calculating noise of VHRP')
cmd = f"{vamphyrepath}/VHRP -VHDATAFILE {vhout_noise} -PROBEFILE {probefile} -TARGETLIST {list_noise} -GLOBALFILE {globalfile} -SITESGLOBAL sites"
worker(cmd)

with open(logfile, "w") as arch:
    arch.write(cmd)

totalsteps = max_total_extension // 2
snmax = 0
nsdata = []
print(f"Probe length is set to {probesize}")
print('Calculating the best extention and threshold, this could take a few minutes')
for istep in tqdm(range(totalsteps + 1)):
    leftext = istep
    rightext = istep
    threshold = probesize + (2 * istep) - total_allowed_mismatches

    vfatfile_signal = "Optimization_results/dist_signal.txt"
    trackfile_signal = "Optimization_results/track_signal.txt"
    cmd = f"{vamphyrepath}/VFAT -VHFILE {vhout_signals} -TARGETLIST {list_signal} -OUTFILE {vfatfile_signal} -LEFTEXT {leftext} " \
          f"-RIGHTEXT {rightext} -THRESHOLD {threshold} -FORMAT {format} -MODE {mode} -TRACKING {tracking} " \
          f"-TRACKFILE {trackfile_signal} -TRACKEXT {trackext}"    
    worker(cmd)

    vfatfile_noise = "Optimization_results/dist_noise.txt"
    trackfile_noise = "Optimization_results/track_noise.txt"
    cmd = f"{vamphyrepath}/VFAT -VHFILE {vhout_noise} -TARGETLIST {list_noise} -OUTFILE {vfatfile_noise} -LEFTEXT {leftext} " \
          f"-RIGHTEXT {rightext} -THRESHOLD {threshold} -FORMAT {format} -MODE {mode} -TRACKING {tracking} " \
          f"-TRACKFILE {trackfile_noise} -TRACKEXT {trackext}"
    worker(cmd)

    with open(trackfile_signal, "r") as arch:
        lines = arch.readlines()
        signal = len(lines) - 3

    with open(trackfile_noise, "r") as arch:
        lines = arch.readlines()
        noise = len(lines) - 3

    sn = math.log2((signal + 1) / (noise + 1))
    if sn > snmax:
        snmax = sn
        imax = istep

    snline = f"{rightext:3d} - {leftext:2d} {threshold:8d} {signal + 1:10d} {noise + 1:10d} {sn:10.2f}\n"
    nsdata.append(snline)

with open(lognsfile, "w") as arch:
    arch.write("\nExtension  Threshold  Signals      Noise    log2 s/n\n\n")
    arch.write("=========================================================\n")
    for i, linea in enumerate(nsdata):
        arch.write(linea)

        arch.write("\n")
    arch.write("=========================================================\n")

    leftext = imax
    rightext = imax
    threshold = probesize + (2 * imax) - total_allowed_mismatches
    arch.write(f"Optimal performance for {leftext}-{rightext}/{threshold} (extension/threshold)\n\n")

with open(lognsfile, "r") as arch:
    nsdata = arch.readlines()
    print("".join(nsdata))

print("Finished!!!")


