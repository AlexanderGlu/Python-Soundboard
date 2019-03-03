#!/usr/bin/python3
#
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

# *************************************************************
#    Python Modul nachinstallieren: 'pip install keyboard'
# *************************************************************

# TODO evtl. python-argparse für Kommandozeilen Interpretierung

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

import os
import configparser
import keyboard
import vlc3 as vlc

konfigurationsdatei = 'PYSB.ini'
hk = []

# ######################   [ Vlc player - ini?! ] ########################################
# Den Vlc Player Initialisieren (für nur eine Instanz)
# ----------------------------------------------------
# TODO evtl. mehrere Instanzen ermöglichen, die parallel gestartet werden mit einer Ansicht was gerade geladen ist?
instanz_vlc = vlc.Instance()
player = instanz_vlc.media_player_new()


# set the volume slider to the current volume
# volslider.set(player.audio_get_volume())


# ----------------- Tk- Dialog --------------------


class VolumeErkennenDialog:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        top.title("Lautstärke angeben")

        self.slider_senkr = ttk.Scale(top, command=self.volume_set, from_=100, to=0, orient=VERTICAL, length=100)
        self.slider_senkr.pack(side=TOP)
        self.volentry = ttk.Entry(top, text=str(root.einzelvol), width=5)
        self.volentry.pack(side=TOP)
        self.buttonexit = ttk.Button(top, text="ok", command=self.buttonexitaction)
        self.buttonexit.pack(side=BOTTOM)
        self.volentry.delete(0, END)
        self.volentry.insert(0, str(root.einzelvol))
        self.slider_senkr.set(int(root.einzelvol))
        self.volentry.bind('<Return>', self.refreshscale)
        self.volentry.bind('<FocusOut>', self.refreshscale)

    def buttonexitaction(self):
        if str(self.slider_senkr.get()) == str(self.volentry.get()):
            self.quit()
        try:
            root.einzelvol = int(self.volentry.get())
        except ValueError:
            print("Das eingegebene Volume konnte nicht gesetzt werden (ValueError)")
            self.volentry.delete(0, END)
            self.volentry.insert(0, self.slider_senkr.get())
        self.quit()

    def refreshscale(self, event):
        try:
            self.slider_senkr.set(int(self.volentry.get()))
        except TclError:
            print("Das eingegebene Volume konnte nicht gesetzt werden (TclError)")
            self.volentry.delete(0, END)
            self.volentry.insert(0, self.slider_senkr.get())
        except ValueError:
            print("Das eingegebene Volume konnte nicht gesetzt werden (ValueError)")
            self.volentry.delete(0, END)
            self.volentry.insert(0, self.slider_senkr.get())

    def volume_set(self, vol):
        root.einzelvol = int(float(vol))
        self.volentry.delete(0, END)
        self.volentry.insert(0, str(int(float(vol))))

    def quit(self):
        self.top.destroy()


class HotkeyErkennenDialog:
    def __init__(self, parent):
        top = self.top = Toplevel(parent)
        top.title("Hotkey eingeben")

        self.frameLabel = Frame(top)
        self.frameLabel.pack(pady=5, padx=5)

        self.l1 = ttk.Label(self.frameLabel, text="Erkannter Shortcut: ")
        self.l1.pack(side=LEFT)
        self.e = ttk.Entry(self.frameLabel)
        self.e.pack(side=RIGHT, padx=5)

        self.b = ttk.Button(top, text="OK", command=self.ok)
        self.b.pack(side=LEFT, pady=5)
        self.b2 = ttk.Button(top, text="Hotkey erkennen", command=self.recordkey)
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


def play(hkvar):
    try:
        hotkeypressed = keyboard.get_hotkey_name()
        for i in hkvar:
            if i[1] == hotkeypressed:
                media = instanz_vlc.media_new(i[0])
                player.set_media(media)
                volumesetplayer(i[2])
                player.play()
    except:
        print("Variable " + hotkeypressed +
              " wurde nicht gefunden oder es ist etwas in der Funktion 'def play(hk) schiefgelaufen'")


def startlisten(hkvar):
    if root_checken() == "keinroot":
        return
    else:
        for i in hkvar:
            root.listenkeyeventhandlerliste.append(keyboard.add_hotkey(i[1], lambda: play(hkvar)))


