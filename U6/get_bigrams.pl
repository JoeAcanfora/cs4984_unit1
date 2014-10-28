#!/usr/bin/perl

use strict;
use warnings;

my $name = $ARGV[0];

open (LOAD, $name) or die ("could not open file");

my $output = $name;
$output .= "_out.txt";
open (OUT, "+>", $output) or die ("could not make output");

while (my $row = <LOAD>)
{
	chomp $row;
	my @tokens = split(/'/, $row);
	print OUT "$tokens[1] $tokens[3]\n";
}