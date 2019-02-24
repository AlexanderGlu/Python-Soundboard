# Python-Soundboard
### Soundboard zur Wiedergabe von Audio-Dateien per Tastatur (Hotkeys und Tastenkombinationen) geschrieben in Python

> Die Idee und initiale Arbeit (Plugins finden, ersten Code zusammenstellen) stammt von [TuxPlayDE](https://www.twitch.tv/tuxplayde "TuxPlayDE - Twitch").

> Zum Abspielen der Audiodateien wird [VLC](https://www.videolan.org/vlc/) verwendet und benötigt!

> Das UI nutzt in dieser Version derzeit (noch?) "Tkinter".

> __Das Programm muss unter Linux mit _'sudo'_ (Root-Rechten) ausgeführt werden, um zugriff auf die Tasteneingaben zu bekommen! (Anforderung der "keyboard"-Bibliothek)__


#### Was wird benötigt? (Wenn nicht schon vorhanden!)
- Python in Version 3
- Tkinter
- VLC

###### Unter Debian/Ubuntu/Mint zum Beispiel:
```
sudo apt install python3
sudo apt install python3-tk
sudo apt install vlc
```

#### Was noch anzupassen ist:
- Alles etwas schöner/professioneller machen :-)
- Aktuell werden noch Textausgaben in der Konsole gemacht, die nicht mehr gebraucht werden.
- Wenn die Dateipfade zu lang werden kann man nur noch den Anfang lesen: Scrollbalken wären noch gut
- Es wird noch nicht berücksichtigt, dass die Config-Datei nicht da sein könnte
- Die Shortcuts, die ins Eingabefeld eingegeben werden können (direkt) werden noch nicht gegengecheckt.
- Evtl. könnte es funktionieren, dass man den Fokus in den Listen verändern kann, während der Dialog zum Shortcut aufnehmen offen ist.
- Sicher noch einiges mehr.
