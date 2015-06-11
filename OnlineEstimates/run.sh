#!/bin/bash
set -e
set -x
#ghc -O3 -fllvm ./variance_welford.hs 
ghc -O3 -rtsopts ./variance_welford.hs 
./variance_welford #+RTS -K100M -RTS
