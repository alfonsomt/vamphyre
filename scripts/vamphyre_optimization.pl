# VAMPhyRE optimization script

my $vamphyrepath = "bin/";
my $probefile = "VPS/vps8.txt";
my $probesize = 8;
#only two related sequences are requiered for the optimization
my $sequence1 = "example_dataset/HPV1.fasta";
my $sequence2 = "example_dataset/HPV4a.fasta";
my $mismatches = 1;
my $strand = "both";
my $format = "NEXUS";
my $mode = "DISTANCE";
my $tracking = "YES";
my $trackext = "NO";
my $dovh ="YES";

#In this case the list is internal
my $list = "list.txt";
my $list_signal = "list_signal.txt";
my $list_noise  = "list_noise.txt";
my $lognsfile = "nslog.txt";

#Only even values are allowed for extensions
my $max_total_extension = 20;
my $total_allowed_mismatches = 2; #For extended regions


if (($max_total_extension % 2) != 0) {
   print "The max extension value is not correct. Must be even\n";
   exit;
} 



my ($leftext, $rightext, $threshold, $vfatfile_signal, $trackfile_signal, $vfatfile_noise, $trackfile_noise, $cmdl, 
   $globalfile, $logfile, @vhcmd, $hits, $signal, $noise, $true_signal, $sn, @lines, @nsdata, $snmax, $imax);

#Zero step: Generate shuffled sequence
$cmdl = "$vamphyrepath/RandomSeq $sequence2 randomseq.fasta";
@vhcmd = `$cmdl`;
print "#@vhcmd\n";
open (ARCH, ">$list_signal");
print ARCH "$sequence1\n";
print ARCH "$sequence2\n";
close ARCH;

open (ARCH, ">$list_noise");
print ARCH "$sequence1\n";
print ARCH "randomseq.fasta\n";
close ARCH;


#First step: Virtual hybridization 
#for signals:
my $vhout_signals = "vhsignals.txt";
$cmdl = "$vamphyrepath/VH5cmdl -probefile $probefile -TARGETLIST $list_signal -OUTFILE $vhout_signals -MISMATCHES $mismatches -STRAND $strand";
print "$cmdl\n";
if ($dovh eq "YES") {
   @vhcmd = `$cmdl`;
   print "@vhcmd\n";
}

#for noise:
my $vhout_noise = "vhnoise.txt";
$cmdl = "$vamphyrepath/VH5cmdl -probefile $probefile -TARGETLIST $list_noise -OUTFILE $vhout_noise -MISMATCHES $mismatches -STRAND $strand";
print "$cmdl\n";
if ($dovh eq "YES") {
   #The random sequence must be calculated for the VH
   my  $randomcmdl = "$vamphyrepath/RandomSeq $sequence2 randomseq.fasta";
   my @RandomSeqCmd = `$randomcmdl`;
   print "@RandomSeqCmd\n";                                                                                                     
   @vhcmd = `$cmdl`;
   print "@vhcmd\n";
}


#Second step: Parsing VH results
#for signals
$globalfile ="vhglobal_signal.txt";
$logfile = "vhlog_signal.txt";
$cmdl ="$vamphyrepath/VHRP -VHDATAFILE $vhout_signals -PROBEFILE $probefile -TARGETLIST $list_signal -GLOBALFILE $globalfile -SITESGLOBAL sites";
@vhcmd = `$cmdl`;
print "@vhcmd\n";

open (ARCH, ">$logfile");
print ARCH "@vhcmd\n";
close (ARCH);

#for noise
$globalfile ="vhglobal_noise.txt";
$logfile = "vhlog_noise.txt";
$cmdl ="$vamphyrepath/VHRP -VHDATAFILE $vhout_noise -PROBEFILE $probefile -TARGETLIST $list_noise -GLOBALFILE $globalfile -SITESGLOBAL sites";
@vhcmd = `$cmdl`;
print "@vhcmd\n";

open (ARCH, ">$logfile");
print ARCH "@vhcmd\n";
close (ARCH);



#Third step: VFAT analysis at different extensions
my $istep;
my $totalsteps = $max_total_extension / 2;

print "\nProbe lenght is set to $probesize\n\n";

$snmax = 0;
for (my $istep = 0; $istep < $totalsteps+1; $istep++) {
    
    #only for test
    $leftext = $istep;
    $rightext = $istep;
    $threshold = $probesize + (2*$istep) - $total_allowed_mismatches;

    $vfatfile_signal = "dist_signal.txt";
    $trackfile_signal = "track_signal.txt";
    $cmdl = "$vamphyrepath/VFAT -VHFILE $vhout_signals -TARGETLIST $list_signal -OUTFILE $vfatfile_signal -LEFTEXT $leftext " .
        "-RIGHTEXT $rightext -THRESHOLD $threshold -FORMAT $format -MODE $mode -TRACKING $tracking " .
        "-TRACKFILE $trackfile_signal -TRACKEXT $trackext";
    print "$cmdl\n";
    @vhcmd = `$cmdl`;
    print "@vhcmd\n";        

    $vfatfile_noise = "dist_noise.txt";
    $trackfile_noise = "track_noise.txt";
    $cmdl = "$vamphyrepath/VFAT -VHFILE $vhout_noise -TARGETLIST $list_noise -OUTFILE $vfatfile_noise -LEFTEXT $leftext " .
        "-RIGHTEXT $rightext -THRESHOLD $threshold -FORMAT $format -MODE $mode -TRACKING $tracking " .
        "-TRACKFILE $trackfile_noise -TRACKEXT $trackext";
    print "$cmdl\n";
    @vhcmd = `$cmdl`;
    print "@vhcmd\n";

    open (ARCH, "$trackfile_signal");
    @lines = <ARCH>;
    close ARCH;
    $signal = (scalar @lines)-3;

    open (ARCH,"$trackfile_noise");
    @lines = <ARCH>;
    close ARCH;
    $noise = (scalar @lines)-3;
    #$true_signal = $signal-$noise;   
    $sn = log(($signal+1)/($noise+1))/log(2);
    if ($sn > $snmax) {
        $snmax = $sn;
	$imax = $istep;
    }
    my $snline = sprintf("%3d - %2d %8d %10d %10d %10.2f\n", $rightext, $leftext, $threshold, $signal+1,  $noise+1, $sn);
    push @nsdata, $snline;
}

open(ARCH, ">$lognsfile");

print ARCH "Extension  Threshold  Signals      Noise    log2 s/n\n\n";
print ARCH "=========================================================\n";
my $linea;
my $i = 0;
foreach $linea (@nsdata) {
    chomp $linea;
    print ARCH "$linea";
    if ($i == $imax) { 
	print ARCH " \<\=opt\n";
    } else {
        print ARCH "\n";
    }
    $i++;
}
print ARCH "=========================================================\n";

$leftext = $imax;
$rightext = $imax;
$threshold = $probesize + (2*$imax) - $total_allowed_mismatches;
print ARCH "Optimal performance for $leftext\-$rightext\/$threshold (extension\/threshold)\n\n";
close ARCH;
open (ARCH, "$lognsfile");
@nsdata = <ARCH>;
close ARCH;
print "@nsdata";
print "Finished\n";
exit;
