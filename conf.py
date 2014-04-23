#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#  kirmah/conf.py
#  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#  software  : Kirmah    <http://kirmah.sourceforge.net/>
#  version   : 2.18
#  date      : 2013
#  licence   : GPLv3.0   <http://www.gnu.org/licenses/>
#  author    : a-Sansara <[a-sansara]at[clochardprod]dot[net]>
#  copyright : pluie.org <http://www.pluie.org/>
#
#  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#  This file is part of Kirmah.
#
#  Kirmah is free software (free as in speech) : you can redistribute it
#  and/or modify it under the terms of the GNU General Public License as
#  published by the Free Software Foundation, either version 3 of the License,
#  or (at your option) any later version.
#
#  Kirmah is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Kirmah.  If not, see <http://www.gnu.org/licenses/>.
#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~ module conf ~~

from getpass          import getuser as getUserLogin
from os               import sep
from os.path          import dirname, realpath, isdir, join

PRG_NAME            = 'Kirmah'
PRG_PACKAGE         = PRG_NAME.lower()
PRG_SCRIPT          = PRG_NAME.lower()
PRG_CLI_NAME        = PRG_SCRIPT+'-cli'
PRG_VERS            = '2.18'
PRG_AUTHOR          = 'a-Sansara'
PRG_COPY            = 'pluie.org'
PRG_YEAR            = '2013'
PRG_WEBSITE         = 'http://kirmah.sourceforge.net'
PRG_LICENSE         = 'GNU GPL v3'
PRG_RESOURCES_PATH  = '/usr/share/'+PRG_PACKAGE+sep
if not isdir(PRG_RESOURCES_PATH):
    PRG_RESOURCES_PATH = dirname(dirname(realpath(__file__)))+sep+'resources'+sep+PRG_PACKAGE+sep
print(PRG_RESOURCES_PATH)
PRG_GLADE_PATH      = PRG_RESOURCES_PATH+'glade'+sep+PRG_PACKAGE+'.glade'
PRG_LICENSE_PATH    = PRG_RESOURCES_PATH+'/LICENSE'
PRG_LOGO_PATH       = join(PRG_RESOURCES_PATH,'..'+sep,'pixmaps'+sep,PRG_PACKAGE+sep,PRG_PACKAGE+'.png')
PRG_LOGO_ICON_PATH  = join(PRG_RESOURCES_PATH,'..'+sep,'pixmaps'+sep,PRG_PACKAGE+sep,PRG_PACKAGE+'_ico.png')
PRG_ABOUT_LOGO_SIZE = 160
PRG_ABOUT_COPYRIGHT = '(c) '+PRG_AUTHOR+' - '+PRG_COPY+' '+PRG_YEAR
PRG_ABOUT_COMMENTS  = ''.join(['Kirmah simply encrypt/decrypt files','\n', 'license ',PRG_LICENSE])
PRG_DESC            = """
  Encryption with symmetric-key algorithm Kirmah.

  three modes are available to encrypt :

    - compression (full / disabled or only final step)
    - random (simulate a random order - based on crypted key - to randomize data)
    - mix (mix data according to a generated map - based on crypted key - with addition of noise)


  Process is as follow :

  for encryption :
    file > [ compression > ] encryption > [randomiz data > mix data > compression > ] file.kmh

    default options depends on file type (binary or text).
      - binary files are compressed only at the end of process
      - text files have a full compression mode
      - random and mix modes are enabled on all files

  for decryption :
    file.kmh > [ uncompression > unmix data > unrandomiz data] > decryption > [uncompression > ] file


  multiprocessing is avalaible for reducing encryption/decryption time.


  for encrypt large binary files, a fastest alternative is possible :
  the split command.

  the split command consist on splitting file into severals parts (with noise addition) according to
  a generated map based on the crypted key.
  the map is fully encrypted as a configuration file (.kcf) which is required to merge all parts

  the merge command is the opposite process.
"""


DEFVAL_NPROC        = 2
DEFVAL_NPROC_MAX    = 8
DEFVAL_NPROC_MIN    = 2
DEFVAL_COMP         = False
DEFVAL_ENCMODE      = True
DEFVAL_MIXMODE      = True
DEFVAL_RANDOMMODE   = True
DEFVAL_USER_PATH    = ''.join([sep,'home',sep,getUserLogin(),sep])
DEFVAL_UKEY_PATH    = ''.join([DEFVAL_USER_PATH, '.', PRG_PACKAGE,sep])
DEFVAL_UKEY_NAME    = '.default.key'
DEFVAL_UKEY_LENGHT  = 1024
DEFVAL_CRYPT_EXT    = '.kmh'

DEBUG               = True
UI_TRACE            = True
PCOLOR              = True

GUI_LABEL_PROCEED   = 'Proceed'
GUI_LABEL_OK        = 'OK'
GUI_LABEL_CANCEL    = 'Cancel'

def redefinePaths(path):

    PRG_GLADE_PATH      = path+PRG_PACKAGE+sep+'glade'+sep+PRG_PACKAGE+'.glade'
    PRG_LICENSE_PATH    = path+PRG_PACKAGE+sep+'LICENSE'
    PRG_LOGO_PATH       = path+'pixmaps'+sep+PRG_PACKAGE+sep+PRG_PACKAGE+'.png'
    PRG_LOGO_ICON_PATH  = path+'pixmaps'+sep+PRG_PACKAGE+sep+PRG_PACKAGE+'_ico.png'
