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
import os
import modules.keyboard as keyboard
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk


class EintragBearbeitenDialog:
    def __init__(self, root, aktuelle_auswahl, hotkey="", dateiname="", volume=15):
        """
        Klasse EintragBearbeitenDialog
          Bietet ein Fenster für die drei Einträge zum anpassen, mit "Datei öffnen" Dialog, Hotkey
          Erkennung und Lautstärke-Schieberegler
        Einstellungen/Werte übernehmen
          Dem Button button_abbrechen und  button_uebernehmen müssen Funktionen nach
          dem erstellen des Objektes zugewiesen werden. Die Werte zum Übernehmen
          können von entry_hk, entry_dn und entry_vu entnommen werden.
        * root (tk master) Das aufrufende Fenster
        * aktuelle_auswahl (int) zum übernehmen und weitergeben der aktuellen Auswahl in der zu bearbeitenden Liste
        * hotkey (string) optional - Standard: "" - evtl. vorhandener Hotkey als vorgabe zum ändern
        * dateiname (string) optional - Standard: "" - evtl. vorhandener Dateiname samt Pfad
        * volume (integer) optional - Standard: 15 - evtl. vorhandener Lautstärkewert

        :param root:
        :param aktuelle_auswahl:
        :param hotkey:
        :param dateiname:
        :param volume:
        """
        self.aktuelle_auswahl = aktuelle_auswahl
        self.scale_pausieren = False
        self.dialogfenster = tk.Toplevel(root)
        self.dialogfenster.title("Eintrag bearbeiten...")

        # Oberer Frame
        # ------------
        self.frame_oben = tk.Frame(self.dialogfenster)
        self.frame_oben.pack(side=tk.TOP, fill=tk.X, expand=1)
        self.frame_oben.columnconfigure(0, weight=1)
        self.frame_oben.columnconfigure(1, weight=20)
        self.frame_oben.columnconfigure(2, weight=1)
        self.frame_oben.rowconfigure(0, weight=1)
        self.frame_oben.rowconfigure(1, weight=1)
        self.frame_oben.rowconfigure(2, weight=1)
        self.frame_oben.rowconfigure(3, weight=1)

        self.label_hk = tk.Label(self.frame_oben, text="Hotkey :")
        self.label_hk.grid(column=0, row=0, padx=5, pady=5, sticky=tk.EW)

        self.entry_hk = tk.Entry(self.frame_oben)
        self.entry_hk.grid(column=1, row=0, padx=5, pady=5, sticky=tk.EW)

        self.button_hk = tk.Button(self.frame_oben, text="Hotkey aufnehmen...", command=self.recordkey)
        self.button_hk.grid(column=2, row=0, padx=5, pady=5, sticky=tk.EW)

        self.label_dn = tk.Label(self.frame_oben, text="Dateiname :")
        self.label_dn.grid(column=0, row=1, padx=5, pady=5, sticky=tk.EW)

        self.entry_dn = tk.Entry(self.frame_oben)
        self.entry_dn.grid(column=1, row=1, padx=5, pady=5, sticky=tk.EW)

        self.button_dn = tk.Button(self.frame_oben, text="Datei öffnen...", command=self.dateioeffnen)
        self.button_dn.grid(column=2, row=1, padx=5, pady=5, sticky=tk.EW)

        self.label_vu = tk.Label(self.frame_oben, text="Lautstärke :")
        self.label_vu.grid(column=0, row=2, padx=5, pady=5, sticky=tk.EW)

        self.entry_vu = tk.Entry(self.frame_oben)
        self.entry_vu.grid(column=1, row=2, padx=5, pady=5, sticky=tk.EW)

        self.scale_vu = ttk.Scale(self.frame_oben, orient=tk.HORIZONTAL, from_=0, to=100, command=self.scaleaktion)
        self.scale_vu.grid(column=2, row=2, padx=7, pady=5, sticky=tk.EW)

        # Unterer Frame
        # -------------
        self.frame_unten = tk.Frame(self.dialogfenster)
        self.frame_unten.pack(side=tk.TOP, fill=tk.X, expand=1)

        self.button_abbrechen = ttk.Button(self.frame_unten, text="Abbrechen")
        self.button_abbrechen.pack(side=tk.RIGHT)

        self.button_uebernehmen = ttk.Button(self.frame_unten, text="OK")
        self.button_uebernehmen.pack(side=tk.RIGHT)

        # UI interne Funktionalität - Bind
        # --------------------------------
        self.entry_vu.bind("<KeyRelease>", self.on_entry_vu_click)  # keyup
        self.entry_vu.bind("<Leave>", self.on_entry_vu_click)  # mouse leaves entry

        # UI mit gelieferten Werten füllen
        # --------------------------------
        self.entry_hk.insert(0, hotkey)
        self.entry_dn.insert(0, dateiname)
        self.entry_vu.insert(0, volume)
        self.scale_vu.set(int(volume))

    def recordkey(self):
        """
        Diese Funktion wird im Dialog genutzt um das erkennen des Hotkeys zu starten

        :return:
        """
        if os.geteuid() != 0:
            messagebox.showinfo("root Rechte", "Dir fehlen die root Rechte um die Überwachung zu"
                                               " starten oder einen Hotkey aufzunehmen (manuelle Eingabe möglich).")
        else:
            # ^^^ nur versuchen einen Hotkey aufzunehmen, wenn root Rechte erkannt werden.
            self.frame_unten.focus()
            # Ich habe den Fokus hier auf den frame selbst gesetzt, damit die registrierte Tasteneingabe
            # (eventueller einzelner Buchstabe oder Zahl nicht im Eingabefeld landen kann. Praktisch könnte zudem
            # auch sein, wenn dann gleich durch bestätigen mit Enter der Dialog bestätigt werden kann.)
            test = keyboard.read_hotkey(suppress=False)
            self.entry_hk.delete(0, tk.END)
            self.entry_hk.insert(0, test)
            return str(test)

    def dateioeffnen(self):
        """
        Diese Funktion startet und verarbeitet intern den Datei öffnen Dialog

        :return:
        """
        neuedatei = ""
        try:
            neuedatei = filedialog.askopenfilename(initialdir="~/", title="Eine Vlc kompatible Datei auswählen",
                                                   filetypes=[("alle Dateien", "*.*")])
        except FileNotFoundError:  # TODO weitere Error möglichkeiten checken/Berücksichtigen
            print("Es wurde keine Datei ausgewählt:")
        if not (len(neuedatei) == 0):
            self.entry_dn.delete(0, tk.END)
            self.entry_dn.insert(0, neuedatei)

    def scaleaktion(self, event):
        """
        Aktualisiert nach verschieben des Lautstärkereglers intern das entry_vu auf den neuen Wert

        * event (float) übergibt vom Scale widget den Stand des Schiebereglers

        :param event:
        :return:
        """
        if not self.scale_pausieren:
            self.entry_vu.delete(0, tk.END)
            self.entry_vu.insert(0, int(float(event)))
        else:
            self.scale_pausieren = False

    def on_entry_vu_click(self, event):
        """
        Setzt den editierten Wert auch beim scale_vu - solange es ein Integer ist,
         sonst wird der wert wieder überschrieben mit dem alten (vom Schieberegler)

        :param event:
        :return:
        """
        del event
        try:
            self.scale_pausieren = True
            self.scale_vu.set(int(self.entry_vu.get()))
        except ValueError:
            self.entry_vu.delete(0, tk.END)
            self.entry_vu.insert(0, int(float(self.scale_vu.get())))

    # def getaktuelleauswahl(self):
    #     return self.aktuelle_auswahl


