# razer-x-color
Set Razer peripherals to X resources colors 

## About
This script reads `color1` from the X resources via `xrdb` and then sets
available RGB/Chroma Razer peripherals, such as keyboard and mouse, to use that
color. Effects can be chosen as well.  
It can be used in symbiosis with [`pywal`](https://github.com/dylanaraps/pywal),
which sets this `color1` as its primary color.

## Installation
In the meantime:
```bash
git clone `https://github.com/LoLei/razer-x-color.git`
cd razer-x-color
# Execute wal before so a colorscheme is generated
# if there are no colors defined in the X resources
python razer-x-color.py
```
TBD: Pip or AUR installation.

## Usage
```bash
$ python razer-x-color.py -h
usage: razer-x-color.py [-h] [--effect {static,breath,reactive,ripple}] [-v]

optional arguments:
  -h, --help            show this help message and exit
  --effect {static,breath,reactive,ripple}
                        set effect (default: static)
  -v, --verbose         increase output verbosity
```
<sup>This might be out of date, just run it with `-h` yourself to see the newest options.</sup>  
Example in action 
[here](https://github.com/LoLei/dotfiles/blob/master/exec-wal.sh).

### Dependencies
* [`openrazer`](https://github.com/openrazer/openrazer)
* [`xrdb`](https://www.archlinux.org/packages/extra/x86_64/xorg-xrdb/)
