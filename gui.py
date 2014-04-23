#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#  kirmah.gui.py
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
# ~~ module gui ~~

from gi.repository    import Gtk, GObject, GLib, Gdk, Pango
from os               import sep, remove
from os.path          import abspath, dirname, join, realpath, basename, getsize, isdir, splitext
from base64           import b64decode, b64encode
from time             import time, sleep
from getpass          import getuser as getUserLogin
from mmap             import mmap
from math             import ceil

from kirmah.crypt     import KeyGen, Kirmah, KirmahHeader, ConfigKey, BadKeyException, b2a_base64, a2b_base64, hash_sha256_file
from kirmah.app       import KirmahApp, FileNotFoundException, FileNeedOverwriteException
from kirmah.ui        import Gui, CliThread
from kirmah           import conf
from psr.sys          import Sys, Io, Const
from psr.log          import Log
from psr.mproc        import Manager
import pdb


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~ class AppGui ~~

class AppGui(Gui):

    DEFAULT_KEY     = 0
    EXISTING_KEY    = 1
    NEW_KEY         = 2

    IS_SOURCE_DEF   = False
    IS_DEST_DEF     = True

    MODE_CRYPT      = True
    COMPRESSION     = True
    NPROC           = 2
    PROCEED         = False

    curKey          = 0
    start           = False
    poslog          = 0


    @Log(Const.LOG_BUILD)
    def __init__(self, wname='window1'):
        """"""
        self.app = KirmahApp(conf.DEBUG, conf.PCOLOR)
        super().__init__(wname)


    @Log(Const.LOG_UI)
    def on_start(self):
        """"""
        self.app.createDefaultKeyIfNone()
        key, size, mark = self.app.getKeyInfos()

        self.curKey = self.DEFAULT_KEY
        self.get('filechooserbutton1').set_filename(self.app.getDefaultKeyPath())
        self.get('filechooserbutton3').set_current_folder(conf.DEFVAL_USER_PATH)
        devPath = '/home/dev/git_repos/kirmah2.15/'
        #~ self.get('filechooserbutton3').set_current_folder(devPath)
        self.get('checkbutton1').set_active(conf.DEFVAL_NPROC>=2)
        self.get('checkbutton3').set_active(True)
        self.get('checkbutton4').set_active(True)
        self.get('spinbutton2').set_value(conf.DEFVAL_NPROC)
        if conf.DEFVAL_NPROC >= 2:
            self.disable('spinbutton2', False)
        self.get('checkbutton2').set_active(conf.DEFVAL_MIXMODE)
        self.get('checkbutton4').set_active(conf.DEFVAL_RANDOMMODE)
        self.get('entry1').set_text(mark)

        Sys.g.UI_AUTO_SCROLL = True
        self.textview    = self.get('textview1')
        self.textview.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 1.0))
        self.textview.modify_font(Pango.font_description_from_string ('DejaVu Sans Mono Book 11'))
        self.textbuffer  = self.textview.get_buffer()
        self.tags        = self.buildTxtTags(self.textbuffer)
        self.progressbar = self.get('progressbar1')
        cbt = self.get('comboboxtext1')
        cbt.connect("changed", self.on_compression_changed)
        tree_iter = cbt.get_model().get_iter_first()
        print(cbt.get_model().get_string_from_iter(tree_iter))
        tree_iter = cbt.get_model().get_iter_from_string('3')
        cbt.set_active_iter(tree_iter)
        cbt = self.get('comboboxtext2')
        cbt.connect("changed", self.on_logging_changed)
        tree_iter = cbt.get_model().get_iter_first()
        tree_iter = cbt.get_model().get_iter_from_string('4')
        cbt.set_active_iter(tree_iter)
        Sys.clear()
        Sys.dprint('INIT UI')
        self.start = True
        self.thkmh = None


    @Log(Const.LOG_UI)
    def launch_thread(self, *args):
        self.progressbar.show()
        def getKmhThread(on_completed, on_interrupted, on_progress, userData, *args):
            thread = CliThread(*args)
            thread.connect("completed"  , on_completed   , userData)
            thread.connect("interrupted", on_interrupted , userData)
            thread.connect("progress"   , on_progress    , userData)
            return thread
        cliargs = ['kirmah-cli.py', 'split', '-df', '/media/Hermes/webbakup/The Raven.avi', '-z', '-r', '-m', '-o', '/home/dev/git_repos/kirmah2.15/The Raven.avi.kmh']
        cliargs = self.app.getCall()
        self.thkmh = getKmhThread(self.thread_finished, self.thread_interrupted, self.thread_progress, None, cliargs, Sys.g.MPEVENT)
        self.thkmh.start()


    @Log(Const.LOG_UI)
    def on_mixdata_changed(self, checkbox):
        """"""
        self.app.setMixMode(not checkbox.get_active())
        if self.start: self.refreshProceed()


    @Log(Const.LOG_UI)
    def on_randomdata_changed(self, checkbox):
        """"""
        self.app.setRandomMode(not checkbox.get_active())
        if self.start: self.refreshProceed()


    @Log(Const.LOG_UI)
    def on_multiproc_changed(self, checkbox, data = None):
        """"""
        disabled = checkbox.get_active()
        self.disable('spinbutton2',disabled)
        self.app.setMultiprocessing(int(self.get('spinbutton2').get_value()) if not disabled else 0)
        if self.start: self.refreshProceed()


    @Log(Const.LOG_UI)
    def on_logging_changed(self, combo):
        """"""
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            v = combo.get_model()[tree_iter][:2][0]
            if v =='DISABLED' :
                Sys.g.DEBUG = False
            elif hasattr(Const, v):
                Sys.g.DEBUG = True
                exec('Sys.g.LOG_LEVEL = Const.'+v)
            else :
                Sys.g.LOG_LEVEL = Const.LOG_DEFAULT
        if self.start: self.refreshProceed()


    @Log(Const.LOG_DEFAULT)
    def on_compression_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter != None:
            model = combo.get_model()
            comp = KirmahHeader.COMP_END if  model[tree_iter][:2][0]=='yes' else (KirmahHeader.COMP_NONE if model[tree_iter][:2][0]=='no' else KirmahHeader.COMP_ALL)
            print(comp)
            self.app.setCompression(comp)
        if self.start: self.refreshProceed()


    @Log(Const.LOG_UI)
    def on_nproc_changed(self, spin):
        """"""
        self.app.setMultiprocessing(int(spin.get_value()))
        if self.start: self.refreshProceed()


    @Log(Const.LOG_UI)
    def on_keylen_changed(self, spin):
        """"""
        filename = self.get('filechooserbutton1').get_filename()
        if Io.file_exists(filename):
            self.app.createNewKey(filename, int(self.get('spinbutton1').get_value()))
            if self.start: self.refreshProceed()


    @Log(Const.LOG_UI)
    def on_new_file_key(self, fc):
        """"""
        filename = fc.get_filename()
        if self.curKey == self.NEW_KEY:
            self.app.createNewKey(filename, int(self.get('spinbutton1').get_value()))
        self.app.selectKey(filename)
        k, s, m = self.app.getKeyInfos(filename)
        self.get('spinbutton1').set_value(s)
        self.get('entry1').set_text(m)
        self.get('filechooserbutton1').set_filename(filename)
        if self.curKey == self.NEW_KEY:
            self.get('radiobutton2').set_active(True)
            self.disable('spinbutton1', True)
        if self.start: self.refreshProceed()


    @Log(Const.LOG_UI)
    def on_switch_mode(self, s, data):
        """"""
        self.app.switchEncMode(not s.get_active())
        if not self.app.splitmode :
            for n in ['checkbutton2','checkbutton4','comboboxtext1','label12']:
                self.disable(n, not self.app.encmode)
        #~ self.on_new_file_dest(self.get('filechooserbutton3'))
        if self.start: self.refreshProceed()


    @Log(Const.LOG_UI)
    def on_switch_format(self, s, data):
        """"""
        self.app.switchFormatMode(not s.get_active())
        if self.app.encmode :
            for n in ['checkbutton1', 'spinbutton2', 'checkbutton2','checkbutton4','comboboxtext1','label12']:
                self.disable(n, self.app.splitmode)
        if not s.get_active() :
            self.get('label8').set_text('encrypt')
            self.get('label9').set_text('decrypt')
            self.get('checkbutton1').set_sensitive(True)
            self.get('spinbutton2').set_sensitive(True)
        else :
            self.get('label8').set_text('split')
            self.get('label9').set_text('merge')
            self.get('checkbutton1').set_sensitive(False)
            self.get('spinbutton2').set_sensitive(False)
        if self.start: self.refreshProceed()


    @Log(Const.LOG_UI)
    def on_new_file_source(self, fc, data=None):
        """"""
        try:
            self.app.setSourceFile(fc.get_filename())
            self.IS_SOURCE_DEF = True
        except FileNotFoundException as e:
            Sys.eprint('FileNotFoundException :' + str(fc.get_filename()), Const.ERROR)
            self.IS_SOURCE_DEF = False
        self.refreshProceed()


    @Log(Const.LOG_UI)
    def on_new_file_dest(self, fc, data=None):
        """"""
        try :
            self.app.setDestFile(fc.get_filename())
            print(self.app.dst)
        except Exception as e :
            print(e)
            pass
        if self.start:
            self.IS_DEST_DEF = True
            self.refreshProceed()


    @Log(Const.LOG_UI)
    def on_existing_key(self, button):
        """"""
        self.curKey = self.EXISTING_KEY
        self.disable('spinbutton1',True)
        self.disable('filechooserbutton1',False)
        self.get('filechooserbutton1').set_filename(self.app.kpath)
        fc = self.get('filechooserbutton1')
        self.on_new_file_key(fc)


    @Log(Const.LOG_UI)
    def on_new_key(self, button):
        """"""
        self.curKey = self.NEW_KEY
        self.disable('spinbutton1',False)
        self.disable('filechooserbutton1',False)
        self.get('filechooserbutton1').set_current_folder(conf.DEFVAL_UKEY_PATH)
        self.get('filechooserbutton1').set_filename(conf.DEFVAL_UKEY_PATH+'.rename.key')


    @Log(Const.LOG_UI)
    def on_default_key(self, button):
        """"""
        self.curKey = self.DEFAULT_KEY
        self.disable('spinbutton1',True)
        self.disable('filechooserbutton1',True)
        fc = self.get('filechooserbutton1')
        fc.set_filename(self.app.getDefaultKeyPath())
        self.on_new_file_key(fc)


    @Log(Const.LOG_UI)
    def on_autoscroll_changed(self, btn):
        """"""
        Sys.g.UI_AUTO_SCROLL = not btn.get_active()


    @Log(Const.LOG_NEVER)
    def clear_log(self, btn):
        """"""
        self.textbuffer.set_text('')


    @Log(Const.LOG_UI)
    def show_log(self):
        """"""
        btn = self.get('button1')
        if not self.PROCEED :
            self.get('frame3').hide()
            self.get('frame1').show()
            self.get('frame2').show()
            self.get('checkbutton3').hide()
            self.repack('frame4', True)
            btn.set_sensitive(self.IS_DEST_DEF and self.IS_SOURCE_DEF)

        else :
            self.repack('frame4', False)
            self.get('frame1').hide()
            self.get('frame2').hide()
            self.get('frame3').show()
            self.get('checkbutton3').show()
            if btn.get_label() == conf.GUI_LABEL_PROCEED :
                btn.set_sensitive(False)


    @Log(Const.LOG_UI)
    def refreshProceed(self):
        """"""
        #~ if self.start :
        self.get('button1').set_sensitive(self.IS_DEST_DEF and self.IS_SOURCE_DEF)


    @Log(Const.LOG_UI)
    def on_proceed(self, btn):
        """"""
        if btn.get_label() == conf.GUI_LABEL_OK :
            btn.set_label(conf.GUI_LABEL_PROCEED)
            self.PROCEED = False
            self.pb.hide()
            self.show_log()

        else :
            if not self.PROCEED :
                self.PROCEED = True
                self.STOPPED = False
                btn.set_sensitive(False)
                self.app.setDestFile(self.get('filechooserbutton3').get_filename())
                if not Io.file_exists(self.app.dst) or self.warnDialog('file '+self.app.dst+' already exists', 'Overwrite file ?'):
                    self.pb = self.get('progressbar1')
                    self.pb.set_fraction(0)
                    self.pb.show()
                    self.pb.pulse()
                    btn.set_sensitive(True)
                    btn.set_label(conf.GUI_LABEL_CANCEL)
                    self.clear_log(self.get('checkbutton3'))
                    self.show_log()
                    self.launch_thread()
                else :
                    self.on_proceed_end(True)
            else :
                self.halt_thread()


    @Log(Const.LOG_UI)
    def halt_thread(self, *args):
        Sys.wlog(Sys.dprint())
        Sys.pwarn(('thread interrupt',), False)
        self.get('button1').set_sensitive(False)
        if self.thkmh is not None and self.thkmh.isAlive():
            self.thkmh.cancel()
        else :
            self.textbuffer.insert_at_cursor('Kmh Thread is not Alive\n')
            self.on_proceed_end(True)
            self.pb.hide()
            self.show_log()


    @Log(Const.LOG_UI)
    def on_proceed_end(self, abort=False):
        """"""
        try :
            btn = self.get('button1')
            btn.set_label('Proceed')
            btn.set_sensitive(True)
            self.PROCEED = False
            if not abort : btn.set_label(conf.GUI_LABEL_OK)
            self.get('checkbutton3').hide()

        except Exception as e:
            Sys.pwarn((('on_proceed_end : ',(str(e),Sys.CLZ_WARN_PARAM), ' !'),), False)
            pass
        return False
