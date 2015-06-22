#!/usr/bin/env perl
# Usage: ./recursive-search.pl <regex/string> <directories/files to search>
use File::Find;
use Term::ANSIColor;

$regex = shift @ARGV;

sub search_regex {
    # $_ contains the filename
    # find() changes directory so the filename is
    #   just <filename>
    $file_name = $_;

    open FILE, $file_name, or die $!;

    while(<FILE>) {
        if ($_ =~ $regex) {
            print color 'bold red';
            # $File::Find::name contains the full file name w/path
            # $. is the line number
            print "[$File::Find::name $.]: ";
            print color 'reset';

            # in this scope, $_ is the line
            print "$_";
        }
    }
    # Reset $. to 0 otherwise the file number
    #   just keeps incrementing to the total
    #   number of lines processed
    $. = 0;
}


find(\&search_regex, @ARGV);
