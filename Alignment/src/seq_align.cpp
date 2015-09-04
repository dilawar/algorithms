/***
 *       Filename:  seq_align.cpp
 *
 *    Description:  Algorithm to align two sequence
 *
 *        Version:  0.0.1
 *        Created:  2015-09-04
 *       Revision:  none
 *
 *         Author:  Dilawar Singh <dilawars@ncbs.res.in>
 *   Organization:  NCBS Bangalore
 *
 *        License:  GNU GPL2
 */

#include "seq_align.h"
#include <string>

SeqAlign::SeqAlign()
{
}

SeqAlign::~SeqAlign()
{
}

void SeqAlign::set_strings(string a, string b)
{
    a_ = a;
    b_ = b;
}