def stoplisten():
    for i in root.listenkeyeventhandlerliste:
        keyboard.remove_hotkey(i)
    player.stop()
    root.listenkeyeventhandlerliste = []


def volumeset(event):
    volume = int(float(event))
    if volume > 100:
        volume = 100
    root.mastervolume = volume
    volumesetplayer(root.aktuelles_einzelvolume)


def calcvolume(einzelvolume, mastervolume):
    if einzelvolume == 0:
        return 0
    if mastervolume == 0:
        return 0
    volumeergebnis = (float(einzelvolume)*(float(mastervolume) / 100))
    return volumeergebnis


def volumesetplayer(einzelvolume):
    #if player is None:
    #    return
    volume = int(calcvolume(einzelvolume, root.mastervolume))
    if volume > 100:
        volume = 100
    if player.audio_set_volume(volume) == -1:
        print('Konnte die Lautstärke nicht anpassen')


def readconfig(configdatei):
    hkvar = []
    config = configparser.ConfigParser()
    config.read(str(configdatei))
    if 'Einstellungen' in config.sections():
        root.mastervolume = 0
        root.mastervolume = int(config['Einstellungen']['mastervolume'])
    else:
        print("Keine Lautstärkeeinstellung in der Konfiguration gefunden")
    count = 1
    if not (str('Hotkeyconfig' + str(count)) in config.sections()):
        print("Kein [Hotkeyconfig1] in '" + configdatei + "' gefunden")
    while str('Hotkeyconfig' + str(count)) in config:
        # -----------------------------------------------------------------------
        #               Dateiname Laden
        try:
            dateiname = config[str('Hotkeyconfig' + str(count))]['Dateiname']
        except KeyError:
            print("Keinen Dateinamen unter " + str('Hotkeyconfig' + str(count)) + " gefunden")
            dateiname = ""
        # -----------------------------------------------------------------------
        #               Hotkey Laden
        try:
            hotkey = config[str('Hotkeyconfig' + str(count))]['Hotkey']
        except KeyError:
            print("Keinen Hotkey unter " + str('Hotkeyconfig' + str(count)) + " gefunden")
            hotkey = ""
        # -----------------------------------------------------------------------
        #               Lautstärke Laden
        try:
            volume = int(config[str('Hotkeyconfig' + str(count))]['Volume'])
        except KeyError:
            print("Keinen Lautstärkeeintrag unter " + str('Hotkeyconfig' + str(count)) + " gefunden")
            volume = ""
        hkvar.append([dateiname, hotkey, volume])
        count = count + 1
    return hkvar


def reloadconfiganddisplay(configdatei):
    root.hotkeys = readconfig(configdatei)
    configinlistenladen()


def writeconfig(configdatei, hkvar):
    config = configparser.ConfigParser()
    config['Einstellungen'] = {'mastervolume': str(root.mastervolume)}
    count = 0
    for i in hkvar:
        count = count + 1
        config[str('Hotkeyconfig' + str(count))] = {
            'Dateiname': str(i[0]),
            'Hotkey': str(i[1]),
            'Volume': str(i[2])
        }
    with open(configdatei, 'w') as cfgfile:
        config.write(cfgfile)


def configinlistenladen():
    listbox_dn.delete(0, END)
    listbox_hk.delete(0, END)
    listbox_vol.delete(0, END)
    for i in root.hotkeys:
        listbox_dn.insert(END, str(i[0]))
        listbox_hk.insert(END, str(i[1]))
        listbox_vol.insert(END, str(i[2]))
    listboxenneuereintraghinzufuegen()
    volslider.set(int(root.mastervolume))


def listboxenneuereintraghinzufuegen():
    listbox_dn.insert(END, "Neuer Eintrag...")
    listbox_hk.insert(END, "Neuer Eintrag...")
    listbox_vol.insert(END, "Neu...")


def listenrechtsklick_hk(event):
    y = str(str(event).split()[5]).strip("y=>")
    # Im event steht die zur liste relative Position des Cursors beim Klick - die so herausgefiltert wird
    listenrechtsklick(y)


def listenrechtsklick_dn(event):
    y = str(str(event).split()[5]).strip("y=>")
    # Im event steht die zur liste relative Position des Cursors beim Klick - die so herausgefiltert wird
    listenrechtsklick(y)


