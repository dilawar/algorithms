#!/bin/bash
set -e
set -x
ghc -O3 -prof -rtsopts ./variance_online.hs 
./variance_online +RTS -K100M -p -RTS
