# razer-x-color

This script reads `color1` from the X resources via `xrdb` and then sets
available RGB/Chroma Razer peripherals, such as keyboard and mouse, to use that
color.  
It can be used in symbiosis with [`pywal`](https://github.com/dylanaraps/pywal),
which sets this `color1` as its primary color. See for example
[here](https://github.com/LoLei/dotfiles/blob/master/exec-wal.sh).

## Dependencies
* [`openrazer`](https://github.com/openrazer/openrazer)
* [`xrdb`](https://www.archlinux.org/packages/extra/x86_64/xorg-xrdb/)
