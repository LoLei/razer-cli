# razer-cli
Command line interface for controlling Razer devices

## About
With this command line interface you can configure your Razer peripherals, such
as keyboard and mouse, set their colors and effects, etc.

The most simple use case (for which this tool was originally developed) is to
use it in symbiosis with [`pywal`](https://github.com/dylanaraps/pywal). Then
this tool will set your Razer colors to Pywal's colors. See below for more
information.

## Installation
In the meantime:
```bash
git clone `https://github.com/LoLei/razer-cli.git`
cd razer-cli
./razer-cli.py
```
TBD: Pip or AUR installation.

## Usage
```bash
$ ./razer-x-color.py -h                                 
usage: razer-x-color.py [-h] [-e EFFECT] [-v] [-c COLOR [COLOR ...]] [-l]
                        [-ll] [-a]

optional arguments:
  -h, --help            show this help message and exit
  -e EFFECT, --effect EFFECT
                        set effect
  -v, --verbose         increase output verbosity
  -c COLOR [COLOR ...], --color COLOR [COLOR ...]
                        choose color (default: X color1), use one argument for
                        hex, or three for base10 rgb
  -l, --list_devices    list available devices
  -ll, --list_devices_long
                        list available devices and all their capabilities
  -a, --automatic       try to find colors and set them to all devices without
                        user arguments, uses X or pywal colors

```
<sup>This might be out of date, just run it with `-h` yourself to see the newest
options.</sup>  

### Example usage with Pywal
To get your mouse and keyboard to use Pywal's colors, simply start `razer-cli`
with the `-a` flag, after having executed `wal`: `./razer-cli.py -a`  
Example in action 
[here](https://github.com/LoLei/dotfiles/blob/master/exec-wal.sh).

#### Other examples
`$ ./razer-cli.py -e ripple -c ff0000`  
`$ ./razer-cli.py -e static -c ffffff`  

You can also leave out the color or the effect:  
`$ ./razer-cli.py -e breath_single`  
`./razer-cli.py -c 55ff99`

Currently this will imply the `-a` flag being used for the missing setting. I
plan on also having the option to reuse the current color/effect, if the
argument is missing, in the future.

## Dependencies
* [`openrazer`](https://github.com/openrazer/openrazer)
* [`xrdb`](https://www.archlinux.org/packages/extra/x86_64/xorg-xrdb/)

## Features to come
* Specifying devices, instead of using all devices
* Reusing current settings, in case user cannot enter the same command again or
  retrieve it from history
