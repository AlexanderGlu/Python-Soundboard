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
import tkinter_gui.eintragbearbeitendialog as eintragbearbeitendialog
import tkinter_gui.about as about


# tkinter gui funktionen
# ----------------------
# TODO evtl in tkinter gui datei einbauen (hauptfenster.py)


def configinlistenladen(var_hotkeys, var_volume,
                        gui_hotkeyliste,
                        gui_dateinamenliste,
                        gui_volumeliste,
                        gui_volumeslider):
    """
    Befüllt die Tkinter GUI mit den geladenen Daten

    * var_hotkeys (list) Enthält die Hotkeys, Dateinamen, Volume
    * var_volume (int) Setzt den Master Volume Regler
    * gui_hotkeyliste (tkinter.Listbox) Die zu befüllende tkinter Liste für Hotkeys
    * gui_dateinamenliste (tkinter.Listbox) Die zu befüllende tkinter Liste für Dateinamen
    * gui_volumeliste (tkinter.Listbox) Die zu befüllende tknter Liste für Volume
    * gui_volumeslider (tkinter.Slider) Der einzustellende tkinter Slider für Mastervolume

    :param var_hotkeys:
    :param var_volume:
    :param gui_hotkeyliste:
    :param gui_dateinamenliste:
    :param gui_volumeliste:
    :param gui_volumeslider:
    :return:
    """
    gui_dateinamenliste.delete(0, tk.END)
    gui_hotkeyliste.delete(0, tk.END)
    gui_volumeliste.delete(0, tk.END)
    for iterator in var_hotkeys:
        gui_hotkeyliste.insert(tk.END, str(iterator[0]))
        gui_dateinamenliste.insert(tk.END, str(iterator[1]))
        gui_volumeliste.insert(tk.END, str(iterator[2]))
    listboxenneuereintraghinzufuegen(gui_hotkeyliste, gui_dateinamenliste, gui_volumeliste)
    gui_volumeslider.set(int(var_volume))


def reloadconfiganddisplay_tk(configdatei,
                              gui_hotkeyliste,
                              gui_dateinamenliste,
                              gui_volumeliste,
                              gui_volumeslider, readconfigfunktion):
    """
    Ruft beide nötigen funktionen zum config laden und in listen laden auf

    * configdatei (string) Der Pfad zur Ini ähnlichen configdatei
    * gui_hotkeyliste (Listbox) wird gefüllt mit den Hotkey-Daten und zurückgegeben
    * gui_dateinamenliste (Listbox) Listen Objekt zum Befüllen
    * gui_volumeliste (Listbox) Listen Objekt zum Befüllen
    * gui_volumeslider (Scale) Objekt um das Mastervolume zu setzen
    * readconfigfunktion (function) zum laden der Konfiguration

    :param configdatei:
    :param gui_hotkeyliste:
    :param gui_dateinamenliste:
    :param gui_volumeliste:
    :param gui_volumeslider:
    :param readconfigfunktion:
    :return hotkeys, var_volume:
    """
    hotkeys, mastervolume = readconfigfunktion(configdatei)
    configinlistenladen(hotkeys, mastervolume,
                        gui_hotkeyliste,
                        gui_dateinamenliste,
                        gui_volumeliste,
                        gui_volumeslider)
    return hotkeys, mastervolume


def save_data(configdatei,
              gui_list_handler,
              gui_volumeslider,
              writeconfigfunktion):
    """
    Lädt die Daten aus den Listen und ruft das Speichern in der Konfigurationsdatei auf

    * configdatei (string) Der Pfad zur Ini ähnlichen configdatei
    * gui_list_handler (object) Listbox 3x
    * gui_volumeslider (Scale) Objekt um das Mastervolume zu setzen
    * writeconfigfunktion (function) zum laden der Konfiguration

    :param configdatei:
    :param gui_list_handler:
    :param gui_volumeslider:
    :param writeconfigfunktion:
    :return :
    """
    hkvar = []
    count = 0
    for eintrag in gui_list_handler[0].listbox.get(0, tk.END):
        if not eintrag == "Neuer Eintrag...":
            hkvar.append([gui_list_handler[0].listbox.get(count),
                         gui_list_handler[1].listbox.get(count),
                         int(gui_list_handler[2].listbox.get(count))])
            count += 1
    mastervolume = int(float(gui_volumeslider.get()))
    writeconfigfunktion(configdatei, hkvar, mastervolume)


