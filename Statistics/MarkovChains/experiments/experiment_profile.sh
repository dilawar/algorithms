#!/bin/bash - 
#===============================================================================
#
#          FILE: experiment_profile.sh
# 
#         USAGE: ./experiment_profile.sh 
# 
#   DESCRIPTION:  Profiling the system of Markov chain.
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Dilawar Singh (), dilawars@ncbs.res.in
#  ORGANIZATION: NCBS Bangalore
#       CREATED: 08/07/2016 11:54:56 AM
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error
PYTHON=`which python`

for (( i = 1; i < 20; i++ )); do
    echo "Running a system of size $i"
    $PYTHON ../markov_chains.py -s $i -p
done
