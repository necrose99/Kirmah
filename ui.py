#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#  kirmah/ui.py
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

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~ module ui ~~

from gi.repository             import Pango
from gi.repository.Gdk         import threads_enter, threads_leave
from gi.repository.Gtk         import AboutDialog, Builder, main as main_enter, main_quit, MessageDialog, MessageType, ButtonsType, ResponseType, PackType
from gi.repository.GdkPixbuf   import Pixbuf
from gi.repository.GObject     import threads_init, GObject, idle_add, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_STRING, TYPE_FLOAT, TYPE_BOOLEAN
from threading                 import Thread, current_thread, enumerate as thread_enum
from multiprocessing           import Event
from psr.sys                   import Sys, Io, Const
from psr.log                   import Log
from kirmah                    import conf
from kirmah.cli                import Cli


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~ class Gui ~~

class Gui():


    @Log(Const.LOG_BUILD)
    def __init__(self, wname):
        """"""
        threads_init()
        self.wname   = wname
        self.builder = Builder()
        self.builder.add_from_file(conf.PRG_GLADE_PATH)
        self.builder.connect_signals(self)
        self.win = self.get(wname)
        self.win.connect('destroy', self.onDeleteWindow)
        self.win.connect('delete-event', self.onDeleteWindow)
        self.win.set_title(conf.PRG_NAME+' v'+conf.PRG_VERS)
        self.win.show_all()
        self.on_start()
        main_enter()


    @Log(Const.LOG_DEBUG)
    def buildTxtTags(self, textbuffer):
        tags = {}
        tags[Const.CLZ_TIME]        = textbuffer.create_tag(Const.CLZ_TIME        , foreground="#208420", weight=Pango.Weight.BOLD)
        tags[Const.CLZ_SEC]         = textbuffer.create_tag(Const.CLZ_SEC         , foreground="#61B661", weight=Pango.Weight.BOLD)
        tags[Const.CLZ_DEFAULT]     = textbuffer.create_tag(Const.CLZ_DEFAULT     , foreground="#FFEDD0")
        tags[Const.CLZ_IO]          = textbuffer.create_tag(Const.CLZ_IO          , foreground="#EB3A3A", weight=Pango.Weight.BOLD)
        tags[Const.CLZ_FUNC]        = textbuffer.create_tag(Const.CLZ_FUNC        , foreground="#EBEB3A", weight=Pango.Weight.BOLD)
        tags[Const.CLZ_CFUNC]       = textbuffer.create_tag(Const.CLZ_CFUNC       , foreground="#EBB33A", weight=Pango.Weight.BOLD)
        tags[Const.CLZ_DELTA]       = textbuffer.create_tag(Const.CLZ_DELTA       , foreground="#397BE8", weight=Pango.Weight.BOLD)
        tags[Const.CLZ_ARGS]        = textbuffer.create_tag(Const.CLZ_ARGS        , foreground="#A1A1A1")
        tags[Const.CLZ_ERROR]       = textbuffer.create_tag(Const.CLZ_ERROR       , background="#830005", foreground="#FFFFFF", weight=Pango.Weight.BOLD)
        tags[Const.CLZ_ERROR_PARAM] = textbuffer.create_tag(Const.CLZ_ERROR_PARAM , background="#830005", foreground="#EBEB3A", weight=Pango.Weight.BOLD)
        tags[Const.CLZ_WARN]        = textbuffer.create_tag(Const.CLZ_WARN        , background="#A81459", foreground="#FFFFFF", weight=Pango.Weight.BOLD)
        tags[Const.CLZ_WARN_PARAM]  = textbuffer.create_tag(Const.CLZ_WARN_PARAM  , background="#A81459", foreground="#EBEB3A", weight=Pango.Weight.BOLD)
        tags[Const.CLZ_PID]         = textbuffer.create_tag(Const.CLZ_PID         , background="#5B0997", foreground="#E4C0FF", weight=Pango.Weight.BOLD)
        tags[Const.CLZ_CPID]        = textbuffer.create_tag(Const.CLZ_CPID        , background="#770997", foreground="#F4CDFF", weight=Pango.Weight.BOLD)
        tags[Const.CLZ_SYMBOL]      = textbuffer.create_tag(Const.CLZ_SYMBOL      , background="#61B661", foreground="#FFFFFF", weight=Pango.Weight.BOLD)
        tags[Const.CLZ_OK]          = textbuffer.create_tag(Const.CLZ_OK          , background="#167B3B", foreground="#FFFFFF", weight=Pango.Weight.BOLD)
        tags[Const.CLZ_KO]          = textbuffer.create_tag(Const.CLZ_KO          , background="#7B1716", foreground="#FFFFFF", weight=Pango.Weight.BOLD)
        tags[Const.CLZ_TITLE]       = textbuffer.create_tag(Const.CLZ_TITLE       , foreground="#FFFFFF", weight=Pango.Weight.BOLD)
        tags[Const.CLZ_TASK]        = textbuffer.create_tag(Const.CLZ_TASK        , foreground="#61B661", weight=Pango.Weight.BOLD)
        tags[Const.CLZ_HEAD_APP]    = textbuffer.create_tag(Const.CLZ_HEAD_APP    , background="#2B5BAB", foreground="#FFFFFF", weight=Pango.Weight.BOLD)
        tags[Const.CLZ_HEAD_SEP]    = textbuffer.create_tag(Const.CLZ_HEAD_SEP    , foreground="#A1A1A1")
        tags[Const.CLZ_HEAD_KEY]    = textbuffer.create_tag(Const.CLZ_HEAD_KEY    , foreground="#EBEB3A", weight=Pango.Weight.BOLD)
        tags[Const.CLZ_HEAD_VAL]    = textbuffer.create_tag(Const.CLZ_HEAD_VAL    , foreground="#397BE8", weight=Pango.Weight.BOLD)
        return tags


    @Log(Const.LOG_UI)
    def onDeleteWindow(self, *args):
        """"""
        mthread = current_thread()
        try:
            self.join_threads(True)
            self.cleanResources()

        except Exception as e:
            pass

        finally:
            main_quit(*args)


    @Log(Const.LOG_UI)
    def list_threads(self):
        """"""
        print('thread list : ')
        for th in thread_enum():
            print(th)


    @Log(Const.LOG_UI)
    def join_threads(self, join_main=False):
        """"""
        mthread = current_thread()
        try:
            for th in thread_enum():
                if th is not mthread :
                    th.join()
            if join_main: mthread.join()

        except Exception as e:
            pass


    @Log(Const.LOG_UI)
    def on_about(self, btn):
        """"""
        about = AboutDialog()
        about.set_program_name(conf.PRG_NAME)
        about.set_version('v '+conf.PRG_VERS)
        about.set_copyright(conf.PRG_ABOUT_COPYRIGHT)
        about.set_comments(conf.PRG_ABOUT_COMMENTS)
        about.set_website(conf.PRG_WEBSITE)
        about.set_website_label(conf.PRG_WEBSITE)
        about.set_license(Io.get_data(conf.PRG_LICENSE_PATH))
        pixbuf = Pixbuf.new_from_file_at_size(conf.PRG_LOGO_PATH, conf.PRG_ABOUT_LOGO_SIZE, conf.PRG_ABOUT_LOGO_SIZE)
        about.set_logo(pixbuf)
        pixbuf = Pixbuf.new_from_file_at_size(conf.PRG_LOGO_PATH, conf.PRG_ABOUT_LOGO_SIZE, conf.PRG_ABOUT_LOGO_SIZE)
        about.set_icon(pixbuf)
        about.run()
        about.destroy()


    @Log(Const.LOG_DEBUG)
    def get(self, name):
        """"""
        return self.builder.get_object(name)


    @Log(Const.LOG_DEBUG)
    def disable(self, name, disabled):
        """"""
        self.get(name).set_sensitive(not disabled)


    @Log(Const.LOG_DEBUG)
    def repack(self, name, expandfill=False, packStart=True):
        w = self.get(name)
        w.get_parent().set_child_packing(w, expandfill, expandfill, 0, PackType.START if packStart else PackType.END )
        return w


    @Log(Const.LOG_DEBUG)
    def detachWidget(self, name, hideParent=True):
        w  = self.get(name)
        wp = w.get_parent()
        if wp is not None :
            wp.remove(w)
            w.unparent()
        if hideParent : wp.hide()


    @Log(Const.LOG_DEBUG)
    def attachWidget(self, widget, parentName, expandfill=None, showParent=True):
        if widget is not None :
            wp = self.get(parentName)
            if wp is not None :
                if expandfill is None : wp.add(widget)
                else :
                    wp.pack_start(widget,expandfill,expandfill,0)
                if showParent : wp.show()


    @Log(Const.LOG_UI)
    def thread_finished(self, thread, ref):
        thread = None
        self.on_proceed_end(False)


    @Log(Const.LOG_UI)
    def on_proceed_end(self, abort=False):
        """"""


    @Log(Const.LOG_UI)
    def thread_interrupted(self, thread, ref):
        thread = None
        self.end_progress()
        self.on_proceed_end(False)


    @Log(Const.LOG_NEVER)
    def thread_progress(self, thread, progress, ref):
        while not Sys.g.LOG_QUEUE.empty():
            data = Sys.g.LOG_QUEUE.get()
            if data is not None :
                if data is not Sys.g.SIGNAL_STOP :
                    for item in data :
                        ei   = self.textbuffer.get_end_iter()
                        offs = ei.get_offset()
                        self.textbuffer.insert_at_cursor(item[0])
                        ei = self.textbuffer.get_end_iter()
                        oi = self.textbuffer.get_iter_at_offset(offs)
                        tagName = item[1]
                        self.textbuffer.apply_tag(self.tags[tagName], oi, ei)
                    self.textbuffer.insert_at_cursor('\n')
                    self.scroll_end()
                else :
                    Sys.dprint('STOP')
                    thread.cancel()
        self.update_progress(progress)


    @Log(Const.LOG_NEVER)
    def update_progress(self, progress, lvl=50):
        if progress > 0 :
            self.progressbar.set_text(str(progress))
            lp   = self.progressbar.get_fraction()
            diff = (progress/100.0 - lp)
            for i in range(lvl):
                nf = lp+(i*diff/lvl)
                if nf < progress/100.0 :
                    self.progressbar.set_fraction(nf)
            self.progressbar.set_fraction(progress/100.0)
        else :
            self.progressbar.set_fraction(self.progressbar.get_fraction()+0.01)


    @Log(Const.LOG_NEVER)
    def end_progress(self):
        self.update_progress(100, 10)


    @Log(Const.LOG_NEVER)
    def scroll_end(self):
        if Sys.g.UI_AUTO_SCROLL :
            if self.textbuffer is not None :
                insert_mark = self.textbuffer.get_insert()
                ei   = self.textbuffer.get_end_iter()
                if ei is not None and insert_mark is not None:
                    self.textbuffer.place_cursor(ei)
                    self.textview.scroll_to_mark(insert_mark , 0.0, True, 0.0, 1.0)


    @Log(Const.LOG_UI)
    def cleanResources(self):
        """"""


    @Log(Const.LOG_UI)
    def on_start(self):
        """"""


    @Log(Const.LOG_UI)
    def warnDialog(self, intro, ask):
        """"""
        dialog = MessageDialog(self.get(self.wname), 0, MessageType.WARNING, ButtonsType.OK_CANCEL, intro)
        dialog.format_secondary_text(ask)
        response = dialog.run()
        dialog.destroy()
        return response == ResponseType.OK;


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~ class IdleObject ~~