def listboxenneuereintraghinzufuegen(gui_hotkeyliste, gui_dateinamenliste, gui_volumeliste):
    """
    Fügt dummy Einträge in die Listen ein die zum erstellen weiterer Einträge dienen

    * gui_hotkeyliste (tkinter.Listbox) Die zu befüllende tkinter Liste für Hotkeys
    * gui_dateinamenliste (tkinter.Listbox) Die zu befüllende tkinter Liste für Dateinamen
    * gui_dateinamenliste (tkinter.Listbox) Die zu befüllende tkinter Liste für Dateinamen
    * gui_volumeliste (tkinter.Listbox) Die zu befüllende tknter Liste für Volume

    :param gui_hotkeyliste:
    :param gui_dateinamenliste:
    :param gui_volumeliste:
    :return:
    """
    gui_dateinamenliste.insert(tk.END, "Neuer Eintrag...")
    gui_hotkeyliste.insert(tk.END, "Neuer Eintrag...")
    gui_volumeliste.insert(tk.END, "Neu...")


def listenrechtsklick(event, eventlistbox, hauptfenster, vlc_dictionary, volumesetplayer):
    """
    Sorgt dafür, dass der richtige Eintrag aus der Liste/Listen gefunden wird und gibt es an die play funktion weiter

    :param event: None - keine funktion
    :param eventlistbox: (Object) -mit der ListScroll die das Event aufruft
    :param hauptfenster: (Object) Enthält das Hauptfenster
    :param vlc_dictionary: (Dict) Enthält "instance": vlc Instanz, "player": vlc palyer,
     "einzelvolume": volume zum abzuspielenden Eintrag
    :param volumesetplayer: Enthält die Funktion zum Setzen der Lautsärke vor dem abspielen
    :return:
    """
    y = str(str(event).split()[5]).strip("y=>")
    auswahl = eventlistbox.listbox.nearest(y)
    if eventlistbox.listbox.get(auswahl) == "Neuer Eintrag...":
        return
    # Die nearest Funktion gibt mit hilfe von y den Eintrag an Position y wieder (relative Koordinate)
    dateiname = hauptfenster.listenhandler[1].listbox.get(auswahl)
    vlc_dictionary["einzelvolume"] = int(hauptfenster.listenhandler[2].listbox.get(auswahl))
    listenrechtsklick_play(dateiname, hauptfenster, vlc_dictionary, volumesetplayer)


def listenrechtsklick_play(dateiname, hauptfenster, vlc_dictionary, volumesetplayer):
    """
    Wird von "listenrechtsklick" aufgerufen und übergibt an vlc die abzuspielenden Daten

    :param dateiname: (string) Dateiname/Pfad
    :param hauptfenster:  (Object) Enthält das Hauptfenster
    :param vlc_dictionary: (Dict) Enthält "instance": vlc Instanz, "player": vlc palyer,
     "einzelvolume": volume zum abzuspielenden Eintrag
    :param volumesetplayer: Enthält die Funktion zum Setzen der Lautsärke vor dem abspielen
    :return:
    """
    if dateiname != "Neuer Eintrag...":
        media = vlc_dictionary["instance"].media_new(dateiname)
        volumesetplayer(int(float(hauptfenster.volslider.get())), vlc_dictionary)
        vlc_dictionary["player"].set_media(media)
        vlc_dictionary["player"].play()


