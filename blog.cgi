#!/usr/bin/perl

use warnings;
use strict;
use CGI;
use CGI::Session;
use Net::LDAP;
use IO::Socket;
use IO::Socket::INET;
use Net::SSH::Perl;
my $q = CGI->new;
my $ip='172.20.1.117';
my $dn;
my $session = CGI::Session->load() or die "there is no session";
my $nameUser=$session->param('userName');

if($session->is_expired() or $session->is_empty()){
        print $q->redirect("http://".$ip."/index.html");
}else{
        print $q->redirect("http://".$ip."/~$nameUser/blogUsers");
}

printf $q->header();

