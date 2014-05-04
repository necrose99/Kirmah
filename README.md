Kirmah
======

{{{----Necrose99---With My Curriousity over Crypto Systems---I figgured it worth a look so I cloned it to Github---}}}
{{{----SF is good but makes it hard to tinker with stuff or contribute back or like. --}}}
{{{----Add in known  Crypto  IE PKI and Py-Bcrpt for streaching keys and protecting the symetric key from party A to Party B it shows promis.  --}}}

Encryption with symmetric-key algorithm Kirmah
http://sourceforge.net/projects/kirmah/?source=directory

Brought to you by: a-sansara (http://sourceforge.net/u/a-sansara/)
http://sourceforge.net/projects/kirmah
Description
 <br><a
href="http://a.fsdn.com/con/app/proj/kirmah/screenshots/kirmahpsgui.png/182/137"><img
alt=""
src="http://a.fsdn.com/con/app/proj/kirmah/screenshots/kirmahpsgui.png"
border="2" height="205" width="390"></a> <a
href="http://a.fsdn.com/con/app/proj/kirmah/screenshots/kirmahpsgui3.png/182/137"><img
alt=""
src="http://a.fsdn.com/con/app/proj/kirmah/screenshots/kirmahpsgui3.png/182/137"
border="2" height="205" width="272"></a><img alt=""
src="http://a.fsdn.com/con/app/proj/kirmah/screenshots/kirmahpsgui2.png"
height="205" width="392"><br>
<br>
<a
href="http://a.fsdn.com/con/app/proj/kirmah/screenshots/kmhgui4.png"><img
alt=""
src="http://a.fsdn.com/con/app/proj/kirmah/screenshots/kmhgui4.png"
border="2" height="205" width="246"></a><a
href="http://a.fsdn.com/con/app/proj/kirmah/screenshots/kirmah-cli_1.png"><img
alt=""
src="http://a.fsdn.com/con/app/proj/kirmah/screenshots/kirmah-cli_1.png"
border="2" height="205" width="294"></a><a
href="http://a.fsdn.com/con/app/proj/kirmah/screenshots/kirmah-cli_2.png"><img
alt=""
src="http://a.fsdn.com/con/app/proj/kirmah/screenshots/kirmah-cli_2.png"
border="0" height="205" width="323"></a><br>
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
