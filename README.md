Kirmah
======

{{{----Necrose99---With My Curriousity over Crypto Systems---I figgured it worth a look so I cloned it to Github---}}}


Encryption with symmetric-key algorithm Kirmah
http://sourceforge.net/projects/kirmah/?source=directory

Brought to you by: a-sansara (http://sourceforge.net/u/a-sansara/)
http://sourceforge.net/projects/kirmah
Description
Encryption with symmetric-key algorithm Kirmah

- generate keys with exotic chars
- redefine key length
- key mark to ensure decryption capabilities
- mix data
- fast with multiprocessing
- possible compression
- gui on gtk3
- cli tool
- python3

DEPENDENCIES :
========
python3, python-gobject, gobject-introspection, pygtk


3 modes are available to encrypt :
========
- compression (full / disabled or only final step)
- random (simulate a random order - based on crypted key - to randomize data)
- mix (mix data according to a generated map - based on crypted key - with addition of noise)

Process is as follow :
========
encrypt :
file > [ compress > ] encrypt > [randomiz data > mix data > compress > ] file.kmh

decrypt:
file.kmh > [ uncompress > unmix data > unrandomiz data] > decrypt > [uncompress > ] file

========
for encrypt/decrypt large binary files, use the fastest alternative : split/merge
