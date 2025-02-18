#!/usr/bin/perl -w
use strict;

my $vamphyrepath = "~/VAMPhyRE/bin";
my $list = "genome_list.txt";
my $vhfile = "vgfs_hpv_vps9.txt";
my $format = "NEXUS";
my $mode = "BOOTSTRAP";
my $tracking = "NO";
my $trackext = "NO";
my $replicates = 20;
my $leftext = 4;
my $rightext = 4;
my $threshold = 15;



my ($vfatfile, $trackfile, $cmdl, @vhcmd, $globalfile, $logfile, $i);




 $vfatfile = "boot\_$leftext\_$rightext\_$threshold.txt";
 $cmdl = "$vamphyrepath/VFAT -VHFILE $vhfile -TARGETLIST $list -OUTFILE $vfatfile -LEFTEXT $leftext " .
        "-RIGHTEXT $rightext -THRESHOLD $threshold -FORMAT $format -MODE $mode -TRACKING $tracking " .
        "-REPLICATES $replicates";
 print "$cmdl\n";
 @vhcmd = `$cmdl`;
 print "@vhcmd\n";
        

print "Finished\n";
exit;
