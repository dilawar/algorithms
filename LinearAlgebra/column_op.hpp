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

#include <vector>
#include <tuple>

typedef std::tuple<size_t, size_t, double> column_op_t;

void apply_column_operation( Eigen::MatrixXd & m, const column_op_t &p )
{
    size_t c1 = std::get<0>(p);
    size_t c2 = std::get<1>(p);
    double s = std::get<2>(p);
    m.col(c1) += s * m.col(c2);
}

void apply_column_operations( Eigen::MatrixXd &m, const std::vector<column_op_t> &ps)
{
    for(auto &p : ps)
        apply_column_operation(m, p);
}

/* --------------------------------------------------------------------------*/
/**
 * @Synopsis  Invert a matrix in place.
 *
 * @Param m  Matrix.
 */
/* ----------------------------------------------------------------------------*/
void invert( Eigen::MatrixXd& m )
{
    std::cout << "Inverting ... \n" << m << std::endl;
    const size_t N = m.rows();

    // Keep the column operations in this vector.
    vector<perm_to_mat> vecColOps;
    for (size_t i = 0; i < N; i++) 
    {
        double p = m(i, i);
        if( p == 0.0 )
            continue;

        for (size_t ii = i; ii < N; ii++) 
        {
        }
    }


}


#endif /* end of include guard: COLUMN_OP_H */
