#!/bin/bash
set -e
set -x
ghc -O3 -rtsopts ./variance_online.hs 
./variance_welford #+RTS -K100M -RTS
