#!/usr/bin/env perl

@FIXES = ();
$cats = "hi";

foreach $file (@ARGV) {
    open FILE, "<", "$file" or die $!;
    while (<FILE>) {
        if ($_ =~ /FIXME.*\(/) {
            $file =~ s/.txt/$1/;
            $_.chomp();
            push @FIXES, "[[$file]] -> $_\\\\"; 
        }
    }
}

foreach $line (@FIXES) {
    print $line, "\n";
}
