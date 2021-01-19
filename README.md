# razer-cli
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-4-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
Command line interface for controlling Razer devices on Linux

## About
With this command line interface you can configure your Razer peripherals, such
as keyboard and mouse, set their colors and effects, etc.

The most simple use case (for which this tool was originally developed) is to
use it in symbiosis with [`pywal`](https://github.com/dylanaraps/pywal). Then
this tool will set your Razer colors to Pywal's colors. See below for more
information.

## Installation
[`pip install razer-cli`](https://pypi.org/project/razer-cli/)

## Usage
```
$ razer-cli -h
usage: razer-cli [-h] [-e EFFECT] [-v] [-c COLOR [COLOR ...]] [-l] [-ll] [-a]
                 [-d DEVICE [DEVICE ...]] [--dpi DPI] [-b BRIGHTNESS]

optional arguments:
  -h, --help            show this help message and exit
  -e EFFECT, --effect EFFECT
                        set effect
  -v, --verbose         increase output verbosity
  -c COLOR [COLOR ...], --color COLOR [COLOR ...]
                        choose color (default: X color1), use one argument for
                        hex, or three for base10 rgb
  -l, --list_devices    list available devices and their supported effects
  -ll, --list_devices_long
                        list available devices and all their capabilities
  -a, --automatic       try to find colors and set them to all devices without
                        user arguments, uses X or pywal colors
  -d DEVICE [DEVICE ...], --device DEVICE [DEVICE ...]
                        only affect these devices, same name as output of -l
  --dpi DPI             set DPI of device
  -b BRIGHTNESS, --brightness BRIGHTNESS
                        set brightness of device
```
<sup>This might be out of date, just run it with `-h` yourself to see the newest
options.</sup>  

### Example usage with Pywal
To get your mouse and keyboard to use Pywal's colors, simply start `razer-cli`
with the `-a` flag, after having executed `wal`: `razer-cli -a`  
Example in action 
[here](https://github.com/LoLei/dotfiles/blob/master/exec-wal.sh).

#### Other examples
`$ razer-cli -e ripple -c ff0000`  
`$ razer-cli -e static -c ffffff`  

You can also leave out the color or the effect:  
`$ razer-cli -e breath_single`  
`$ razer-cli -c 55ff99`

Currently this will imply the `-a` flag being used for the missing setting. I
plan on also having the option to reuse the current color/effect, if the
argument is missing, in the future.

#### Effects
Effects are listed in
[`razer_cli/settings.py`](https://github.com/LoLei/razer-cli/blob/master/razer_cli/settings.py).
The effects that are supported per device can be listed with `razer-cli -l[l]`.
Some of the built-in effects or not implemented yet. If such an effect is
chosen, a notice will be logged. There are also custom effects that do not exist
normally, such as `multicolor`, which is described in the same file.

Here's a showcase of that effect:
<p align="center">
  <img src="https://raw.githubusercontent.com/LoLei/razer-cli/master/images/randomshowcase.gif">
</p>

#### Other symbiosis tools
* [`wpgtk`](https://github.com/deviantfero/wpgtk)
* [`Chameleon`](https://github.com/GideonWolfe/Chameleon)

## Dependencies
* [`openrazer`](https://github.com/openrazer/openrazer)
  * :warning: Do not install `openrazer` from [pip](https://pypi.org/project/openrazer/), which is something else.
  * Instead install it from one of the various package managers of your distribution.
* [`xrdb`](https://www.archlinux.org/packages/extra/x86_64/xorg-xrdb/)
  * Also available on most distros.

## Disclaimer
Not all devices have been tested, but basic effects should work everywhere. Some guesswork is being done as to what capabilities are supported on specific devices. If you need more advanced configuration, consider using the GUIs [Polychromatic](https://github.com/polychromatic/polychromatic/), [RazerGenie](https://github.com/z3ntu/RazerGenie) or [RazerCommander](https://gitlab.com/gabmus/razerCommander) which have specific implementations for most devices.
  
Feel free to open feature request issues or PRs.

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/Ansis100"><img src="https://avatars2.githubusercontent.com/u/35926716?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Ansis</b></sub></a><br /><a href="https://github.com/LoLei/razer-cli/commits?author=Ansis100" title="Code">💻</a></td>
    <td align="center"><a href="https://t1c.dev"><img src="https://avatars0.githubusercontent.com/u/44733677?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Kainoa Kanter</b></sub></a><br /><a href="#ideas-ThatOneCalculator" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="https://www.ifohancroft.com"><img src="https://avatars0.githubusercontent.com/u/3461282?v=4?s=100" width="100px;" alt=""/><br /><sub><b>IFo Hancroft</b></sub></a><br /><a href="https://github.com/LoLei/razer-cli/issues?q=author%3Aifohancroft" title="Bug reports">🐛</a> <a href="#userTesting-ifohancroft" title="User Testing">📓</a></td>
    <td align="center"><a href="https://github.com/GM-Script-Writer-62850"><img src="https://avatars2.githubusercontent.com/u/564653?v=4?s=100" width="100px;" alt=""/><br /><sub><b>GM-Script-Writer-62850</b></sub></a><br /><a href="https://github.com/LoLei/razer-cli/commits?author=GM-Script-Writer-62850" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
