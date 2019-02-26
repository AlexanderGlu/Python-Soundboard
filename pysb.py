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

# TODO neues Tuple Dateiformat siehe: pickle und shelve
#

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

import os, shelve, math
import keyboard  # , time
import vlc3 as vlc

if sys.hexversion >= 0x03010000:
    # use some advanced feature
    print("Deine Version passt.")
else:
    print("Benutze python 3 :D")
    # use an alternative implementation or warn the user

konfigurationsdatei = 'PYSB.shelv.config'
hk = []


# ----------------- Tk- Dialog --------------------
# TODO löschen von Einträgen

class volumeErkennenDialog:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        top.title("Lautstärke angeben")

        self.slider_senkr = Scale(top, command=self.volume_set, from_=100, to=0, orient=VERTICAL, length=100)
        self.slider_senkr.pack(side=TOP)
        self.volentry = Entry(top, text=str(root.einzelvol), width=5)
        self.volentry.pack(side=TOP)
        self.buttonexit = Button(top, text="ok", command=self.buttonexitaction)
        self.buttonexit.pack(side=BOTTOM)
        self.volentry.delete(0, END)
        self.volentry.insert(0, str(root.einzelvol))
        print("volume-scale menüaufbau..")
        print(root.einzelvol)
        self.slider_senkr.set(int(root.einzelvol))
        self.volentry.bind('<Return>', self.refreshscale)
        self.volentry.bind('<FocusOut>', self.refreshscale)


    def buttonexitaction(self):
        print("--" + str(self.slider_senkr.get()) + "--" + str(self.volentry.get()))
        if str(self.slider_senkr.get()) == str(self.volentry.get()):
            self.quit()
        root.einzelvol = self.volentry.get()
        self.quit()


    def refreshscale(self, event):
        try:
            self.slider_senkr.set(int(self.volentry.get()))
        except:
            print("Das eingegebene Volume konnte nicht gesetzt werden")


    def volume_set(self, vol):
        root.einzelvol = int(vol)
        print("test" + str(vol))
        self.volentry.delete(0, END)
        self.volentry.insert(0, str(vol))

    def quit(self):
        self.top.destroy()


class hotkeyerkennenDialog:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        top.title("Hotkey eingeben") # klappts?? TODO testen oder entfernen

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
        if not (root_checken() == "keinroot"):
            # ^^^ nur versuchen einen Hotkey aufzunehmen, wenn root Rechte erkannt werden.
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
                volumesetplayer(i[2])
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
    volume = int(event)
    if volume > 100:
        volume = 100
    root.mastervolume = volume
    volumesetplayer(root.aktuelles_einzelvolume)
    # TODO hier muss noch volumesetplayer aufgerufen werden.

def calcvolume(einzelvolume, mastervolume):
    #print("\nErrechne ziellautstärke")
    #print("Einzelvolume/Dateivolume: " + str(einzelvolume))
    #print("Mastervolume            : " + str(mastervolume))
    if einzelvolume == 0:
        return 0
    if mastervolume == 0:
        return 0
    volumeergebnis = (float(einzelvolume)*(float(mastervolume) / 100 ))
    #print("Zielvolume:             : " + str(volumeergebnis))
    return volumeergebnis


def volumesetplayer(einzelvolume):
    if root.player == None:
        return
    volume = int(calcvolume(einzelvolume, root.mastervolume))
    #print("Zurückgegebene Lautstärke als int: " + str(int(volume)))
    if volume > 100:
        volume = 100
    if root.player.audio_set_volume(volume) == -1:
        print('schschschsch... self.errorDialog("Failed to set volume")')


