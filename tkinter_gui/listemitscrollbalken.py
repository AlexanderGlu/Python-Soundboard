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
from tkinter import ttk as ttk


class ScrollListe:
    def __init__(self, host):
        """
        Initiiert ein Listbox mir Vertikaler und Horizontaler Scrollbar
          der "topframe" muss beim Aufrufer per pack oder grid eingebunden werden.
        :param host:
        """
        self.topframe = ttk.Frame(host)

        self.listbox = tk.Listbox(self.topframe)
        self.scrollbar_vertikal = ttk.Scrollbar(self.topframe, orient=tk.VERTICAL)

        self.scrollbar_horizontal = ttk.Scrollbar(self.topframe, orient=tk.HORIZONTAL)

        self.scrollbar_horizontal.configure(command=self.listbox.xview)
        self.listbox.configure(xscrollcommand=self.scrollbar_horizontal.set, yscrollcommand=self.scrollbar_vertikal.set)
        self.scrollbar_vertikal.configure(command=self.listbox.yview)

        self.topframe.columnconfigure(0, weight=999)
        self.topframe.columnconfigure(1, weight=1)
        self.topframe.rowconfigure(0, weight=999)
        self.topframe.rowconfigure(1, weight=1)

        self.listbox.grid(column=0, row=0, sticky=tk.NSEW)
        self.scrollbar_vertikal.grid(column=1, row=0, sticky=tk.NSEW)
        self.scrollbar_horizontal.grid(column=0, row=1, rowspan=2, sticky=tk.NSEW)


# def fill(listbox, startnummer, anzahl, extrastr):
#     for i in range(startnummer, anzahl+1):
#         listbox.insert(tk.END, str(i) + extrastr + pf)
#
#
# pf = " - "
# for i in range(21):
#     pf = pf + str(i) + " soo long   "

# if __name__ == '__main__':
#     app = tk.Tk()
#
#     app.title("Listentext")
#     frame_fuer_listen = tk.Frame(app)
#     frame_fuer_listen.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)
#
#     scrolllistenhandler = []
#     for sl_nr in range(3):
#         scrolllistenhandler.append(ScrollListe(frame_fuer_listen))
#         scrolllistenhandler[sl_nr].topframe.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
#
#     fill(scrolllistenhandler[0].listbox, 1, 15, "num1")
#     fill(scrolllistenhandler[1].listbox, 15, 40, "num2")
#     fill(scrolllistenhandler[2].listbox, 40, 55, "num3")
#
#     app.mainloop()
