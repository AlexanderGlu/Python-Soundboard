#!/usr/bin/env python3
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
# TODO optional Video berücksichtigen - mit extra fenster das evtl immer offen ist auch zum aus-key'en
#  bestimmten Hintergrund
# TODO evtl. mehrere Instanzen ermöglichen, die parallel gestartet werden mit einer Ansicht was gerade geladen ist?
# TODO ein Fenster mit allen parallel gestarteten listener'n und dazugehörigen
#  player'n - optional zum einzeln killen und einzelnem neuen hinzufügen
#  fenster mit scrollbar, eine klasse für player+ hk/dateiname/volslider Anzeige - sowie
#  slider für abspielfortschritt der einzelnen
#  mute button einzeln - gesamt
# TODO evtl playlisten als einzelne einträge unterstützen mit playeranzeige/nächster-letzter titel
# TODO laden und speichern in ein menü einbinden
# TODO ctrl+s (zum speichern der config) / ctrl+c (zum abbrechen des abspielens/zuhörens) /
#  ctrl+q zum beenden ohne speichern
# TODO alles in der gui sichtbare an text und infos als string/dictionary/liste einbinden mit englischem
#  text/titel und beim start von eienr ini nach sprachauswahl laden lassen
# TODO beim ersten start nach der sprache fragen und dann in einer lang.ini abspeichern


# from tkinter import filedialog
import tkinter as tk
# from tkinter import ttk
from tkinter import messagebox
import os
import configparser
# import keyboard
import modules.keyboard as keyboard
# import vlc
import modules.vlc3 as vlc
import tkinter_gui.hauptfenster as hauptfenster
# import tkinter_gui.listemitscrollbalken as listboxscroll
import tkinter_gui.funktionen as funktionen


konfigurationsdatei = 'PYSB.ini'
hk = []

# ######################   [ Vlc player - ini?! ] ########################################
# Den Vlc Player Initialisieren (für nur eine Instanz)
# ----------------------------------------------------
# vlc.Instance
# vlc_instance = vlc.Instance()
# vlc_player = vlc_instance.media_player_new()
var_vlc = {"instance": vlc.Instance(), "einzelvolume": 15}
var_vlc["player"] = (var_vlc["instance"].media_player_new())


# Gui unabhängige Funktionen:
# ---------------------------


def play(hkvar, vlc_dictionary):
    """
    Ließt den gedrückten Hotkey aus und spielt dazu gehörende Datei und Lautstärke ab

    * hkvar (list) Liste enthält
      ((hotkey1'string', dateiname1'string', volume1'int'),(hotkey2'string', dateiname2'string', volume2'int'), ...)
    * vlc_dictionary (Dict) enthält 'instance':vlc instanz, 'player': vlc player,
      'einzelvolume': vol der aktuellen Datei

    :param hkvar:
    :param vlc_dictionary:
    :return:
    """
    global var_mastervolume
    hotkeypressed = None
    try:
        hotkeypressed = keyboard.get_hotkey_name()
        for iterator in hkvar:
            if iterator[0] == hotkeypressed:
                vlc_dictionary["einzelvolume"] = iterator[2]
                media = vlc_dictionary["instance"].media_new(iterator[1])
                vlc_dictionary["player"].set_media(media)
                volumesetplayer(var_mastervolume, vlc_dictionary)
                vlc_dictionary["player"].play()
    except ValueError:  # TODO hier eventuell noch die Error Varianten austesten.
        print("Variable " + hotkeypressed +
              " wurde nicht gefunden oder es ist etwas in der Funktion 'def play(hk) schiefgelaufen'")


def startlisten(haupt_fenster, vlc_dictionary):
    """
    Startet Instanzen vom Modul Keyboard mit den eingestellten Hotkeys und den dazugehörigen Dateien

    * haupt_fenster (Object) Enthält das Henster
    * vlc_dictionary (Dict) enthält 'instance':vlc instanz, 'player': vlc player,
      'einzelvolume': vol der aktuellen Datei

    :param haupt_fenster:
    :param vlc_dictionary:
    :return:
    """
    global handler_list_hotkeys
    hkvar = []
    count = 0
    for i in haupt_fenster.listenhandler[0].listbox.get(0, tk.END)[0:-1]:
        hkvar.append([
            i,
            haupt_fenster.listenhandler[1].listbox.get(count),
            int(haupt_fenster.listenhandler[2].listbox.get(count))
        ])
        count += 1

    if root_checken() == "keinroot":
        return
    else:
        for iterator in hkvar:
            handler_list_hotkeys.append(keyboard.add_hotkey(iterator[0],
                                                            lambda: play(
                                                                hkvar,
                                                                vlc_dictionary)))


