#!/usr/bin/perl


use DBI;
use warnings;
use File::Path qw(make_path remove_tree);
use strict;
use CGI;
use Quota;
use Net::LDAP;
use IO::Socket;
use IO::Socket::INET;
use open qw( :encoding(UTF-8) :std ); 
use Net::SSH::Perl;
my $q = new CGI;

my $nameUser;
my $password;
my $email;
my $name;
my $lastName;
my $address;
my $gidNumber;
my $qInfo;
my $ip='172.20.1.117';
my $inf= $q->param('codigoVerif');
my @valores = split('_',$inf);
my $user = $valores[1]; 

my $dsn='DBI:mysql:usuarios:localhost';
my $username='usersql';
my $passwd='qwer1234';


my $dbh=DBI->connect($dsn,$username,$passwd) or die "ERROR en la conexion a la base de datos";


my $select = " SELECT nombreUsuario,passwd,nombre,apellido,postal,email,gidnumber from usuario WHERE nombreUsuario=\"$user\"";

my $sth = $dbh->prepare($select);
$sth->execute();
$qInfo = $sth ->fetchrow_arrayref() or undef;

if( not defined $qInfo ){

	die "bad verification";
} 

$nameUser = $qInfo->[0];
$password = $qInfo->[1];
$name = $qInfo->[2];
$lastName = $qInfo->[3];
$address = $qInfo->[4];
$email = $qInfo->[5];
$gidNumber = $qInfo->[6];

$sth->finish();
$dbh->disconnect();







my $ldapconnect = Net::LDAP->new( "127.0.0.1", version => 3, port => 389 );



my $bind = $ldapconnect->bind( "cn=admin,dc=127,dc=0,dc=0,dc=1",
    password => "RoMon07" );
if ( $bind->code ) {
      printf "Content-type: text/html\n\n";
     printf "hello there12";


}

 my $uids = $ldapconnect->search(
                        base => "ou=People,dc=127,dc=0,dc=0,dc=1",
                        scope => "sub",
                        filter => "uidNumber=*", 
                        attrs   => [ 'uidNumber' ],
                        );
        my @uids;
        if ($uids->count > 0) {
                foreach my $uid ($uids->all_entries) {
                        push @uids, $uid->get_value('uidNumber');
                }
        }       
        
        @uids = sort { $b <=> $a } @uids;

        my $high = $uids[0];
	my $uidNumber=++$high;
       
my $result = $ldapconnect->add("uid=". $nameUser .",ou=People,dc=127,dc=0,dc=0,dc=1", 
                attr => [ 'cn' => $nameUser ,
                          'sn' => $lastName ,
                          'uid' => $nameUser ,
			  'loginShell' => '/bin/bash',
			  'gidNumber' => $gidNumber ,
			  'uidNumber' => $uidNumber ,
			  'homeDirectory' => '/home/'.$nameUser ,
			  'givenName' => $name , 
                          'userPassword' => $password ,
                          'mail' => $email,
			  'street' => $address,
			  'objectclass' => ['person','inetOrgPerson','posixAccount','shadowAccount'], 
                        ]
		              );


if ( $result->code!=0 ) {
        printf $q->redirect("http://127.0.0.1/registration.html");

}else{
	printf $uidNumber;
	Quota::setqlim('/dev/sda5',$uidNumber,50000,600000,0,0,0,0);
	#Connect
       my $ssh = Net::SSH::Perl->new($ip,debug=>1,protocol=>2,port=>2777);
       $ssh->login($nameUser, $password);
       $ssh->cmd("chmod 777 /home/$nameUser/public_html/blogUsers/fp-content");
       $ssh->cmd("exit");





	printf $q->redirect("http://127.0.0.1/index.html");
}
print $q->header;
