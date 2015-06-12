#!/bin/bash
set -e
set -x
if [[ "$1" == "prof" ]]; then
    HSFLAGS="-rtsopts -prof -O3"
    HSRUN="+RTS -K100M -p"
else
    HSFLAGS="-rtsopts -O3"
    HSRUN="+RTS -K100M"
fi
ghc $HSFLAGS ./variance_online.hs 
./variance_online $HSRUN -RTS