def stoplisten(vlc_dictionary):
    """
    Stoppt alle zuvor gestarteten und gespeicherten Instanzen vom modul keyboard

    * vlc_dictionary (Dict) enthält 'instance':vlc instanz, 'player': vlc player,
      'einzelvolume': vol der aktuellen Datei

    :param vlc_dictionary:
    :return:
    """
    # möglicher fehler "KeyError"
    global handler_list_hotkeys  # (list) Die gespeicherten Instanzen vom modul keyboard
    for iterator in handler_list_hotkeys:
        keyboard.remove_hotkey(iterator)
    vlc_dictionary["player"].stop()
    handler_list_hotkeys = []


def volumesetplayer(mastervolume, vlc_dictionary):
    """
    Setzt bei der aktuellen Vlc Instanz die Lautstärke neu

    * mastervolume (int) 0-100
    * vlc_dictionary (Dict) enthält 'instance':vlc instanz, 'player': vlc player,
      'einzelvolume': vol der aktuellen Datei

    :param mastervolume:
    :param vlc_dictionary:
    :return:
    """
    if vlc_dictionary["einzelvolume"] == 0 or mastervolume == 0:
        volume = 0
    else:
        volume = int(vlc_dictionary["einzelvolume"]*mastervolume/100)
    if volume > 100:
        volume = 100
    if vlc_dictionary["player"].audio_set_volume(volume) == -1:
        print('Konnte die Lautstärke nicht anpassen')


def readconfig(configdatei):
    """
    Gibt die Hotkeyliste und das Mastervolume nach dem Auslesen aus der configdatei zurück

    * configdatei (str) Der Pfad zur Ini ähnlichen configdatei
    * hkvar (list) wird gefüllt mit den Hotkey-Daten und zurückgegeben
    * mastervolume (int) wird gefüllt mit dem mastervolume und zurückgegeben

    :param configdatei:
    :return hkvar, mastervolume:
    """
    hkvar = []
    mastervolume = 0
    config = configparser.ConfigParser()
    config.read(str(configdatei))
    if 'Einstellungen' in config.sections():
        mastervolume = int(config['Einstellungen']['mastervolume'])
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
        hkvar.append([hotkey, dateiname, volume])
        count = count + 1
    return hkvar, mastervolume


def writeconfig(configdatei, hkvar, mastervolume):
    """
    Schreibt die aktuellen Daten der Variablen in die Ini Datei

    * configdatei (string) Der Pfad zur Ini ähnlichen configdatei
    * hkvar (list) Die Hotkey-Daten werden gespeichert
    * mastervolume Das Mastervolume wird gespeichert

    :param configdatei:
    :param hkvar:
    :param mastervolume:
    :return:
    """
    config = configparser.ConfigParser()
    config['Einstellungen'] = {'mastervolume': str(mastervolume)}
    count = 0
    for iterator in hkvar:
        count = count + 1
        config[str('Hotkeyconfig' + str(count))] = {
            'Hotkey': str(iterator[0]),
            'Dateiname': str(iterator[1]),
            'Volume': str(iterator[2])
        }
    with open(configdatei, 'w') as cfgfile:
        config.write(cfgfile)


def root_checken():
    """
    Gibt "keinroot" zurück, wenn der Nutzer keine root-Rechte hat und zeigt eine Infomeldung an

    :return (str):
    """
    if os.geteuid() != 0:
        messagebox.showinfo("root Rechte", "Dir fehlen die root Rechte um die Überwachung zu"
                                           " starten oder einen Hotkey aufzunehmen (manuelle Eingabe möglich).")
        return "keinroot"


# Funktionen für die GUI
# ----------------------
# fast alle verschoben nach ./tkinter_gui/funktionen.py
def fdialogoffen(setorget, var_bool=None):
    """
    Zum Abfragen und setzen der Variable var_var_dialog_offen. Diese Variable wird genutzt
    um zu Kontrollieren, dass nur ein Doalogfenster zu Zeit geöffnet ist.

    Beispiel:
     fdialogoffen("set", True)
    oder:
     mein_bool = fdialogoffen("get")

    :param setorget: (string) "set" um das Bool zu setzen oder "get" um es auszulesen
    :param var_bool: (Bool) Optional bei "get"
    :return var_dialog_offen: (Bool) gibt den Zustand der Variable zurück (nur bei "get")
    """
    global var_dialog_offen
    if setorget == "set":
        var_dialog_offen = var_bool
    if setorget == "get":
        return var_dialog_offen


