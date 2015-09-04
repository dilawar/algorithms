/***
 *       Filename:  seq_align.h
 *
 *    Description:  Align two sequences.
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

#ifndef SEQ_ALIGN_H
#define SEQ_ALIGN_H

#include <string>

using namespace std;

class SeqAlign
{
    public:
        SeqAlign();
        ~SeqAlign();

    private:
        /* data */
        string a_;
        string b_;
};
#endif /* end of include guard: SEQ_ALIGN_H */
