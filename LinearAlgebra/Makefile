all : ./test_colop

./test_colop : test_colop.cpp ./column_op.hpp
	g++ -O3 -I/usr/include/eigen3 -std=c++11 $<  -o $@
