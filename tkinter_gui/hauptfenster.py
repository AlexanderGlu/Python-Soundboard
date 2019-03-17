# *********************************************************************************************************************
#    This file is part of PYSB Python Soundboard.
#
#    Authors: Tim H. <contact at https://discord.gg/8hRXDnM (TuxPlayDE#6693), https://www.twitch.tv/tuxplayde>
#                   Alexander Glüsing <alexandergluesing@posteo.de>
#
#    PYSB Python Soundboard is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    PYSB Python Soundboard is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PYSB Python Soundboard.  If not, see <http://www.gnu.org/licenses/>.
# *********************************************************************************************************************


import tkinter as tk
import tkinter_gui.listemitscrollbalken as listboxscroll
from tkinter import ttk


class Hauptfenster:
    """
    Enthält das Tkinter Startfenster für PYSB
    """
    def __init__(self, root):
        """
        Initialisiert das Startfenster für Pysb

        :param root: Das root Fenster in das es eingebaut wird
        """
        self.root = root

        # Das Menü
        # --------
        self.menue = tk.Menu(self.root)
        self.root.config(menu=self.menue)
        # "reiter" datei
        self.menue_dateimenue = tk.Menu(self.menue)
        self.menue.add_cascade(label="Datei", menu=self.menue_dateimenue)
        self.menue_dateimenue.add_command(label="speichern...")
        self.menue_dateimenue.add_command(label="Neu Laden")
        self.menue_dateimenue.add_separator()
        self.menue_dateimenue.add_command(label="Beenden")

        self.menue_help = tk.Menu(self.menue)
        self.menue.add_cascade(label="about", menu=self.menue_help)
        self.menue_help.add_command(label="Help")
        self.menue_help.add_command(label="about")

        # TODO löschen (relaod und save button)
        # # self.root = tk.Frame(self.parent)
        # # Frame mit [Laden] und [Speichern]
        # # ---------------------------------
        # self.frame_saveandreload = ttk.Frame(self.root)
        # self.frame_saveandreload.pack(side=tk.TOP)
        # self.reloadButton = ttk.Button(self.frame_saveandreload, text="Config neu Laden")
        # self.saveButton = ttk.Button(self.frame_saveandreload, text="Speichern")
        # self.reloadButton.pack(side=tk.LEFT, padx=5, pady=5)
        # self.saveButton.pack(side=tk.RIGHT, padx=5, pady=5)

        # Frame mit den Listen (Hotkeys, Dateinamen, Volume)
        # --------------------------------------------------
        self.frame_listen = ttk.Frame(self.root)
        self.frame_listen.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.frame_listen.columnconfigure(0, weight=4)
        self.frame_listen.columnconfigure(1, weight=60)
        self.frame_listen.columnconfigure(2, weight=1)
        self.frame_listen.rowconfigure(0, weight=1)
        self.frame_listen.rowconfigure(1, weight=999)

        self.ueberschrift_hk = ttk.Label(self.frame_listen, text="Hotkeys:")
        self.ueberschrift_hk.grid(column=0, row=0)
        self.ueberschrift_dn = ttk.Label(self.frame_listen, text="Dateinamen:")
        self.ueberschrift_dn.grid(column=1, row=0)
        self.ueberschrift_vo = ttk.Label(self.frame_listen, text="Volume:")
        self.ueberschrift_vo.grid(column=2, row=0)

        self.listenhandler = []
        for i in range(3):
            self.listenhandler.append(listboxscroll.ScrollListe(self.frame_listen))
            self.listenhandler[i].topframe.grid(column=i, row=1, sticky=tk.NSEW)

        self.label_editinfo = tk.Label(self.root, text='(Zum editieren "Doppelklicken"         ' +
                                                        'Zum Löschen [entf] drücken     ' +
                                                        'Rechtsklick zum abspielen)')
        self.label_editinfo.pack()

        # Frame für den allgemeinen Lautstärkeregler
        # ------------------------------------------
        self.frame_volume = tk.Frame(self.root)
        self.frame_volume.pack(fill=tk.X)
        #self.frame_volume.rowconfigure(0, weight=1)
        #self.frame_volume.rowconfigure(1, weight=100)
        self.frame_volume.columnconfigure(0, weight=1)
        self.frame_volume.columnconfigure(1, weight=100)

        self.label_volume = tk.Label(self.frame_volume, text="Lautsärke:")
        # self.label_volume.pack(side=tk.LEFT, padx=10)
        self.label_volume.grid(column=0, row=0, padx=10)
        self.volslider = tk.Scale(self.frame_volume, from_=0, to=100, orient=tk.HORIZONTAL, length=600)
        # self.volslider.pack(side=tk.LEFT, fill=tk.X, expand=1)
        self.volslider.grid(column=1, row=0, sticky=tk.EW)

        # Frame für das starten/Stopppen der Überwachung
        # ----------------------------------------------
        self.frame_ueberwachung = tk.Frame(self.root)
        self.frame_ueberwachung.pack(fill=tk.X)
        self.label_ueberwachung = tk.Label(self.frame_ueberwachung, text="Shortcut- Überwachung: ")
        self.label_ueberwachung.pack(side=tk.LEFT)
        self.button_ueberw_start = ttk.Button(self.frame_ueberwachung, text='starten')
        self.button_ueberw_start.pack(side=tk.LEFT, padx=5, pady=5)
        self.button_ueberw_stop = ttk.Button(self.frame_ueberwachung, text='stoppen')
        self.button_ueberw_stop.pack(side=tk.LEFT, padx=5, pady=5)
        self.button_ueberw_quit = ttk.Button(self.frame_ueberwachung, text='Quit', command=self.root.quit)
        self.button_ueberw_quit.pack(side=tk.RIGHT, padx=5, pady=5)