def listendoppelklick(event, var_ursprungsliste, gui_listenhandler, root_fenster, fdialogoffen):
    """
    Ruft den Dialog zum bearbeiten des ausgewählten Eintrags auf

    :param event: Keine Funktion
    :param var_ursprungsliste: (string) enthält "hk"-Hotkeyliste "dn"-Dateinamenliste oder "vu"-Volumeliste
    :param gui_listenhandler: (Object) Enthält die 3 ListScoll
    :param root_fenster:
    :param fdialogoffen: Enthält die Funktion zum setzen der bool ob ein Dialog geöffnet ist
    :return:
    """
    del event
    dialogoffen = fdialogoffen("get", None)
    if not dialogoffen:
        fdialogoffen("set", True)
        hklist = gui_listenhandler[0].listbox
        dnlist = gui_listenhandler[1].listbox
        vulist = gui_listenhandler[2].listbox
        aktuelle_auswahl = None
        if var_ursprungsliste == "hk":
            aktuelle_auswahl = hklist.curselection()[0]
        elif var_ursprungsliste == "dn":
            aktuelle_auswahl = dnlist.curselection()[0]
        elif var_ursprungsliste == "vu":
            aktuelle_auswahl = vulist.curselection()[0]

        if hklist.get(aktuelle_auswahl) == "Neuer Eintrag...":
            editdialog = eintragbearbeitendialog.EintragBearbeitenDialog(root_fenster, aktuelle_auswahl)
        else:
            # TODO Platzierung des neuen Dialoges bestimmen? über - neben dem Hauptfenster - Beim cursor?

            var_hk = hklist.get(aktuelle_auswahl)
            var_dn = dnlist.get(aktuelle_auswahl)
            var_vu = int(vulist.get(aktuelle_auswahl))
            editdialog = eintragbearbeitendialog.EintragBearbeitenDialog(root_fenster, aktuelle_auswahl,
                                                                         var_hk, var_dn, var_vu)
        editdialog.button_abbrechen["command"] = lambda: editdialog_abbrechen(editdialog, fdialogoffen)
        editdialog.button_uebernehmen["command"] = lambda: editdialog_uebernehmen(gui_listenhandler, editdialog,
                                                                                  fdialogoffen)
        root_fenster.wait_window(editdialog.dialogfenster)


def editdialog_abbrechen(editdialog_handler, fdialogoffen):
    """
    Schließt das Dialogfenster

    :param editdialog_handler: (Object) Endhält den Edit-Dialog
    :param fdialogoffen: (Funktion) Enthält die Funktion zum setzen der bool ob ein Dialog geöffnet ist
    :return:
    """
    editdialog_handler.dialogfenster.destroy()
    fdialogoffen("set", False)


def editdialog_uebernehmen(gui_listenhandler, dialog_handler, fdialogoffen):
    """
    Speichert die Eingaben in den Listen und Beendet den Dialog

    :param gui_listenhandler: (Object) Enthält die 3 ListScoll
    :param dialog_handler: (Object) Endhält den Edit-Dialog
    :param fdialogoffen: (Funktion) Enthält die Funktion zum setzen der bool ob ein Dialog geöffnet ist
    :return:
    """
    gui_listenhandler[0].listbox.delete(dialog_handler.aktuelle_auswahl)
    gui_listenhandler[0].listbox.insert(dialog_handler.aktuelle_auswahl, dialog_handler.entry_hk.get())
    gui_listenhandler[1].listbox.delete(dialog_handler.aktuelle_auswahl)
    gui_listenhandler[1].listbox.insert(dialog_handler.aktuelle_auswahl, dialog_handler.entry_dn.get())
    gui_listenhandler[2].listbox.delete(dialog_handler.aktuelle_auswahl)
    gui_listenhandler[2].listbox.insert(dialog_handler.aktuelle_auswahl, dialog_handler.entry_vu.get())

    dialog_handler.dialogfenster.destroy()
    fdialogoffen("set", False)


def listedeketekey(event, aktuelle_listscroll, lh):
    """
    Entfernt ausgewählte Einträge aus den Listen

    :param event: Keine Funktion
    :param aktuelle_listscroll: (Object) Enthält die ListScroll, die das Event aufgerufen hat
    :param lh: (Object) Enthält die 3 ListScroll
    :return:
    """
    del event
    aktuelle_auswahl = aktuelle_listscroll.listbox.curselection()[0]
    if not(lh[0].listbox.get(aktuelle_auswahl) == "Neuer Eintrag..."):
        if lh[0].listbox.size() > 1:
            lh[0].listbox.delete(aktuelle_auswahl)
            lh[1].listbox.delete(aktuelle_auswahl)
            lh[2].listbox.delete(aktuelle_auswahl)
        else:
            print("Die Liste ist schon leer oder ein anderes Problem")


def show_about(root_fenster):
    """
    Öffnet das About Fenster

    :param root_fenster:
    :return:
    """
    aboutdialog = about.AboutDialog(root_fenster)
    root_fenster.wait_window(aboutdialog.dialogfenster)
