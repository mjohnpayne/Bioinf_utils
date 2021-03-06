#
# Author: Jarrod Chapmon, Isaac Ho
#
# Copyright 2011 The Regents of the University of California.
# All rights reserved.

# The United States Government has rights in this work pursuant
# to contracts DE-AC03-76SF00098, W-7405-ENG-36 and/or
# W-7405-ENG-48 between the United States Department of Energy
# and the University of California.

# Redistribution and use in source and binary forms are permitted
# provided that: (1) source distributions retain this entire
# copyright notice and comment, and (2) distributions including
# binaries display the following acknowledgement:  "This product
# includes software developed by the University of California,
# JGI-PSF and its contributors" in the documentation or other
# materials provided with the distribution and in all advertising
# materials mentioning features or use of this software.  Neither the
# name of the University nor the names of its contributors may be
# used to endorse or promote products derived from this software
# without specific prior written permission.

# THIS SOFTWARE IS PROVIDED "AS IS" AND WITHOUT ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE.

#!/jgi/tools/bin//perl -w
$n_args = @ARGV;
if (!$n_args)  {
    die "Usage: fastaLengths.pl <fasta file>\n";
}

foreach my $file (@ARGV) {

    open(F,$file) || die "Couldn't open $file\n";

    my $sequence = "";
    my $id = "NO_CURRENT_ID";
    my $n_bases = 0;

    while (my $i = <F>) {
	chomp $i;
	
	if ($i =~ /^>/) {
	    
	    if ($id ne "NO_CURRENT_ID") {
		$n_bases = length($sequence);
		print "$id\t$n_bases\n";
		$sequence = "";
	    }
	    
	    ($id) = $i =~ /^>(\S+)/;
	    
	} else {
	    
	    $sequence .= $i;
	}
    }
    close F;
    
    $n_bases = length($sequence);
    print "$id\t$n_bases\n";
}

