#!/usr/bin/env perl
# This short script just adds color to the matching portion of the string.
# There must be a regex pattern as the first argument.
# Otherwise input can come from a file, from a pipe, a redirect, or from the standard input stream.

use Term::ANSIColor;

my $regex = shift@ARGV;
$regex = "(" . $regex . ")";

while (<>) {
    if ($_ =~ m{$regex}g) {
        printf $`;

        print color 'bold red';
        printf "$1";

        print color 'reset';
        print $';
    }
}

