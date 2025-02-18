#! /usr/bin/perl
#retrieve_seq.pl
#version 1
#
#Written by Paul Stothard, Canadian Bioinformatics Help Desk
#based on a script by Oleg Khovayko http://olegh.spedia.net
#Modified for Alfonso Mendez Tenorio to allow https and other formats Dec 12,2016
#This script uses NCBI's Entrez Programming Utilities to perform
#batch requests to NCBI Entrez.
#
#Values in the 'edit these' section should be changed to meet your requirements
#Warning!!!:  If initialization errors are raise may you need to install some
#additional packages:
#sudo perl -MCPAN -e shell
#cpan>install LWP::Simple
#cpan>install Mozilla::CA 
#See 'Entrez Programming Utilities' for more info at
#http://eutils.ncbi.nlm.nih.gov/entrez/query/static/eutils_help.html
#################################################################################
#$GenomeList: Name of the file with the list of accession keys to be downloaded #
#################################################################################

use warnings;
use strict;
use LWP::Simple;
use LWP::UserAgent;   

#--------------edit these
my $output_file;
my $db;
my $query;
my $report; 
#---------------

my $url;
my $esearch;

my $esearch_result;

#my $esearch_result;

my $count;
my $query_key;
my $web_env;

my $retstart;
my $retmax;


my $GenomeList = "listita.txt";   #List of sequences to search
my @Genomes;
my $Nogenomas;
my $prog;


#All sequence's names are stored in the array @Genome 
open (INFILE, $GenomeList);
  @Genomes = <INFILE>;
close INFILE;

$Nogenomas = scalar @Genomes;
  
my $i;
for($i=0; $i < $Nogenomas; $i++){
    $query = $Genomes[$i];
    chomp $query;

    $output_file = $query . ".txt";
    #$output_file = $query . ".fasta";
    #$output_file = $query . ".gb";
    #$output_file = $query . ".fasta"; 
    $db = "nucleotide";
    #$query = "NC_007530[accession]";
    #Access keys are important, as RefSeq records do not include the sequence, just the annotation 
    #Report can be gb, fasta or ft (feature table), but can be others 
    #$report = "gb";
    $report = "fasta";
    $report = "ft";
    #$report = "gbwithparts";
    #$report = "fasta_cds_na"; 

    $url = "https://www.ncbi.nlm.nih.gov/entrez/eutils";
    $esearch = "$url/esearch.fcgi?" . "db=$db&retmax=1&usehistory=y&term=";
    #This is a remot search, with LWP
    
    my $ua = LWP::UserAgent->new();
    my $req = new HTTP::Request GET => $esearch . $query;
    my $res = $ua->request($req);
    my $esearch_result = $res->content;

#print "$esearch_result\n";
#exit;

    #my $esearch_result = get($esearch . $query);  
    #A regular expression to extract the data
    $esearch_result =~  m/<Count>(\d+)<\/Count>.*<QueryKey>(\d+)<\/QueryKey>.*<WebEnv>(\S+)<\/WebEnv>/s;

    $count = $1;
    $query_key = $2;
    $web_env = $3;


    $retmax = 500;



    open (OUTFILE, ">" . $output_file) or die ("Error: Cannot open $output_file : $!");

    #print "$count entries to retrieve\n";
    #print "retrieving $i entry ...";

    for ($retstart = 0; $retstart < $count; $retstart = $retstart + $retmax) {
        #print "Requesting entries $retstart to " . ($retstart + $retmax) . "\n";
        $prog = $i+1;
        print "Downloading entry $prog: $query...\n";
        my $efetch = "$url/efetch.fcgi?" . "rettype=$report&retmode=text&retstart=$retstart&retmax=$retmax&" . "db=$db&query_key=$query_key&WebEnv=$web_env";   

        #my $ua = LWP::UserAgent->new();
        #my $req = new HTTP::Request GET => $esearch . $query;
        #my $res = $ua->request($req);
        #my $efetch_result = $res->content;
        my $efetch_result = get($efetch);

        print (OUTFILE $efetch_result);  #gets the sequence
        sleep(3);  #This is an obligatory delay to avoid hanging the NCBI web server
    }

    close (OUTFILE) or die( "Error: Cannot close $output_file file: $!");

}

print "Finished...\n";

exit;
