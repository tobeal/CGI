#!/usr/bin/perl

use warnings;
use strict;
use CGI::Session;
use CGI;
use Net::LDAP;
use IO::Socket;
use IO::Socket::INET;
my $q = new CGI;
my $dn;
my $ip='172.20.1.117';
my $session = CGI::Session->load() or die "there is no session";

my $result=$session->delete();
printf $q->redirect("http://".$ip);
printf $q->header();
