# *********************************************************************************************************************
#    This file is part of PYSB Python Soundboard.
#
#    Authors: Tim H. <contact at https://discord.gg/8hRXDnM (TuxPlayDE#6693), https://www.twitch.tv/tuxplayde>
#             Alexander Glüsing <alexandergluesing@posteo.de>
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
from tkinter import ttk


class AboutDialog:
    def __init__(self, root):
        self.dialogfenster = tk.Toplevel(root)
        self.dialogfenster.title("About Python Soundboard")
        self.dialogfenster.wm_resizable(100, 100)

        # Oberer Frame
        # ------------
        self.frame_oben = ttk.Frame(self.dialogfenster)
        self.frame_oben.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.abouttext = """PYSB Python Soundboard

Soundboard zur Wiedergabe von Audio-Dateien per Tastatur (Hotkeys und Tastenkombinationen) geschrieben in Python
Die Idee und initiale Arbeit (Plugins finden, ersten Code zusammenstellen) stammt von TuxPlayDE.
Zum Abspielen der Audiodateien wird VLC verwendet und benötigt!
Das UI nutzt in dieser Version "Tkinter".

Das Programm muss unter Linux mit 'sudo' (Root-Rechten) ausgeführt werden, um zugriff auf die Tasteneingaben
zu bekommen! (Anforderung der "keyboard"-Bibliothek)

Website: https://github.com/AlexanderGlu/Python-Soundboard"""
        self.text = ttk.Label(self.frame_oben, text=self.abouttext)
        self.text.pack(padx=5, pady=5)
        self.button_ok = ttk.Button(self.frame_oben, text="OK", command=self.dialogfenster.destroy)
        self.button_ok.pack(pady=5, padx=5)


# def show_dialog_eintraege_bearbeiten(root):
#     dlg = AboutDialog(root)
#
#     root.wait_window(dlg.dialogfenster)
#
#
# if __name__ == '__main__':
#     badummtss = {"test": "nummer_eens", "N°2": "Nuuhmehr touw22"}
#
#     window = tk.Tk()
#     window.title("About")
#     frame = tk.Frame(window)
#     frame.pack()
#
#     textfeld = tk.Text(frame)
#     textfeld.pack(padx=5, pady=5)
#     textfeld.insert(tk.END, "Startbereich\n Dictionary nach Zuweisung:\n")
#     textfeld.insert(tk.END, badummtss)
#     dialog = AboutDialog(window)
#     window.wait_window(dialog.dialogfenster)
#
#     window.mainloop()