def listenrechtsklick_vol(event):
    y = str(str(event).split()[5]).strip("y=>")
    # Im event steht die zur liste relative Position des Cursors beim Klick - die so herausgefiltert wird
    listenrechtsklick(y)


def listenrechtsklick(y):
    auswahl = listbox_dn.nearest(y)
    # Die nearest Funktion gibt mit hilfe von y den Eintrag an Position y wieder (relative Koordinate)
    file = (listbox_dn.get(auswahl), listbox_vol.get(auswahl))
    listenrechtsklick_play(file)


def listenrechtsklick_play(file):
    if file[0] != "Neuer Eintrag...":
        media = instanz_vlc.media_new(file[0])
        volumesetplayer(file[1])
        root.aktuelles_einzelvolume = file[1]
        player.set_media(media)
        player.play()


def listendoppelklick_hotkey(event):
    auswahl = listbox_hk.curselection()[0]  # Den ausgewählten Eintrag in der Listbox auslesen
    root.hotkeyAufnahme = "test"
    d = HotkeyErkennenDialog(root)  # Dialog zum Hotkey abfragen aufrufen
    root.wait_window(d.top)  # ^^^
    if root.hotkeyAufnahme == "":  # Wurde kein Hotkey im Dialog eingegeben?
        print("Hotkey wurde nicht aufgenommen/kein hotkey bekommen.")
    else:
        listbox_hk.delete(auswahl)  # Den Eintrag in der Liste austauschen
        listbox_hk.insert(auswahl, root.hotkeyAufnahme)  # ^^^
        if listbox_hk.size() == (auswahl + 1):  # Der Eintrag für ein neues Element in der Liste wurde geändert/gewählt
            root.hotkeys.append(["", str(root.hotkeyAufnahme), 15])  # Einen neuen Eintrag in der Tuple anlegen
            listbox_dn.delete(auswahl)
            listbox_vol.delete(auswahl)
            # Eintrag in der Dateinamen Liste aktualisieren auf ein leeren Inhalt (ist ja komplett neu)
            listbox_dn.insert(auswahl, "")  # ^^^
            listbox_vol.insert(auswahl, 15)  # ^^^
            listboxenneuereintraghinzufuegen()  # Neuen Platzhalter für hinzufügen erstellen.
        else:
            root.hotkeys[auswahl] = ((root.hotkeys[auswahl][0]), str(root.hotkeyAufnahme), root.hotkeys[auswahl][2])
            # Die Tuple von der config/gelesenen Liste auch aktualisieren


def listendoppelklick_dateiname(event):
    auswahl = listbox_dn.curselection()[0]  # den ausgewählten eintrag in der listbox auslesen
    try:
        root.neuedatei = ""
        root.neuedatei = filedialog.askopenfilename(initialdir="~/", title="Eine Vlc kompatible Datei auswählen",
                                                    filetypes=[("alle Dateien", "*.*")])
    except:
        print("Es wurde keine Datei ausgewählt:")
    if not (len(root.neuedatei) == 0):
        # TODO (Die angabe aller Audioformate wäre ganz schön mühsam - villeicht später)
        listbox_dn.delete(auswahl)  # Den Eintrag in der Liste austauschen
        listbox_dn.insert(auswahl, root.neuedatei)  # ^^^
        if listbox_dn.size() == (auswahl + 1):  # Der Eintrag für ein neues Element in der Liste wurde geändert/gewählt
            root.hotkeys.append([str(root.neuedatei), "", 15])  # Einen neuen Eintrag in der Tuple anlegen
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
    vol_dialog = VolumeErkennenDialog(root)  # Dialogaufbau
    root.wait_window(vol_dialog.top)  # Warten auf den Dialog

    listbox_vol.delete(auswahl)
    listbox_vol.insert(auswahl, root.einzelvol)

    temp = root.hotkeys[auswahl]
    del root.hotkeys[auswahl]
    root.hotkeys.insert(auswahl, [temp[0], temp[1], root.einzelvol])


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


