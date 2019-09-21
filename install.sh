#!/bin/sh

# Adapted from https://github.com/GideonWolfe/Zathura-Pywal/blob/master/install.sh

# Set a path for local binaries
# add this to your path
BINPATH=$HOME/.local/bin

# make sure this path exists
mkdir -p "$BINPATH"

# make the scripts executable
chmod u+x ./razer-cli.py

# link the scripts to the PATH
ln -s "$(pwd)/razer-cli.py" "$BINPATH/razer-cli"

# Add user bin path to local bashrc
while true; do
    read -p "Do you want to add $BINPATH to your PATH
    by appending to your bashrc? [y/n] " yn
    case $yn in
        [Yy]* ) echo "Yes";
          echo export PATH="$BINPATH:\$PATH" >> $HOME/.bashrc;
          source $HOME/.bashrc
          break;;
        [Nn]* ) echo "No";break;;
        * ) echo "Please answer yes or no.";;
    esac
done

cat <<EOM
Installed to "$BINPATH"
Make sure "$BINPATH" is in your PATH
you may do so by adding the following line to your bashrc or zshrc
export PATH="$BINPATH:\$PATH"
EOM