def readconfig(configdatei):
    try:
        with shelve.open(configdatei) as shelvefile:
            hk = shelvefile["hk"]
            root.mastervolume = shelvefile["mastervolume"]
        shelvefile.close()
    except:
        print("Beim laden gab es irgendeinen Fehler")
    #alter code:
    # lauf = 0
    # hk = []
    # zeile1_pfad = ""
    # zeile2_hk = ""
    # with open(configdatei, "r") as configuration:
    #     for i in configuration:
    #         lauf = lauf + 1
    #         if lauf == 1:
    #             zeile1_pfad = i.strip()
    #         elif lauf == 2:
    #             zeile2_hk = i.strip()
    #             volumestandardwert=15
    #             # TODO alles von alt- auf neu umbauen was shelve betriff/datei laden/speichern + converter..
    #             # TODO configconverter erstellen - mit erkennung einer "alten configdatei" sowie anschließendem
    #             #   löschen
    #             hk.append((zeile1_pfad, zeile2_hk, volumestandardwert))
    #             lauf = 0
    #     configuration.close()
    return hk


def reloadconfiganddisplay(configdatei):
    root.hotkeys = readconfig(configdatei)
    configinlistenladen()
    # TODO shelve test:
    # cd=str(configdatei) + ".shelve"
    # with shelve.open(cd) as shelvefile:
    #     hhkk=shelvefile["hk"]
    # shelvefile.close()
    # print("shelvefileinhalt:")
    # print(hhkk)
    # print("vs ori:")
    # print(root.hotkeys)


def writeconfig(configdatei, hk):
    with shelve.open(configdatei) as shelvefile:
        shelvefile["hk"] = hk
        print("mastervolume soll gespeichert werden: " + str(root.mastervolume))
        shelvefile["mastervolume"] = root.mastervolume
    shelvefile.close()
    # with open(configdatei, "w") as configuration:
    #     for i in hk:
    #         configuration.write(i[0])
    #         configuration.write("\n")
    #         configuration.write(i[1])
    #         configuration.write("\n")
    #     configuration.close()


# def writeconfig_new_shelve(configdatei, hk):
#     cd=str(configdatei) + ".shelve"
#     with shelve.open(cd,) as shelvefile:
#         shelvefile["hk"] = hk
#     shelvefile.close()


def configinlistenladen():
    listbox_dn.delete(0, END)
    listbox_hk.delete(0, END)
    listbox_vol.delete(0, END)
    for i in root.hotkeys:
        listbox_dn.insert(END, str(i[0]))
        listbox_hk.insert(END, str(i[1]))
        listbox_vol.insert(END, str(i[2]))
    listboxenneuereintraghinzufuegen()
    print("mastervolume soll gesetzt werden: " + str(int(root.mastervolume)))
    volslider.set(int(root.mastervolume))


def listboxenneuereintraghinzufuegen():
    listbox_dn.insert(END, "Neuer Eintrag...")
    listbox_hk.insert(END, "Neuer Eintrag...")
    listbox_vol.insert(END, "Neu...")


def listenrechtsklick_hk(event):
    y = str(str(event).split()[5]).strip("y=>")
    # Im event steht die zur liste relative Position des Cursors beim Klick - die so herausgefiltert wird
    listenrechtsklick("hk", y)


def listenrechtsklick_dn(event):
    y = str(str(event).split()[5]).strip("y=>")
    # Im event steht die zur liste relative Position des Cursors beim Klick - die so herausgefiltert wird
    listenrechtsklick("dn", y)


def listenrechtsklick_vol(event):
    y = str(str(event).split()[5]).strip("y=>")
    # Im event steht die zur liste relative Position des Cursors beim Klick - die so herausgefiltert wird
    listenrechtsklick("vol", y)

def listenrechtsklick(liste, y):
    auswahl = listbox_dn.nearest(y)
    # Die nearest Funktion gibt mit hilfe von y den Eintrag an Position y wieder (relative Koordinate)
    file=(listbox_dn.get(auswahl), listbox_vol.get(auswahl))
    listenrechtsklick_play(file)


