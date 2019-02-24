#!/usr/bin/python3
#
# ***********************************************************************************************************************
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
# ***********************************************************************************************************************

# #############################################################
#    Python Modul nachinstallieren: 'pip install keyboard'
# #############################################################

# ---    keyboard.get_hotkey_name(names=None)
# ---
# ---[source]
# ---
# ---Returns a string representation of hotkey from the given key names, or
# ---the currently pressed keys if not given. This function:
# ---
# ---    normalizes names;
# ---    removes "left" and "right" prefixes;
# ---    replaces the "+" key name with "plus" to avoid ambiguity;
# ---    puts modifier keys first, in a standardized order;
# ---    sort remaining keys;
# ---    finally, joins everything with "+".
# ---
# ---Example:
# ---
# ---get_hotkey_name(['+', 'left ctrl', 'shift'])
# ---# "ctrl+shift+plus"
# ---
# ---
# ---    print(hotkeypressed[0])
# ---    print(hotkeypressed)

# evtl. python-argparse für Kommandozeilen Interpretierung
# python-regex

# TODO per entry Volume
# TODO neues Tuple Dateiformat siehe: pickle und shelve
# TODO Dafür sorgen, dass wenn ein Hotkey aufgenommen wird ab der Aufforderung dafür durch Doppelklick der Eintrag
#  dafür registriert und weitergegeben wird an die funktion.
#  damit nicht durch den wechseln der Auswahl in der Liste der falsche Eintrag überschrieben wird.
#

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

import os
import keyboard  # , time
import vlc3 as vlc

if sys.hexversion >= 0x03010000:
    # use some advanced feature
    print("Deine Version passt.")
else:
    print("Benutze python 3 :D")
    # use an alternative implementation or warn the user

konfigurationsdatei = 'PYSB.config'
hk = []


# ----------------- Tk- Dialog --------------------
# TODO löschen von Einträgen

class hotkeyerkennenDialog:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)

        self.frameLabel = Frame(top)
        self.frameLabel.pack(pady=5, padx=5)

        self.l1 = Label(self.frameLabel, text="Erkannter Shortcut: ")
        self.l1.pack(side=LEFT)
        self.e = Entry(self.frameLabel)
        self.e.pack(side=RIGHT, padx=5)

        self.b = Button(top, text="OK", command=self.ok)
        self.b.pack(side=LEFT, pady=5)
        self.b2 = Button(top, text="Hotkey erkennen", command=self.recordkey)
        self.b2.pack(side=RIGHT, pady=5)

    def ok(self):
        root.hotkeyAufnahme = self.e.get()
        self.top.destroy()

    def recordkey(self):
        self.b.focus()
        # Ich habe den Fokus hier auf den button gesetzt, damit die registrierte Tasteneingabe
        # (eventueller einzelner Buchstabe oder Zahl nicht im Eingabefeld landen kann. Praktisch könnte zudem
        # auch sein, wenn dann gleich durch bestätigen mit Enter der Dialog bestätigt werden kann.)
        test = keyboard.read_hotkey(suppress=False)

        self.e.delete(0, END)
        self.e.insert(0, test)


def play(hk):
    try:
        hotkeypressed = keyboard.get_hotkey_name()
        for i in hk:
            if i[1] == hotkeypressed:
                media = root.instanz_vlc.media_new(i[0])
                root.player.set_media(media)
                root.player.play()
    except:
        print("Variable " + hotkeypressed +
              " wurde nicht gefunden oder es ist etwas in der Funktion 'def play(hk) schiefgelaufen'")


def startlisten(hk):
    if root_checken() == "keinroot":
        return
    else:
        for i in hk:
            # test=keyboard.add_hotkey(i[1], lambda: play(hk))
            root.listenkeyeventhandlerliste.append(keyboard.add_hotkey(i[1], lambda: play(hk)))


def stoplisten():
    for i in root.listenkeyeventhandlerliste:
        keyboard.remove_hotkey(i)
    root.player.stop()
    root.listenkeyeventhandlerliste = []