class IdleObject(GObject):
    """
    Override gi.repository.GObject to always emit signals in the main thread
    by emmitting on an idle handler
    """

    @Log(Const.LOG_UI)
    def __init__(self):
        """"""
        GObject.__init__(self)


    @Log(Const.LOG_NEVER)
    def emit(self, *args):
        """"""
        idle_add(GObject.emit, self, *args)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~ class CliThread ~~

class CliThread(Thread, IdleObject):
    """
    Cancellable thread which uses gobject signals to return information
    to the GUI.
    """
    __gsignals__ =  {  # signal type            signal return      signal args
        "completed"   : ( SIGNAL_RUN_LAST, TYPE_NONE, ()),
        "interrupted" : ( SIGNAL_RUN_LAST, TYPE_NONE, ()),
        "progress"    : ( SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_FLOAT,))
    }


    @Log(Const.LOG_DEBUG)
    def __init__(self, rwargs, event):
        Thread.__init__(self)
        IdleObject.__init__(self)
        self.setName('CliThread')
        self.cliargs = rwargs
        self.event   = event

    @Log(Const.LOG_DEBUG)
    def run(self):
        """"""
        self.cancelled = False
        Sys.g.MPEVENT.clear()
        print(Sys.g.LOG_LEVEL)
        Cli('./', Sys.getpid(), self.cliargs, self, Sys.g.LOG_LEVEL)
        self.emit("completed")


    @Log(Const.LOG_NEVER)
    def progress(self, value):
        """"""
        self.emit("progress", value)


    @Log(Const.LOG_NEVER)
    def cancel(self):
        """
        Threads in python are not cancellable, so we implement our own
        cancellation logic
        """
        self.cancelled = True
        self.event.set()


    @Log(Const.LOG_NEVER)
    def stop(self):
        """"""
        if self.isAlive():
            self.cancel()
            if current_thread().getName()==self.getName():
                try:
                    self.emit("interrupted")
                    Sys.thread_exit()
                except RuntimeError as e :
                    print(str(self.getName()) + ' COULD NOT BE TERMINATED')
                    raise e
