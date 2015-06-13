#!/bin/bash
set -e
set -x
if [[ "$1" == "prof" ]]; then
    HSFLAGS="-rtsopts -prof -fprof-auto"
    HSRUN="+RTS -K300M -p"
else
    HSFLAGS="-rtsopts -O3"
    HSRUN="+RTS -K100M"
fi
ghc $HSFLAGS ./variance_online.hs 
time ./variance_online $HSRUN -RTS