def volumeset(event):
    if root.player == None:
        return
    volume = int(event)
    if volume > 100:
        volume = 100
    if root.player.audio_set_volume(volume) == -1:
        print('schschschsch... self.errorDialog("Failed to set volume")')


def readconfig(configdatei):
    lauf = 0
    hk = []
    zeile1_pfad = ""
    zeile2_hk = ""
    with open(configdatei, "r") as configuration:
        for i in configuration:
            lauf = lauf + 1
            if lauf == 1:
                zeile1_pfad = i.strip()
            elif lauf == 2:
                zeile2_hk = i.strip()

                hk.append((zeile1_pfad, zeile2_hk))
                lauf = 0
        configuration.close()
    return hk


def reloadconfiganddisplay(configdatei):
    root.hotkeys = readconfig(configdatei)
    configinlistenladen()


def writeconfig(configdatei, hk):
    with open(configdatei, "w") as configuration:
        for i in hk:
            configuration.write(i[0])
            configuration.write("\n")
            configuration.write(i[1])
            configuration.write("\n")
        configuration.close()


def configinlistenladen():
    listbox_dn.delete(0, END)
    listbox_hk.delete(0, END)
    for i in root.hotkeys:
        listbox_dn.insert(END, str(i[0]))
        listbox_hk.insert(END, str(i[1]))
    listboxenneuereintraghinzufuegen()


def listboxenneuereintraghinzufuegen():
    listbox_dn.insert(END, "Neuer Eintrag...")
    listbox_hk.insert(END, "Neuer Eintrag...")


def listenrechtsklick_hk(event):
    y = str(str(event).split()[5]).strip("y=>")
    # Im event steht die zur liste relative Position des Cursors beim Klick - die so herausgefiltert wird
    listenrechtsklick("hk", y)


def listenrechtsklick_dn(event):
    y = str(str(event).split()[5]).strip("y=>")
    # Im event steht die zur liste relative Position des Cursors beim Klick - die so herausgefiltert wird
    listenrechtsklick("dn", y)


def listenrechtsklick(liste, y):
    auswahl = listbox_dn.nearest(y)
    # Die nearest Funktion gibt mit hilfe von y den Eintrag an Position y wieder (relative Koordinate)
    listenrechtsklick_play(listbox_dn.get(auswahl))


def listenrechtsklick_play(file):
    if file != "Neuer Eintrag...":
        media = root.instanz_vlc.media_new(file)
        root.player.set_media(media)
        root.player.play()


def listendoppelklick_hotkey(event):
    root.hotkeyAufnahme = "test"
    d = hotkeyerkennenDialog(root)  # Dialog zum Hotkey abfragen aufrufen
    root.wait_window(d.top)  # ^^^
    if root.hotkeyAufnahme == "":  # Wurde kein Hotkey im Dialog eingegeben?
        print("Hotkey wurde nicht aufgenommen/kein hotkey bekommen.")
    else:
        auswahl = listbox_hk.curselection()[0]  # Den ausgewählten Eintrag in der Listbox auslesen
        listbox_hk.delete(auswahl)  # Den Eintrag in der Liste austauschen
        listbox_hk.insert(auswahl, root.hotkeyAufnahme)  # ^^^
        if listbox_hk.size() == (auswahl + 1):  # Der Eintrag für ein neues Element in der Liste wurde geändert/gewählt
            root.hotkeys.append(("", str(root.hotkeyAufnahme)))  # Einen neuen Eintrag in der Tuple anlegen
            listbox_dn.delete(auswahl)
            # Eintrag in der Dateinamen Liste aktualisieren auf ein leeren Inhalt (ist ja komplett neu)
            listbox_dn.insert(auswahl, "")  # ^^^
            listboxenneuereintraghinzufuegen()  # Neuen Platzhalter für hinzufügen erstellen.
        else:
            root.hotkeys[auswahl] = ((root.hotkeys[auswahl][0]), str(
                root.hotkeyAufnahme))  # Die Tuple von der config/gelesenen Liste auch aktualisieren


