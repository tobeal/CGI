#!/usr/bin/perl

use warnings;
use strict;
use CGI::Session;
use CGI;
use Net::LDAP;
use IO::Socket;
use IO::Socket::INET;
use Net::SSH::Perl; 
my $q = new CGI;
my $dn;
my $ip='172.20.1.117';
my $session = CGI::Session->load() or die "there is no session";
my $nameUser=$session->param('userName');
my $password=$session->param('password');
if($session->is_expired() or $session->is_empty()){
	print $q->redirect("http://".$ip."/index.html");
}else{
       my $ssh = Net::SSH::Perl->new("172.20.1.117",debug=>1,protocol=>2,port=>2777);
       $ssh->login($nameUser, $password);
       $ssh->cmd("mv /home/".$nameUser."/public_html/.htaccess.deny  /home/".$nameUser."/public_html/.htaccess");
       $ssh->cmd("exit");

}

printf $q->header();
