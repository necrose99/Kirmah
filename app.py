#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#  kirmah.app.py
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
# ~~ module app ~~

from os.path                    import splitext
from threading                  import Thread, Timer, Event, get_ident, enumerate as thread_enum, current_thread
from kirmah                     import conf
from kirmah.crypt               import KeyGen, Kirmah, KirmahHeader
from psr.sys                    import Sys, Io, Const, init
from psr.log                    import Log


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~ class KirmahApp ~~

class KirmahApp:

    @Log(Const.LOG_BUILD)
    def __init__(self, debug=True, color=True, loglvl=Const.LOG_DEFAULT):
        """"""
        self.encmode         = conf.DEFVAL_ENCMODE
        self.splitmode       = False
        self.compression     = conf.DEFVAL_COMP
        self.mix             = conf.DEFVAL_MIXMODE
        self.random          = conf.DEFVAL_RANDOMMODE
        self.nproc           = conf.DEFVAL_NPROC
        self.src             = None
        self.dst             = None
        self.kpath           = None
        Sys.g.GUI            = True
        init(conf.PRG_NAME, debug, Sys.getpid(), color, loglvl)


    @Log(Const.LOG_DEBUG)
    def getDefaultKeyPath(self):
        """"""
        return conf.DEFVAL_UKEY_PATH+conf.DEFVAL_UKEY_NAME


    @Log(Const.LOG_DEBUG)
    def createDefaultKeyIfNone(self):
        """"""
        kpath = self.getDefaultKeyPath()
        if not Io.file_exists(kpath):
            if Sys.isUnix() :
                if not Sys.isdir(conf.DEFVAL_UKEY_PATH) :
                    Sys.mkdir_p(conf.DEFVAL_UKEY_PATH)
                    Io.set_data(kpath, KeyGen(conf.DEFVAL_UKEY_LENGHT).key)
        self.selectKey(kpath)


    @Log(Const.LOG_DEBUG)
    def createNewKey(self, filename, size):
        """"""
        if not Sys.isdir(Sys.dirname(filename)):
            Sys.mkdir_p(Sys.dirname(filename))
        Io.set_data(filename,KeyGen(size).key[:size])


    @Log(Const.LOG_DEBUG)
    def getKeyInfos(self, filename=None):
        """"""
        if filename is None : filename = self.getDefaultKeyPath()
        if not Io.file_exists(filename):
            raise FileNotFoundException(filename)
        k = Io.get_data(filename)
        s = len(k)
        m = KeyGen(s).getMark(k)
        return k, s, m


    @Log(Const.LOG_DEBUG)
    def selectKey(self, filename):
        """"""
        if not Io.file_exists(filename):
            raise FileNotFoundException(filename)
        self.kpath = filename


    @Log(Const.LOG_DEBUG)
    def setCompression(self, value=1):
        """"""
        self.compression = value


    @Log(Const.LOG_DEBUG)
    def setMixMode(self, enable=True):
        """"""
        self.mix = enable


    @Log(Const.LOG_DEBUG)
    def setRandomMode(self, enable=True):
        """"""
        self.random = enable


    @Log(Const.LOG_DEBUG)
    def setMultiprocessing(self, nproc):
        """"""
        # disable
        if nproc is None or nproc is False or nproc < conf.DEFVAL_NPROC_MIN :
            self.nproc = 0
        # enable
        else :
            self.nproc = nproc if nproc <= conf.DEFVAL_NPROC_MAX else conf.DEFVAL_NPROC_MAX


    @Log(Const.LOG_DEBUG)
    def switchEncMode(self, isEnc=True):
        """"""
        self.encmode = isEnc


    @Log(Const.LOG_DEBUG)
    def switchFormatMode(self, isTxt=True):
        self.splitmode = not isTxt


    @Log(Const.LOG_DEBUG)
    def setSourceFile(self, filename):
        """"""
        if not Io.file_exists(filename) :
            raise FileNotFoundException()
        else :
            self.src = filename


    @Log(Const.LOG_DEBUG)
    def hasSrcFile(self):
        """"""
        return Io.file_exists(self.src)


    @Log(Const.LOG_DEBUG)
    def setDestFile(self, path):
        """"""
        if path is not None :
            self.dst = ''.join([path, Sys.sep, '' if self.src is None else Sys.basename(self.src)])
            if self.encmode:
                self.dst = ''.join([self.dst, Kirmah.EXT if not self.splitmode else Kirmah.EXT_TARK])
            else :
                self.dst, ext = Sys.getFileExt(self.dst)
                if not ext == (Kirmah.EXT if not self.splitmode else Kirmah.EXT_TARK):
                    self.dst += ext
            #~ if Io.file_exists(self.dst):
                #~ raise FileNeedOverwriteException(self.dst)
        else : self.dst = None


    @Log(Const.LOG_DEFAULT)
    def getCall(self):
        q      = ''
        action = ('enc' if self.encmode else 'dec') if not self.splitmode else ('split' if self.encmode else 'merge')
        comp   = '-a'   if self.compression==1 else ('-z' if self.compression==2 else '-Z')
        mproc  = ''     if self.nproc==0 or self.splitmode else '-j'+str(self.nproc)
        rmode  = '-r'   if self.random else '-R '
        mmode  = '-m'   if self.mix else '-M'
        debug  = '-fd'  if Sys.g.DEBUG else '-f'
        key    = '-k'+q+self.kpath+q if self.kpath != self.getDefaultKeyPath() else ''
        #~ q      = '"'
        call   = ['kirmah-cli.py',debug, action,q+self.src+q,comp,mproc,rmode,mmode,'-o',q+self.dst+q,key]
        print('python '+(' '.join(call)))
        return call


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~ class FileNotFoundException ~~

class FileNotFoundException(BaseException):
    """"""

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~ class FileNeedOverwriteException ~~

class FileNeedOverwriteException(BaseException):
    """"""
