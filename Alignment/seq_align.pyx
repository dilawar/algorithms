# distutils: language = c++
# distutils: sources = src/seq_align.cpp

from cython.operator cimport dereference as deref, preincrement as inc
from libcpp.vector cimport vector
from libcpp.string cimport string

cdef extern from "src/seq_align.h":
    cdef cppclass SeqAlign:
        string a_, b_
        SeqAlign()
        void set_strings(string, string)

cdef class PySeqAlign:

    cdef SeqAlign *thisptr

    def __cinit__(self, a, b):
        self.thisptr = new SeqAlign()
        self.thisptr.set_strings(a, b)

    def __cinit__(self, a, b):
        self.thisptr = new SeqAlign()
        self.thisptr.set_strings(a, b)

    property a:
        def __get__(self): return self.thisptr.a_
        def __set__(self, a): self.thisptr.a_ = a
    
    property b:
        def __get__(self): return self.thisptr.b_
        def __set__(self, b): self.thisptr.b_ = b