def listendoppelklick_dateiname(event):
    auswahl = listbox_dn.curselection()[0]  # den ausgewählten eintrag in der listbox auslesen
    try:
        root.neuedatei = filedialog.askopenfilename(initialdir="~/", title="Eine Vlc kompatible Datei auswählen",
                                                    filetypes=[("alle Dateien","*.*")])
        # TODO (Die angabe aller Audioformate wäre ganz schön mühsam - villeicht später)
        listbox_dn.delete(auswahl)  # Den Eintrag in der Liste austauschen
        listbox_dn.insert(auswahl, root.neuedatei)  # ^^^
        if listbox_dn.size() == (auswahl + 1):  # Der Eintrag für ein neues Element in der Liste wurde geändert/gewählt
            root.hotkeys.append((str(root.neuedatei), ""))  # Einen neuen Eintrag in der Tuple anlegen
            listbox_hk.delete(
                auswahl)  # Eintrag in der Dateinamen Liste aktualisieren auf ein leeren Inhalt (ist ja komplett neu)
            listbox_hk.insert(auswahl, "")  # ^^^
            listboxenneuereintraghinzufuegen()  # Neuen Platzhalter für hinzufügen erstellen.
        else:
            root.hotkeys[auswahl] = (str(root.neuedatei), root.hotkeys[auswahl][1])
            # Die Tuple von der config/gelesene liste auch aktualisieren
    except:
        print("Es wurde keine Datei ausgewählt:")


def listendeletekey_hotkey(event):
    auswahl = listbox_hk.curselection()[0]
    listendelete(auswahl)


def listendeletekey_dateiname(event):
    auswahl = listbox_dn.curselection()[0]
    listendelete(auswahl)


def listendelete(auswahl):
    if listbox_dn.size() > 1:
        listbox_hk.delete(auswahl)
        listbox_dn.delete(auswahl)
        del root.hotkeys[auswahl]
    else:
        print("Die Liste ist schon leer oder ein anderes Problem")


def root_checken():
    if os.geteuid() != 0:
        # TODO hier funktion reinbringen:
        print("noch nicht gemacht - kein root!! errormessage")
        messagebox.showinfo("root Rechte", "Dir fehlen die root Rechte um die Überwachung zu starten.")
        return "keinroot"
        #raise ImportError('You must be root to use this library on linux.')


# TODO irgendwann entfernen? definition zum ausgeben der tuple im Terminal
def printtuple():
    for i in root.hotkeys:
        print(i[0])
        print(i[1])
        print("\n")


