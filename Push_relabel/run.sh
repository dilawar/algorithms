#!/bin/bash 
g++ -Wall -std=c++0x -DDEBUG -DEX2 push_relabel.cc -o push_relabel -lboost_graph && ./push_relabel 
