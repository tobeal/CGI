#!/usr/bin/perl

#Wordpress config

use DBI;


print "----------------------------------------------------------------------------------------" . "\n";

my $db_id="wordpress_" . int(rand(10000));

print $db_id . "\n";

my $dbh = DBI->connect("DBI:mysql:host=localhost;port=3306", "root", "RoMon07");
$dbh->do("create database " . $db_id) or die "Cannot create database \n ";
$dbh->do("create user " . $db_id . "@localhost identified by 'wps';") or die "Cannot create user \n ";
$dbh->do("grant all privileges on " . $db_id . ".* to " . $db_id) or die "Cannot grant privileges \n ";
$dbh->do("flush privileges") or die "Error \n ";

my $ruta ="/home/usuarioprueba";
my $filename = $ruta . "/public_html/wordpress/wp-config.php";

open(FILE, "<" . $filename) || die "File not found";
my @lines = <FILE>;
close(FILE);

my @newlines;
foreach(@lines) {
   $_ =~ s/database_name_here/$db_id/g;
   $_ =~ s/username_here/$db_id/g;
   $_ =~ s/password_here/wps/g;
   push(@newlines,$_);
}

open(FILE, ">" . $filename) || die "File not found";
print FILE @newlines;
close(FILE);
