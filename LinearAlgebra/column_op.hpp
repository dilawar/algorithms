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

using namespace std;

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
    Eigen::MatrixXd temp = m;
    const size_t N = m.rows();

    // Keep the column operations in this vector.
    std::vector< column_op_t > vecColOps;
    std::vector<double> diag(N, 1);

    // We have to turn the matrix to column reduced echleon form. 
    for (size_t i = 0; i < N; i++) 
    {
        double p = m(i, i);
        if( p == 0.0 )
            continue;

        for (size_t ii = 0; ii < N; ii++) 
        {
            if( i == ii )
                continue;
            double s = - m(i,ii) / m(i,i);
            if( s == 0.0)
                continue;
            assert( s != 0 );
            m.col(ii) += s * m.col(i);
            vecColOps.push_back( {ii, i, s} );
        }
        diag[i] = m(i, i);
    }

    apply_column_operations( m, vecColOps );
    
    // rescale the column and rows depending on the diagonal.
    for( size_t i = 0; i < diag.size(); i++ )
    {
        if( diag[i] == 1 )
            continue;
        m.col( i ) /= diag[i];
        m.row( i ) /= diag[i];
    }
}


#endif /* end of include guard: COLUMN_OP_H */
