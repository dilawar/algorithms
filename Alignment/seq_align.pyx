# distutils: language = c++
# distutils: sources = src/seq_align.cpp

cdef extern from "src/seq_align.h":
    cdef cppclass SeqAlign:
        SeqAlign() except +

cdef class PySeqAlign:
    cdef SeqAlign *thisptr

    def __cinit__(self):
        self.thisptr = new SeqAlign()