if __name__ == '__main__':
    root = Tk()

    root.title("PySB - Python-Soundboard")
    root.hotkeys = readconfig("PYSB.config")
    root.hotkeyAufnahme = ""
    root.listenkeyeventhandlerliste = []

    # Frame mit [Laden] und [Speichern]
    # ---------------------------------
    frame_saveandreload = Frame(root)
    frame_saveandreload.pack(side=TOP)
    reloadButton = Button(frame_saveandreload, text="Config neu Laden",
                          command=lambda: reloadconfiganddisplay(konfigurationsdatei))
    saveButton = Button(frame_saveandreload, text="Speichern",
                        command=lambda: writeconfig(konfigurationsdatei, root.hotkeys))
    reloadButton.pack(side=LEFT, padx=5, pady=5)
    saveButton.pack(side=RIGHT, padx=5, pady=5)

    # Frame mit den Zwei Sub-Frames für Hotkeys und Dateinamen, sowie Volume Button
    # -----------------------------------------------------------------------------
    # TODO Frame mit Volume Button und weiteren zum Bearbeiten/anpassen -
    #  evtl. UI Fenster zum anpassen von Hotkey und Dateinamen in einem.
    frame_listen = Frame(root)
    frame_listen.pack(fill=BOTH, expand=1)

    # Frame mit der linken Liste (Hotkeys)
    # ------------------------------------
    frame_listenleft = Frame(frame_listen, width=23)
    frame_listenleft.pack(side=LEFT, fill=Y)
    label_hk = Label(frame_listenleft, text="Shortcuts:")
    label_hk.pack(side=TOP)
    listbox_hk = Listbox(frame_listenleft)
    listbox_hk.pack(fill=Y, expand=1)

    # Frame mit der mittleren?/rechten Liste (Dateinamen)
    # ---------------------------------------------------
    frame_listenright = Frame(frame_listen)
    frame_listenright.pack(side=RIGHT, fill=BOTH, expand=1)
    label_dn = Label(frame_listenright, text="Dateinamen:")
    label_dn.pack(side=TOP)
    listbox_dn = Listbox(frame_listenright)
    listbox_dn.pack(side=LEFT, fill=BOTH, expand=1)

    label_editinfo = Label(root,
                           text='(Zum editieren "Doppelklicken"         ' +
                                'Zum Löschen [entf] drücken     ' +
                                'Rechtsklick zum abspielen)')
    label_editinfo.pack()

    # Frame für den allgemeinen Lautstärkeregler
    # ------------------------------------------
    frame_volume = Frame(root)
    frame_volume.pack(fill=X)
    label_volume = Label(frame_volume, text="Lautsärke:")
    label_volume.pack(side=LEFT, padx=10)
    volslider = Scale(frame_volume, command=volumeset, from_=0, to=100, orient=HORIZONTAL, length=600)
    volslider.pack(side=LEFT, fill=X, expand=1)

    # Frame für das starten/Stopppen der Überwachung
    # ----------------------------------------------
    frame_ueberwachung = Frame(root)
    frame_ueberwachung.pack(fill=X)
    label_ueberwachung = Label(frame_ueberwachung, text="Shortcut- Überwachung: ")
    label_ueberwachung.pack(side=LEFT)
    button_ueberw_start = Button(frame_ueberwachung, text='starten', command=lambda: startlisten(root.hotkeys))
    button_ueberw_start.pack(side=LEFT, padx=5, pady=5)
    button_ueberw_stop = Button(frame_ueberwachung, text='stoppen', command=lambda: stoplisten())
    button_ueberw_stop.pack(side=LEFT, padx=5, pady=5)
    button_ueberw_quit = Button(frame_ueberwachung, text='Quit', command=root.quit)
    button_ueberw_quit.pack(side=RIGHT, padx=5, pady=5)

    # Funktionen einbinden
    # --------------------
    listbox_hk.bind('<Button-3>', listenrechtsklick_hk)
    listbox_hk.bind('<Double-Button-1>', listendoppelklick_hotkey)
    listbox_hk.bind('<Delete>', listendeletekey_hotkey)
    listbox_dn.bind('<Button-3>', listenrechtsklick_dn)
    listbox_dn.bind('<Double-Button-1>', listendoppelklick_dateiname)
    listbox_dn.bind('<Delete>', listendeletekey_dateiname)

    # Listen befüllen
    # ---------------
    configinlistenladen()

    # ######################   [ Vlc player - ini?! ] ########################################
    # Den Vlc Player Initialisieren (für nur eine Instanz)
    # ----------------------------------------------------
    # TODO evtl. mehrere Instanzen ermöglichen, die parallel gestartet werden mit einer Ansicht was gerade geladen ist?
    root.instanz_vlc = vlc.Instance()
    root.player = root.instanz_vlc.media_player_new()
    # set the volume slider to the current volume
    # self.volslider.SetValue(self.player.audio_get_volume() / 2)
    volslider.set(root.player.audio_get_volume())

    # #### below is a test, now use the File->Open file menu   #### kopiert :-)
    # ####media = self.Instance.media_new('output.mp4')
    # ####self.player.set_media(media)
    # ####self.player.play() # hit the player button
    # ####self.player.video_set_deinterlace(str_to_bytes('yadif'))

    root.mainloop()
