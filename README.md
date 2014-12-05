YMP
===


This media player currently supports Youtube playlists and
exports a [MPRIS2](http://specifications.freedesktop.org/mpris-spec/latest/) interface to control it.

Recommended gnome plugin:
* https://extensions.gnome.org/extension/55/media-player-indicator/


![YMP Screenshot](https://raw.githubusercontent.com/wiki/Dav1dde/ymp/screenshots/scrot1.png)


Features:
* Youtube playlists
* Grooveshark playlists
* Soundcloud playlists
* Complete MPRIS2 interface


## Installation ##

YMP currently uses libVLC as a backend and is written entirely in Python.

Dependencies:
* libVLC
* Python 3
* Python 3 Dbus
* [pafy](https://pypi.python.org/pypi/Pafy/0.3.66)
* [pygrooveshark](https://github.com/koehlma/pygrooveshark)
* [soundcloud](https://pypi.python.org/pypi/soundcloud/0.4.1)

In the sections below is described how to install the dependencies on certain systems.
After installing these, you can install `ymp` systemwide with the command `sudo setup.py install`
or you can start `ymp` like that: `python -m ymp -h`.

If you decide to install `ymp` globally, you might also want to install the `ymp.dekstop` and
`ymp.png`/`ymp.svg` files to the appropriate places (e.g. `/usr/share/applications/ymp.desktop`,
`/usr/share/icons/hicolor/48x48/apps/ymp.png` and `/usr/share/icons/hicolor/scalable/apps/ymp.svg`
or the matching folders in your home directory).

### Ubuntu/Debian ###

```
sudo apt-get install python3 python3-pip python3-dbus libvlc-dev
```

```
sudo pip3 -r requirements.txt
```

### Arch Linux ###

```
pacman -S vlc python python-pip python-dbus
```

```
sudo pip3 -r requirements.txt
```

## Configuration ##

Configuration can be done via commandline:

```
usage: ymp [-h] [--config FILE] [-f FILE] [-p [PLAYLIST [PLAYLIST ...]]] [-s]
           [--soundcloud SOUNDCLOUD] [-r] [--backend BACKEND]
           [--backend-options BACKEND_OPTIONS]

optional arguments:
  -h, --help            show this help message and exit
  --config FILE         Path to a configfile
  -f FILE, --playlist-file FILE
                        Path to a newline separated file of playlists
  -p [PLAYLIST [PLAYLIST ...]], --playlist [PLAYLIST [PLAYLIST ...]]
                        List of playlists
  -s, --shuffle         Shuffle songs of a playlist
  --soundcloud SOUNDCLOUD
                        Soundcloud client id, can be generated for free
  -r, --repeat          Play playlists on repeat
  --backend BACKEND     Sound backend for playing music. Currently only
                        supports VLC
  --backend-options BACKEND_OPTIONS
                        String containing additional options for the backend,
                        this is backend specfic!
```

Or through a config-file located in `~/.config/ymp/ymp.conf` (or the one passed via `--config`):

```
[ymp]
shuffle=true
repeat=true
playlist_file=~/Music/ymp/playlists.lst
soundcloud=*SOUND CLOUD KEY*
backend=VLC
```

The config is a simple ini file, with only one section called `ymp`, if using a config file
you most likely also want to use a playlist-file. A playlist file is a newline separated file
of youtube/grooveshark/soundcloud playlists.

### Soundcloud ###

Youtube and Grooveshark work out of the box, but for Soundcloud you need an API key, you can
get one for free from `http://soundcloud.com/you/apps/new` (you need a Soundcloud account),
register `ymp` (any name possible) and save the Soundcloud API key, that's it.
