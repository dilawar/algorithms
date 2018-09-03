/***
 *    Description:  Column Operations.
 *
 *        Created:  2018-09-03

 *         Author:  Dilawar Singh <dilawars@ncbs.res.in>
 *   Organization:  NCBS Bangalore
 *        License:  MIT License
 */

#ifndef COLUMN_OP_H

#define COLUMN_OP_H

typedef std::tuple<size_t, size_t, double> column_op_t;

void apply_column_operation( Eigen::MatrixXd & m, const column_op_t &p )
{
    size_t c1 = std::get<0>(p);
    size_t c2 = std::get<1>(p);
    double s = std::get<2>(p);
    m.col(c1) += s * m.col(c2);
}



#endif /* end of include guard: COLUMN_OP_H */
