#!/usr/bin/perl

use warnings;
use strict;
use CGI::Session;
use CGI;
use CGI::Session;
use Net::LDAP;
use IO::Socket;
use IO::Socket::INET;
my $q = new CGI;
my $pass=$q->param('pass');
my $pass2=$q->param('pass2');
my $email=$q->param('email');
my $name=$q->param('name');
my $lastName=$q->param('lastName');
my $address=$q->param('postalAddress');
my $dn;
my $ip='172.20.1.117';
my $ldap = Net::LDAP->new("127.0.0.1", version =>3, port=> 389);
my $session = CGI::Session->load() or die "there is no session";
my $nameUser=$session->param('userName');


if($pass ne $pass2){
print "Content-type: text/html\n\n";	
printf "ERROR PASSWORD NO COINCIDEN";
}else{
my $mesg = $ldap->bind("cn=admin,dc=127,dc=0,dc=0,dc=1", password=> "RoMon07" );
my $searchBase = "ou=People,dc=127,dc=0,dc=0,dc=1";
  $mesg = $ldap->search(base => $searchBase, filter => "uid=$nameUser" );
     
    my $entry = $mesg->shift_entry;
     
    if ($entry)
    {
       $dn = $entry->dn;
        #$entry->dump;
    }
    
    
$mesg = $ldap->modify( $dn, replace => { 'cn'=>$name,'sn'=>$lastName,'givenName'=>$name,'mail' => $email,'street'=>$address } );


if ( $mesg and $mesg->code() == 0 ) {
          print $q->redirect("http://".$ip."/index.html");
}else{
        print $q->redirect("http://".$ip."/updateUser.html");
}

}
printf $q->header();