def fvar_mastervolume(getorset, mastervolume=None):
    """
    Zum Abfragen und setzen der Variable var_mastervolume. Diese Variable wird genutzt
    um die Masterlautstärke global benutzen zu können.

    Beispiel:
     fvar_mastervolume("set", 100)
    oder:
     mastervolume = fvar_mastervolume("get")

    :param getorset: (str) "set" um das int zu setzen oder "get" um es auszulesen
    :param mastervolume: (int) Wert von 0-100 für die Lautstärkeangabe
    :return var_mastervolume: (int) - Optional - wird zurückgegeben wenn get gewählt wurde
    """
    global var_mastervolume
    if getorset == "set":
        var_mastervolume = mastervolume
    if getorset == "get":
        return var_mastervolume


def scale_volumeset(event, vlc_dictionary):
    """
    Sollte vom Volume scale aufgerufen werden und setzt die globale variable und übergibt an vlc die Lautstärke

    * vlc_dictionary (Dict) enthält 'instance':vlc instanz, 'player': vlc player,
      'einzelvolume': vol der aktuellen Datei

    :param event:
    :param vlc_dictionary:
    :return:
    """
    global var_mastervolume

    volume = int(float(event))
    if volume > 100:
        volume = 100
    var_mastervolume = volume
    volumesetplayer(var_mastervolume, vlc_dictionary)

# Variable in die das die Hotkeys, etc. und das Mastervolume aus der Datei geladen wird


var_hotkeys, var_mastervolume = readconfig(konfigurationsdatei)
var_dialog_offen = False
handler_list_hotkeys = []

if __name__ == '__main__':
    fenster = tk.Tk()
    # Fenstertitel und Icon setzen
    fenster.title("PySB - Python-Soundboard")
    fenster.tk.call('wm', 'iconphoto', fenster, tk.PhotoImage(file='data/PYSB.png'))

    # Aus dem Ordner tkinter_gui das Hauptfenster laden und einbinden
    hf = hauptfenster.Hauptfenster(fenster)

    # # Funktionen einbinden
    # # --------------------

    # Abkürzung der variable - hflh enthält die aus dem Hauptfenster geladene Variable mit den Listen
    lh = hf.listenhandler

    lh[0].listbox.bind('<Button-3>',
                       lambda event: funktionen.listenrechtsklick(
                           event, lh[0], hf, var_vlc, volumesetplayer))
    lh[1].listbox.bind('<Button-3>',
                       lambda event: funktionen.listenrechtsklick(
                           event, lh[1], hf, var_vlc, volumesetplayer))
    lh[2].listbox.bind('<Button-3>',
                       lambda event: funktionen.listenrechtsklick(
                           event, lh[2], hf, var_vlc, volumesetplayer))

    lh[0].listbox.bind('<Delete>', lambda event: funktionen.listedeketekey(event, lh[0], lh))
    lh[1].listbox.bind('<Delete>', lambda event: funktionen.listedeketekey(event, lh[1], lh))
    lh[2].listbox.bind('<Delete>', lambda event: funktionen.listedeketekey(event, lh[2], lh))

    lh[0].listbox.bind('<Double-Button-1>',
                       lambda event: funktionen.listendoppelklick(event, "hk", lh, fenster, fdialogoffen))
    lh[1].listbox.bind('<Double-Button-1>',
                       lambda event: funktionen.listendoppelklick(event, "dn", lh, fenster, fdialogoffen))
    lh[2].listbox.bind('<Double-Button-1>',
                       lambda event: funktionen.listendoppelklick(event, "vu", lh, fenster, fdialogoffen))

    hf.volslider.configure(command=lambda event: scale_volumeset(event, var_vlc))

    hf.button_ueberw_start.configure(command=lambda: startlisten(hf, var_vlc))
    hf.button_ueberw_stop.configure(command=lambda: stoplisten(var_vlc))

    # Menü einbinden
    # --------------

    hf.menue_dateimenue.entryconfig(
        1, command=lambda: funktionen.save_data(
            konfigurationsdatei,
            lh,  # 3 tkinter listen
            hf.volslider,  # Master Volume
            writeconfig))  # Funktion zum weitergeben und ausführen
    hf.menue_dateimenue.entryconfig(
        2, command=lambda: funktionen.reloadconfiganddisplay_tk(
            konfigurationsdatei,
            lh[0].listbox,  # Hotkey Listbox
            lh[1].listbox,  # Dateinamen Listbox
            lh[2].listbox,  # Volume Listbox
            hf.volslider,  # Master Volume
            readconfig))  # Funktion zum weitergeben und ausführen
    hf.menue_dateimenue.entryconfig(4, command=fenster.quit)
    hf.menue_help.entryconfig(2, command=lambda: funktionen.show_about(fenster))

    # Listen befüllen
    # ---------------
    funktionen.configinlistenladen(var_hotkeys, var_mastervolume,
                                   lh[0].listbox,
                                   lh[1].listbox,
                                   lh[2].listbox,
                                   hf.volslider)

    hf.volslider.set(float(var_mastervolume))
    fenster.mainloop()