def setslider(event):
    volslider.set(int(root.mastervolume))
    # hacky mc hack hack :) wird nur genutzt um beim Start den scale (volume) Wert zu laden


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
    reloadButton = ttk.Button(frame_saveandreload, text="Config neu Laden",
                              command=lambda: reloadconfiganddisplay(konfigurationsdatei))
    saveButton = ttk.Button(frame_saveandreload, text="Speichern",
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
    frame_listen_hk = Frame(frame_listen, width=43)
    frame_listen_hk.pack(side=LEFT, fill=Y)

    label_hk = Label(frame_listen_hk, text="Shortcuts:")
    label_hk.pack(side=TOP)
    frame_listen_hk_mitte = Frame(frame_listen_hk)
    frame_listen_hk_mitte.pack(side=TOP, fill=Y, expand=1)
    listbox_hk = Listbox(frame_listen_hk_mitte)
    listbox_hk.pack(side=LEFT, fill=Y, expand=1)
    # scrollbar_hk_ve = ttk.Scrollbar(frame_listen_hk_mitte, orient=VERTICAL)
    # scrollbar_hk_ve.pack(side=LEFT, fill=Y)
    # scrollbar_hk_ve.configure(command=listbox_hk.yview)
    # scrollbar_hk_ho = ttk.Scrollbar(frame_listen_hk, orient=HORIZONTAL)
    # scrollbar_hk_ho.pack(side=TOP, fill=X)
    # scrollbar_hk_ho.configure(command=listbox_hk.xview)

    # Frame mit der Dateinamen Liste
    # ------------------------------
    frame_listen_dn = Frame(frame_listen)
    frame_listen_dn.pack(side=LEFT, fill=BOTH, expand=1)
    label_dn = Label(frame_listen_dn, text="Dateinamen:")
    label_dn.pack(side=TOP)
    frame_listen_dn_mitte = Frame(frame_listen_dn)
    frame_listen_dn_mitte.pack(side=TOP, fill=BOTH, expand=1)
    listbox_dn = Listbox(frame_listen_dn_mitte)
    listbox_dn.pack(side=LEFT, fill=BOTH, expand=1)
    # scrollbar_dn_ve = ttk.Scrollbar(frame_listen_dn_mitte, orient=VERTICAL)
    # scrollbar_dn_ve.pack(side=LEFT, fill=Y)
    # scrollbar_dn_ve.configure(command=listbox_dn.yview)
    # scrollbar_dn_ho = ttk.Scrollbar(frame_listen_dn, orient=HORIZONTAL)
    # scrollbar_dn_ho.pack(side=TOP, fill=X)
    # scrollbar_dn_ho.configure(command=listbox_dn.xview)

    # Frame mit der Volume Liste
    # --------------------------
    frame_liste_volume = Frame(frame_listen, width=7)
    frame_liste_volume.pack(side=RIGHT, fill=Y)
    label_vol = Label(frame_liste_volume, text="Vol.")
    label_vol.pack(side=TOP)
    scrollbar_vol_ve = ttk.Scrollbar(frame_liste_volume, orient=VERTICAL)
    scrollbar_vol_ve.pack(side=RIGHT, fill=Y)
    listbox_vol = Listbox(frame_liste_volume, width=7)
    listbox_vol.pack(side=RIGHT, fill=Y, expand=1)
    scrollbar_vol_ve.configure(command=listbox_vol.yview)

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
    volslider = ttk.Scale(frame_volume, command=volumeset, from_=0, to=100, orient=HORIZONTAL, length=600)
    volslider.pack(side=LEFT, fill=X, expand=1)

    # Frame für das starten/Stopppen der Überwachung
    # ----------------------------------------------
    frame_ueberwachung = Frame(root)
    frame_ueberwachung.pack(fill=X)
    label_ueberwachung = Label(frame_ueberwachung, text="Shortcut- Überwachung: ")
    label_ueberwachung.pack(side=LEFT)
    button_ueberw_start = ttk.Button(frame_ueberwachung, text='starten', command=lambda: startlisten(root.hotkeys))
    button_ueberw_start.pack(side=LEFT, padx=5, pady=5)
    button_ueberw_stop = ttk.Button(frame_ueberwachung, text='stoppen', command=lambda: stoplisten())
    button_ueberw_stop.pack(side=LEFT, padx=5, pady=5)
    button_ueberw_quit = ttk.Button(frame_ueberwachung, text='Quit', command=root.quit)
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

    volslider.set(root.mastervolume)

    root.mainloop()
