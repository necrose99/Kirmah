#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#  kirmah/cliapp.py
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
# ~~ module cliapp ~~

import  kirmah.conf     as conf
from    kirmah.crypt    import KirmahHeader, Kirmah, BadKeyException, represents_int, KeyGen
from    psr.sys         import Sys, Const, Io
from    psr.log         import Log
import  tarfile

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~ class CliApp ~~

class CliApp:

    @Log(Const.LOG_BUILD)
    def __init__(self, home, path, parser, a, o):
        """"""
        self.parser = parser
        self.a      = a
        self.o      = o
        self.home   = home
        self.stime  = Sys.datetime.now()
        if not self.o.keyfile :
            self.o.keyfile = self.home+'.kirmah'+Sys.sep+'.default.key'


    @Log(Const.LOG_DEBUG)
    def onCommandKey(self):
        """"""
        if int(self.o.length) >= 128 and int(self.o.length) <= 4096 :
            self.parser.print_header()
            if not self.o.outputfile : self.o.outputfile = self.home+'.kirmah'+Sys.sep+'.default.key'
            kg   = KeyGen(int(self.o.length))
            done = True
            if Io.file_exists(self.o.outputfile) and not self.o.force :

                Sys.pwarn((('the key file ',(self.o.outputfile, Sys.Clz.fgb3), ' already exists !'),
                           'if you rewrite this file, all previous files encrypted with the corresponding key will be unrecoverable !'))

                done   = Sys.pask('Are you sure to rewrite this file')
                self.stime  = Sys.datetime.now()
            if done :
                Io.set_data(self.o.outputfile, kg.key)
            Sys.pstep('Generate key file', self.stime, done)

            if done :
                Sys.print(' '*5+Sys.realpath(self.o.outputfile), Sys.Clz.fgB1, True)

        else :
            self.parser.error_cmd((('invalid option ',('-l, --length', Sys.Clz.fgb3), ' value (', ('128',Sys.Clz.fgb3),' to ', ('4096',Sys.Clz.fgb3),')'),))


    @Log(Const.LOG_DEBUG)
    def onCommandEnc(self):
        """"""
        done   = True
        if self.o.outputfile is None :
            self.o.outputfile = Sys.basename(self.a[1])
        if self.o.outputfile[-len(Kirmah.EXT):] != Kirmah.EXT :
            print(self.o.outputfile[-len(Kirmah.EXT):])
            self.o.outputfile += Kirmah.EXT
        print(self.o.outputfile)

        d        = self.getDefaultOption((self.o.compress,self.o.fullcompress,self.o.nocompress))
        compress = (KirmahHeader.COMP_END if d == 0 or (d is None and Io.is_binary(self.a[1])) else (KirmahHeader.COMP_ALL if d==1 or d is None else KirmahHeader.COMP_NONE))
        random   = True if (self.o.random is None and self.o.norandom is None) or self.o.random else False
        mix      = True if (self.o.mix is None and self.o.nomix is None) or self.o.mix else False

        if (self.o.multiprocess is not None and not represents_int(self.o.multiprocess)) or (not self.o.multiprocess is None and not(int(self.o.multiprocess)>=2 and int(self.o.multiprocess) <=8)) :
            self.parser.error_cmd((('invalid option ',('-j, --multiprocess', Sys.Clz.fgb3), ' value (', ('2',Sys.Clz.fgb3),' to ', ('8',Sys.Clz.fgb3),')'),))

        nproc = int(self.o.multiprocess) if not self.o.multiprocess is None and int(self.o.multiprocess)>=2 and int(self.o.multiprocess) <=8 else 1

        if not Sys.g.QUIET : self.parser.print_header()

        if Io.file_exists(self.o.outputfile) and not self.o.force:
            Sys.pwarn((('the file ',(self.o.outputfile, Sys.Clz.fgb3), ' already exists !'),))
            done  = Sys.pask('Are you sure to rewrite this file')
            self.stime = Sys.datetime.now()

        if done :

            try :
                Sys.ptask()

                key    = Io.get_data(self.o.keyfile)
                km     = Kirmah(key, None, compress, random, mix)

                km.encrypt(self.a[1], self.o.outputfile, nproc)

            except Exception as e :
                done = False
                print(e)
                raise e
                pass

        if not Sys.g.QUIET :
            self.onend_cmd('Kirmah Encrypt', self.stime, done, self.o.outputfile)


    @Log(Const.LOG_DEBUG)
    def onCommandDec(self):
        """"""
        done  = True
        if self.o.outputfile is None :
            self.o.outputfile = self.a[1][:-4] if self.a[1][-4:] == Kirmah.EXT else self.a[1]

        if not Sys.g.QUIET : self.parser.print_header()

        if Io.file_exists(self.o.outputfile) and not self.o.force:
            Sys.pwarn((('the file ',(self.o.outputfile, Sys.Clz.fgb3), ' already exists !'),))
            done  = Sys.pask('Are you sure to rewrite this file')
            self.stime = Sys.datetime.now()

        if done :

            try :

                if (self.o.multiprocess is not None and not represents_int(self.o.multiprocess)) or (not self.o.multiprocess is None and not(int(self.o.multiprocess)>=2 and int(self.o.multiprocess) <=8)) :
                    self.parser.error_cmd((('invalid option ',('-j, --multiprocess', Sys.Clz.fgb3), ' value (', ('2',Sys.Clz.fgb3),' to ', ('8',Sys.Clz.fgb3),')'),))

                nproc = int(self.o.multiprocess) if not self.o.multiprocess is None and int(self.o.multiprocess)>=2 and int(self.o.multiprocess) <=8 else 1

                Sys.ptask()

                key    = Io.get_data(self.o.keyfile)
                km     = Kirmah(key)

                km.decrypt(self.a[1], self.o.outputfile, nproc)

            except BadKeyException:
                done = False
                Sys.pwarn((('BadKeyException : ',('wrong key ',Sys.CLZ_WARN_PARAM), ' !'),), False)

        if not Sys.g.QUIET :
            self.onend_cmd('Kirmah Decrypt', self.stime, done, self.o.outputfile)


    @Log(Const.LOG_DEBUG)
    def onCommandSplit(self):
        """"""
        done  = True
        Sys.cli_emit_progress(1)
        if not self.o.parts is None and not(int(self.o.parts)>=12 and int(self.o.parts) <=62) :
            self.parser.error_cmd((('invalid option ',('-p, --parts', Sys.Clz.fgb3), ' value (', ('12',Sys.Clz.fgb3),' to ', ('62',Sys.Clz.fgb3),')'),))
        else : self.o.parts = int(self.o.parts)

        if not Sys.g.QUIET : self.parser.print_header()
        if self.o.outputfile is not None :
            if self.o.outputfile[-5:]!='.tark' : self.o.outputfile += '.tark'
            if Io.file_exists(self.o.outputfile) and not self.o.force:
                Sys.pwarn((('the file ',(self.o.outputfile, Sys.Clz.fgb3), ' already exists !'),))
                done  = Sys.pask('Are you sure to rewrite this file')
                self.stime = Sys.datetime.now()

        if done :

            try :
                Sys.ptask()
                Sys.cli_emit_progress(2)
                key    = Io.get_data(self.o.keyfile)
                km     = Kirmah(key)
                hlst   = km.ck.getHashList(Sys.basename(self.a[1]), self.o.parts, True)
                Sys.cli_emit_progress(3)
                kcf    = km.splitFile(self.a[1], hlst)
                t      = int(Sys.time())
                times  = (t,t)
                p      = 85
                Sys.cli_emit_progress(p)
                Io.touch(kcf, times)
                frav = 0.24
                for row in hlst['data']:
                    p += frav
                    Io.touch(row[1]+km.EXT,times)
                    Sys.cli_emit_progress(p)
                if self.o.outputfile is not None :
                    d = Sys.datetime.now()
                    if Sys.g.DEBUG : Sys.wlog(Sys.dprint())
                    Sys.ptask('Preparing tark file')
                    hlst['data'] = sorted(hlst['data'], key=lambda lst: lst[4])
                    with tarfile.open(self.o.outputfile, mode='w') as tar:
                        tar.add(kcf, arcname=Sys.basename(kcf))
                        p    = 90
                        for row in hlst['data']:
                            tar.add(row[1]+km.EXT, arcname=Sys.basename(row[1]+km.EXT))
                            p += frav
                            Sys.cli_emit_progress(p)
                    Sys.pstep('Packing destination file', d, True)
                    d = Sys.datetime.now()
                    Sys.ptask('Finalize')
                    for row in hlst['data']:
                        Io.removeFile(row[1]+km.EXT)
                        p += frav
                        Sys.cli_emit_progress(p)
                    Io.removeFile(kcf)
                    Sys.pstep('Cleaning', d, True)

            except Exception as e :
                done = False
                if Sys.g.DEBUG :
                    print('split exception')
                    print(e)

                    #~ raise e
                elif not Sys.g.QUIET :
                    Sys.pwarn((str(e),))

        if not Sys.g.QUIET:
            Sys.cli_emit_progress(100)
            self.onend_cmd('Kirmah Split', self.stime, done, self.o.outputfile)



    @Log(Const.LOG_DEBUG)
    def onCommandMerge(self):
        """"""
        done   = True

        if not Sys.g.QUIET : self.parser.print_header()

        if done :
            toPath = None
            try :
                Sys.ptask()

                key    = Io.get_data(self.o.keyfile)
                km     = Kirmah(key)
                kcf    = None
                istar  = True
                try:
                    import tarfile
                    dpath = Sys.dirname(Sys.realpath(self.o.outputfile))+Sys.sep if self.o.outputfile is not None else Sys.dirname(Sys.realpath(self.a[1]))+Sys.sep
                    if self.o.outputfile is None :
                        self.o.outputfile = dpath
                    with tarfile.open(self.a[1], mode='r') as tar:
                        #~ print(dpath)
                        tar.extractall(path=dpath)
                        kcf = None
                        for tarinfo in tar:
                            #~ print(tarinfo.name)
                            if tarinfo.isreg() and tarinfo.name[-4:]=='.kcf':
                                #~ print(dpath+tarinfo.name)
                                kcf = dpath+tarinfo.name
                    if kcf is not None :
                        km.DIR_OUTBOX = dpath
                        toPath = km.mergeFile(kcf, self.o.outputfile)
                except BadKeyException:
                    Sys.pwarn((('BadKeyException : ',('wrong key ',Sys.CLZ_WARN_PARAM), ' !'),), False)
                    done = False

                except Exception :
                    istar  = False
                    toPath = km.mergeFile(self.a[1], self.o.outputfile)

                #~ if self.o.outputfile is not None :
                #~ Io.rename(toPath, self.o.outputfile)
                #~ toPath = self.o.outputfile

            except BadKeyException:
                Sys.pwarn((('BadKeyException : ',('wrong key ',Sys.CLZ_WARN_PARAM), ' !'),), False)
                done = False

            except Exception as e :
                done = False
                if Sys.g.DEBUG :
                    print(e)
                elif not Sys.g.QUIET :
                    Sys.pwarn((str(e),))
        if not done :
            if istar :
                with tarfile.open(self.a[1], mode='r') as tar:
                    for tarinfo in tar:
                        Sys.removeFile(dpath+tarinfo.name)

        if not Sys.g.QUIET :
            self.onend_cmd('Kirmah Merge', self.stime, done, toPath)


    @Log(Const.LOG_ALL)
    def getDefaultOption(self, args):
        """"""
        c = None
        for i, a in enumerate(args) :
            if a :
                c = i
                break
        return c


    @Log(Const.LOG_DEBUG)
    def onend_cmd(self, title, stime, done, outputfile):
        """"""
        s = Const.LINE_SEP_CHAR*Const.LINE_SEP_LEN
        Sys.print(s, Sys.CLZ_HEAD_LINE)
        Sys.wlog([(s, Const.CLZ_HEAD_SEP)])
        Sys.pstep(title, stime, done, True)
        Sys.print(s, Sys.CLZ_HEAD_LINE)
        Sys.wlog([(s, Const.CLZ_HEAD_SEP)])
        if done and outputfile is not None:
            Sys.cli_emit_progress(100)
            Sys.print(' '*5+Sys.realpath(outputfile), Sys.Clz.fgB1, False)
            Sys.print(' ('+Sys.getFileSize(outputfile)+')', Sys.Clz.fgB3)
            bdata = [(' '*5+Sys.realpath(outputfile), 'io'),(' ('+Sys.getFileSize(outputfile)+')','func')]
            Sys.wlog(bdata)
            Sys.wlog(Sys.dprint())