def listenrechtsklick_play(file):
    if file[0] != "Neuer Eintrag...":
        media = root.instanz_vlc.media_new(file[0])
        print(file[1])
        volumesetplayer(file[1])
        root.aktuelles_einzelvolume=file[1]
        root.player.set_media(media)
        root.player.play()


def listendoppelklick_hotkey(event):
    auswahl = listbox_hk.curselection()[0]  # Den ausgewählten Eintrag in der Listbox auslesen
    root.hotkeyAufnahme = "test"
    d = hotkeyerkennenDialog(root)  # Dialog zum Hotkey abfragen aufrufen
    root.wait_window(d.top)  # ^^^
    if root.hotkeyAufnahme == "":  # Wurde kein Hotkey im Dialog eingegeben?
        print("Hotkey wurde nicht aufgenommen/kein hotkey bekommen.")
    else:
        listbox_hk.delete(auswahl)  # Den Eintrag in der Liste austauschen
        listbox_hk.insert(auswahl, root.hotkeyAufnahme)  # ^^^
        if listbox_hk.size() == (auswahl + 1):  # Der Eintrag für ein neues Element in der Liste wurde geändert/gewählt
            root.hotkeys.append(("", str(root.hotkeyAufnahme), 15))  # Einen neuen Eintrag in der Tuple anlegen
            listbox_dn.delete(auswahl)
            listbox_vol.delete(auswahl)
            # Eintrag in der Dateinamen Liste aktualisieren auf ein leeren Inhalt (ist ja komplett neu)
            listbox_dn.insert(auswahl, "")  # ^^^
            listbox_vol.insert(auswahl,15)  # ^^^
            listboxenneuereintraghinzufuegen()  # Neuen Platzhalter für hinzufügen erstellen.
        else:
            root.hotkeys[auswahl] = ((root.hotkeys[auswahl][0]), str(root.hotkeyAufnahme), root.hotkeys[auswahl][2])
            # Die Tuple von der config/gelesenen Liste auch aktualisieren


def listendoppelklick_dateiname(event):
    auswahl = listbox_dn.curselection()[0]  # den ausgewählten eintrag in der listbox auslesen
    try:
        root.neuedatei=""
        root.neuedatei = filedialog.askopenfilename(initialdir="~/", title="Eine Vlc kompatible Datei auswählen",
                                                filetypes=[("alle Dateien","*.*")])
    except:
        print("Es wurde keine Datei ausgewählt:")
    if not (len(root.neuedatei) == 0):
        # TODO (Die angabe aller Audioformate wäre ganz schön mühsam - villeicht später)
        listbox_dn.delete(auswahl)  # Den Eintrag in der Liste austauschen
        listbox_dn.insert(auswahl, root.neuedatei)  # ^^^
        if listbox_dn.size() == (auswahl + 1):  # Der Eintrag für ein neues Element in der Liste wurde geändert/gewählt
            root.hotkeys.append((str(root.neuedatei), "", 15))  # Einen neuen Eintrag in der Tuple anlegen
            listbox_hk.delete(auswahl)
            listbox_vol.delete(auswahl)
            # Eintrag in der Dateinamen Liste aktualisieren auf ein leeren Inhalt (ist ja komplett neu)
            listbox_hk.insert(auswahl, "")  # ^^^
            listbox_vol.insert(auswahl, 15)  # ^^^
            listboxenneuereintraghinzufuegen()  # Neuen Platzhalter für hinzufügen erstellen.
        else:
            root.hotkeys[auswahl] = (str(root.neuedatei), root.hotkeys[auswahl][1], root.hotkeys[auswahl][2])
            # Die Tuple von der config/gelesene liste auch aktualisieren


def listendoppelklick_volume(event):
    auswahl = listbox_vol.curselection()[0]
    root.einzelvol = listbox_vol.get(auswahl)
    volDialog = volumeErkennenDialog(root)  # dialogaufbau
    root.wait_window(volDialog.top)  # warten auf dialog

    listbox_vol.delete(auswahl)
    listbox_vol.insert(auswahl, root.einzelvol)

    temp= root.hotkeys[auswahl]
    del root.hotkeys[auswahl]
    root.hotkeys.insert(auswahl, (temp[0], temp[1], root.einzelvol))



