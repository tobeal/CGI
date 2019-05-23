#!/usr/bin/perl


use strict;
use warnings;
use Archive::Tar;
use File::Find;


my $destino="/backup/copiaSeguridad.tar";
my @copias=('/home','/usr/lib/cgi-bin');

my @contenedor = ();

#con la siguiente funcion metemos en contenedor todo el contenido que haya en los directorios copias

find (sub {push @contenedor,$File::Find::name},@copias);

my $archivotar = Archive::Tar->new();

$archivotar->add_files(@contenedor);

$archivotar->write($destino,9);