# def uebernehmen(df, v):
#     badummtss["hk"] = df.entry_hk.get()
#     badummtss["dn"] = df.entry_dn.get()
#     badummtss["vu"] = df.entry_vu.get()
#     textfeld.insert(tk.END, "\nDictionary in uebernehmen funktion Werte übernommen (hinzugefügt)\n")
#     textfeld.insert(tk.END, badummtss)
#
#     df.dialogfenster.destroy()
#     return v
#
#
# def abbrechen(df):
#     df.dialogfenster.destroy()
#
#
# def show_dialog_eintraege_bearbeiten(root, v):
#     badummtss["tescht"] = "Hollidoo"
#     textfeld.insert(tk.END, "\nDictionary in show Dialog funktion - (aktualisiert)\n")
#     textfeld.insert(tk.END, badummtss)
#
#     hk = "i"  # test - hotkey
#     dn = "/home/alexander/scripte/jack-audio/jackmix/jackmix.config.jm-xml"  # test - dateiname
#     vu = 38  # test lautstärke
#     # dialog aufrufen zum testen
#     # --------------------------
#     dialog = EintragBearbeitenDialog(root, hk, dn, vu)
#     dialog.button_uebernehmen.config(command=lambda: uebernehmen(dialog, v))
#     dialog.button_abbrechen.config(command=lambda: abbrechen(dialog))
#
#     root.wait_window(dialog.dialogfenster)
#     # dialog.dialogfenster.destroy()
#
#
# if __name__ == '__main__':
#     badummtss = {"test": "nummer_eens", "N°2": "Nuuhmehr touw22"}
#
#     window = tk.Tk()
#     window.title("Dummy-Aufruf")
#     frame = tk.Frame(window)
#     frame.pack()
#
#     textfeld = tk.Text(frame)
#     textfeld.pack(padx=5, pady=5)
#     textfeld.insert(tk.END, "Startbereich\n Dictionary nach Zuweisung:\n")
#     textfeld.insert(tk.END, badummtss)
#     button1 = ttk.Button(frame, text="Dialog öffnen...",
#     ###command=lambda: show_dialog_eintraege_bearbeiten(window, badummtss))
#     button1.pack(padx=5, pady=5)
#
#     window.mainloop()
