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
my $ldap = Net::LDAP->new("pruebasu.tk", version =>3, port=> 389);
my $session = CGI::Session->load() or die "there is no session";


if($session->is_expired() or $session->is_empty()){
	print $q->redirect("http://".$ip."/index.html");
}else{
	print $q->redirect("http://".$ip."/updateUser.html");
}

printf $q->header();
