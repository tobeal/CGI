#!/usr/bin/perl
use Quota;
use strict;
use warnings;

my $nameUser=$ENV{'PAM_USER'};
my $uidNumber=getpwnam($nameUser);

Quota::setqlim('/dev/sda5',$uidNumber,5000,8000,0,0,0,0);
