#!/usr/bin/env perl

# FIXES array will contain all the issues that the script finds.
@FIXES = ();

# The first arg is the file to write to
$target = $ARGV[0];

foreach $file (@ARGV) {

    # The file to write to should not be included in the search
    # If it were included in the search, fixme issues would be duplicated
    if ($file eq $target) {
        next;
    }

    open FILE, "<", "$file" or die $!;

    # Search for the FIXME string
    while (<FILE>) {
        if ($_ =~ /FIXME.*\(/) {
            $file =~ s/.txt/$1/;
            $_.chomp();
            push @FIXES, "[[$file]] -> $_\\\\"; 
        }
    }
}

open FILE, "<", $target or die $!;

@LINES = <FILE>;
close(FILE);

open FILE, ">", $target or die $!;

foreach my $LINE ( @LINES ) {
    print FILE $LINE;

    # If the line "Fix Me Links" is found in the file
    # It means we have found the location where we want to start putting the links
    # Erase everything after the "Fix Me Link" line and insert a new line
    # Then write the @FIXES array to the end of the target file.
    if ($LINE =~ /Fix Me Links/) {
        print FILE "\n";
        foreach $line (@FIXES) {
            $insert = $line . "\n";
            print FILE $insert;
        }
        exit(0);
    }
}
