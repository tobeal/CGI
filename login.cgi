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
my $nameUser=$q->param('userNameLog');
my $pass=$q->param('passLog');
my $dn;
my $ip='172.20.1.117';
my $ldap = Net::LDAP->new("127.0.0.1", version =>3, port=> 389);
my $mesg = $ldap->bind();

my $searchBase = "ou=People, dc=127,dc=0,dc=0,dc=1";

  $mesg = $ldap->search(base => $searchBase, filter => "uid=$nameUser" );
     
    my $entry = $mesg->shift_entry;
     
    if ($entry)
    {
       $dn = $entry->dn;   
    }
    $ldap->unbind;

 $ldap = Net::LDAP->new("127.0.0.1", version =>3, port=> 389);
 $mesg = $ldap->bind($dn , password=> "$pass" ); 
 #informacion para el almacenamiento de la sesion del usuario
 my $session = new CGI::Session();
 my $CGISESSID = $session->id();
 print $session->header;
 $session->param('userName', $nameUser); 
 $session->param('password', $pass); 
 $session->expire('+1h');
 $session->flush();			

	if ( $mesg and $mesg->code() == 0 ) {
#Connect
	print $q->header;

	print "<form action=\"/index.html\" method=\"get\">";
   	print "<input type=\"submit\" value=\"Logueado de forma correcta,continuar\""; 
        print "name=\"Submit\" id=\"frm1_submit\" />";	
	print "</form>";
}