def listendeletekey_hotkey(event):
    auswahl = listbox_hk.curselection()[0]
    listendelete(auswahl)


def listendeletekey_dateiname(event):
    auswahl = listbox_dn.curselection()[0]
    listendelete(auswahl)


def listendeletekey_volume(event):
    auswahl = listbox_vol.curselection()[0]
    listendelete(auswahl)


def listendelete(auswahl):
    if listbox_dn.size() > 1:
        listbox_hk.delete(auswahl)
        listbox_dn.delete(auswahl)
        listbox_vol.delete(auswahl)
        del root.hotkeys[auswahl]
    else:
        print("Die Liste ist schon leer oder ein anderes Problem")


def root_checken():
    if os.geteuid() != 0:
        messagebox.showinfo("root Rechte", "Dir fehlen die root Rechte um die Überwachung zu"
                                           " starten oder einen Hotkey aufzunehmen (manuelle Eingabe möglich).")
        return "keinroot"
        #raise ImportError('You must be root to use this library on linux.')


# TODO irgendwann entfernen? definition zum ausgeben der tuple im Terminal
def printtuple():
    for i in root.hotkeys:
        print(i[0])
        print(i[1])
        print("\n")


def setslider(event):
    volslider.set(int(root.mastervolume))
    # hacky mc hack hack :) wird nur genutzt um beim start den scale (volume) zu laden

if __name__ == '__main__':
    root = Tk()

    root.title("PySB - Python-Soundboard")
    root.hotkeyAufnahme = ""
    root.listenkeyeventhandlerliste = []
    root.einzelvol = 0  # wird verwendet für den Volume-Dialog
    root.aktuelles_einzelvolume = 0  # wird verwendet beim setzen der Lautstärke
    root.mastervolume = 0  #
    root.hotkeys = readconfig(konfigurationsdatei)

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

    # Frame mit der Dateinamen Liste
    # ------------------------------
    frame_listen_dn = Frame(frame_listen)
    frame_listen_dn.pack(side=LEFT, fill=BOTH, expand=1)
    label_dn = Label(frame_listen_dn, text="Dateinamen:")
    label_dn.pack(side=TOP)
    listbox_dn = Listbox(frame_listen_dn)
    listbox_dn.pack(side=LEFT, fill=BOTH, expand=1)

    # Frame mit der Volume Liste
    # --------------------------
    frame_liste_volume = Frame(frame_listen)
    frame_liste_volume.pack(side=RIGHT, fill=Y)
    label_vol = Label(frame_liste_volume, text="Vol.")
    label_vol.pack(side=TOP)
    listbox_vol = Listbox(frame_liste_volume, width=5)
    listbox_vol.pack(side=RIGHT, fill=Y, expand=1)


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
    volslider = Scale(frame_volume, command=volumeset, from_=0, to=100, orient=HORIZONTAL, length=600)  #, variable=scalevar)
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
    root.bind('<FocusIn>', setslider)  # wird nur genutzt um beim start den scale (volume) zu setzen
    listbox_hk.bind('<Button-3>', listenrechtsklick_hk)
    listbox_hk.bind('<Double-Button-1>', listendoppelklick_hotkey)
    listbox_hk.bind('<Delete>', listendeletekey_hotkey)
    listbox_dn.bind('<Button-3>', listenrechtsklick_dn)
    listbox_dn.bind('<Double-Button-1>', listendoppelklick_dateiname)
    listbox_dn.bind('<Delete>', listendeletekey_dateiname)
    listbox_vol.bind('<Button-3>', listenrechtsklick_vol)
    listbox_vol.bind('<Double-Button-1>', listendoppelklick_volume)
    listbox_vol.bind('<Delete>', listendeletekey_volume)

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
