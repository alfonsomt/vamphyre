#!/usr/bin/env python
import os
import subprocess
import math
from tqdm import tqdm
import argparse
import time 


vamphyrepath = "~/VAMPhyRE_test/bin"

parser = argparse.ArgumentParser()
print('minimal use:\n' +
      'VAMPhyRE-opt.py -p vps8 -s1 path_to_sequence_1 -s2 -s1 path_to_sequence_1 \n')
      
parser.add_argument("-p", "--PROBEFILE", type = str, 
                    default = "vps13", metavar = "",
                    help = 'VPS file (default = vps8)')

parser.add_argument("-s1", "--SEQUENCE1", type = str, 
                    default = "Genomas/HpGP-ALG-001.fsa", metavar = "",
                    help = 'set the path to sequence 1')

parser.add_argument("-s2", "--SEQUENCE2", type = str, 
                    default = "Genomas/HpGP-ALG-002.fsa", metavar = "",
                    help = 'set the path to sequence 2')

parser.add_argument("-m" ,"--MISMATCHES", type = int, 
                    default = 1, metavar = "",
                    help = 'Number of allowed mismatches (default = 1)')

parser.add_argument("-strand", "--STRAND", 
                    type = str, default= "both", metavar = "",
                    help = 'Strad used as target [direct/comple/both]  (default = both)')

parser.add_argument("-format", "--VFATFORMAT", 
                    type = str, metavar = "", default = "NEXUS",
                    help = 'Format of the distance table [MEGA/PHYLIP/NEXUS] (default = MEGA)')

parser.add_argument("-mode","--MODE", type = str, metavar = "", 
                    default = "DISTANCE",
                    help = 'Comparison mode [CHAR/DISTANCE/BOOTSTRAP] (default = DISTANCE)')

parser.add_argument("-tracking","--TRACKING", 
                    type = str, metavar = "" , default = "YES",
                    help = 'Track pairs of extended probes [YES/NO] (default = YES)')

parser.add_argument("-trackext","--TRACKEXT", type = str, metavar = "", default = "NO",
                    help = 'Track extended segments [YES/NO] (default = NO)')


args = parser.parse_args()

probefile = os.path.join(os.path.abspath(os.path.expanduser(vamphyrepath[:-3])), 'VPS/', args.PROBEFILE + '.txt')
probesize = int(args.PROBEFILE[3:])
sequence1 = args.SEQUENCE1
sequence2 = args.SEQUENCE2
mismatches = args.MISMATCHES
strand = args.STRAND
format = args.VFATFORMAT
mode = args.MODE
tracking = args.TRACKING
trackext = args.TRACKEXT
max_total_extension = 20
total_allowed_mismatches = 2

list_signal = "temp_list_signal.txt"
list_noise = "temp_list_noise.txt"
lognsfile = "temp_nslog.txt"
globalfile = "temp_vhglobal_noise.txt"
logfile = "temp_vhlog_noise.txt"
vhout_signals = "temp_vhsignals.txt"
globalfile = "temp_vhglobal_signal.txt"
logfile = "temp_vhlog_signal.txt"
random_seq = 'temp_randomseq.fasta'


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
vhout_noise = "temp_vhnoise.txt"
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

    vfatfile_signal = "temp_dist_signal.txt"
    trackfile_signal = "temp_track_signal.txt"
    cmd = f"{vamphyrepath}/VFAT -VHFILE {vhout_signals} -TARGETLIST {list_signal} -OUTFILE {vfatfile_signal} -LEFTEXT {leftext} " \
          f"-RIGHTEXT {rightext} -THRESHOLD {threshold} -FORMAT {format} -MODE {mode} -TRACKING {tracking} " \
          f"-TRACKFILE {trackfile_signal} -TRACKEXT {trackext}"    
    worker(cmd)

    vfatfile_noise = "temp_dist_noise.txt"
    trackfile_noise = "temp_track_noise.txt"
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

files = os.listdir('.')

r_files = []
for f in files:
    if f.startswith("temp_"):
        os.remove(f)

print("Finished!!!")


