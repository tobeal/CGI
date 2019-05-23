#!/usr/bin/perl


use DBI;
use warnings;
use File::Path qw(make_path remove_tree);
use strict;
use CGI;
use Net::LDAP;
use IO::Socket;
use IO::Socket::INET;
use Email::Send::SMTP::Gmail;

my $q = new CGI;
my $nameUser = $q->param('userName');
my $password = $q->param('pass');
my $password2 = $q->param('pass2');
my $email = $q->param('email');
my $name = $q->param('name');
my $lastName = $q->param('lastName');
my $address = $q->param('postal');
my $gidNumber = $q->param('grupo');
my $ip='172.20.1.117';

if(not defined $nameUser or not defined $password or not defined $password2 or not defined $email or not defined $name or not defined $lastName or not defined $address or not defined $gidNumber or
 $nameUser eq "root"){

die "ERROR datos no introducidos correctamente o intento de registro con root";

}

if($password ne $password2){
        print "<h1>Por favor introduzca en los dos casos la misma clave</h1>";
        print "<input type='button' value=>'De acuerdo' .".".onclick='javascript:history.back(1)'>";
        exit;

}



my $dsn ='DBI:mysql:usuarios:localhost';
my $username='usersql';
my $passwd='qwer1234';

my $dbh= DBI->connect($dsn,$username,$passwd) or die "ERROR en la conexion a la base de datos";

my $sth = $dbh->prepare("insert into usuario(nombreUsuario,passwd,nombre,apellido,postal,email,gidnumber) values (?,?,?,?,?,?,?)");

$sth->execute ($nameUser,$password,$name,$lastName,$address,$email,$gidNumber);

$dbh->disconnect();

my $message="http://$ip/cgi-bin/addUser.cgi?codigoVerif=Se11Jr13a97_$nameUser";

my ($mail,$error)=Email::Send::SMTP::Gmail->new( -smtp=>'smtp.gmail.com',
						 -login=>'serllito1113@gmail.com',
						 -pass=>'ukstssoazlsuevoo',
						 -layer=>'ssl');

$mail->send(-to=>$email ,-subject=>'Confirmar registro de usuario',-body=>$message);


$mail->bye;


print $q->redirect("http://".$ip."/index.html");
