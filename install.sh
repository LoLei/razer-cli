#!/bin/bash

# Adapted from https://github.com/GideonWolfe/Zathura-Pywal/blob/master/install.sh

echo "Started installation..."

# Set a path for local binaries
# add this to your path
BINPATH=$HOME/.local/bin

# Make sure this path exists
mkdir -p "$BINPATH"

# Make the scripts executable
chmod u+x ./razer-cli.py

# Link the scripts to the PATH
ln -s "$(pwd)/razer-cli.py" "$BINPATH/razer-cli"

# Add user bin path to local bashrc
while true; do
  read -p "Do you want to add $BINPATH to your PATH by appending to your bashrc? [y/n] " yn
  case $yn in
    [Yy]* ) echo "Yes";
            echo export PATH="$BINPATH:\$PATH" >> $HOME/.bashrc;
            source $HOME/.bashrc;
            break;;
    [Nn]* ) echo "No";break;;
    * ) echo "Please answer yes or no.";;
  esac
done

# Symlink to to /usr/bin if wanted
# Needed to have it recognized via i3 config
ROOT_SYMLINK=0
while true; do
  read -p "Do you want to create a symlink in /usr/bin? (Required for i3 compatibility, requires root) [y/n] " yn
  case $yn in
    [Yy]* ) echo "Yes";
            ROOT_SYMLINK=1
            break;;
    [Nn]* ) echo "No";break;;
    * ) echo "Please answer yes or no.";;
  esac
done

if [ $ROOT_SYMLINK == 1 ];
then
  if [ $EUID != 0 ];
  then
    sudo ln -s "$(pwd)/razer-cli.py" "/usr/bin/razer-cli"
  else
    ln -s "$(pwd)/razer-cli.py" "/usr/bin/razer-cli"
  fi
fi

cat <<EOM
Installation finished.
EOM
