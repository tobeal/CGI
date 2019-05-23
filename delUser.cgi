#!/usr/bin/perl
use warnings;
use strict;
use CGI;
use CGI::Session;
use Net::LDAP;
use IO::Socket;
use IO::Socket::INET;
my $q = new CGI;
my $pass=$q->param('password');
my $pass2=$q->param('password2');
my $dn ;
my $session = CGI::Session->load() or die "there is no session";
my $nameUser=$session->param('userName');
my $ip='172.20.1.117';
print $q->header;
my $searchBase = "ou=People, dc=127,dc=0,dc=0,dc=1";
my $ldap = Net::LDAP->new("127.0.0.1", version =>3, port=> 389);
if($pass ne $pass2){
printf"Content-type: text/html\n\n";
printf"ERROR LAS PASSWORDS NO COINCIDEN";
}else{
my $mesg = $ldap->bind("cn=admin,dc=127,dc=0,dc=0,dc=1", password=> "RoMon07");
  $mesg = $ldap->search(base => $searchBase, filter => "uid=$nameUser" );
     
    my $entry = $mesg->shift_entry;
     
    if ($entry)
    {
       $dn = $entry->dn;
        $entry->dump;
    }

 $ldap->unbind();
$ldap = Net::LDAP->new("127.0.0.1", version =>3, port=> 389);
 $mesg = $ldap->bind($dn, password=> $pass );
if ( $mesg and $mesg->code() == 0 ){

     $ldap->unbind();        
     $ldap = Net::LDAP->new("127.0.0.1", version =>3, port=> 389);
     $mesg = $ldap->bind("cn=admin,dc=127,dc=0,dc=0,dc=1", password=> "RoMon07" );
     $mesg = $ldap->delete($dn);

	if ( $mesg and $mesg->code() == 0 ) {
	  print "<form action=\"/index.html\" method=\"get\">";
        print "<input type=\"submit\" value=\"Eliminado de forma correcta,pulse este boton\"";
        print   "name=\"Submit\" id=\"frm1_submit\" />";
        print   "</form>";
  
    		
   		$ldap->unbind();
	}else{ 
	  print "<form action=\"/index.html\" method=\"get\">";
        print "<input type=\"submit\" value=\"Eliminado de forma correcta,pulse este boton\"";
        print   "name=\"Submit\" id=\"frm1_submit\" />";
        print   "</form>";
	my $session = CGI::Session->load() or die "there is no session";

	my $result=$session->delete();
	printf $q->redirect("http://".$ip);
	printf $q->header();


	
		
 	        $ldap->unbind();
	}   

 
}else{
   $ldap->unbind();
 
}
}
