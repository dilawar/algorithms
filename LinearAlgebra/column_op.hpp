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
    m.col(std::get<0>(p)) += std::get<2>(p) * m.col( std::get<1>(p) );
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

/* --------------------------------------------------------------------------*/
/** NOTE: This method is horribly slow.
 * @Synopsis  Invert a matrix using elementary column operations.
 *
 * @Param m   Given matrix.
 *
 * @Returns Inverted matrix.
 *
 * A = IP1 P2 P3 .. Pn
 * A^-1 = Pn^-1 Pn-1^-1 .. P1^-1 
 *
 * Where Pn^-1 is Pn[i,j] = -P[i,j] /= 0 e.g.
 *     P                            p^-1
 *  [[ 1, -2, -3, -4],           [[1., 2., 3., 4.],
 *    [ 0,  1,  0,  0],            [0., 1., 0., 0.],
 *    [ 0,  0,  1,  0],            [0., 0., 1., 0.],
 *    [ 0,  0,  0,  1]]            [0., 0., 0., 1.]]            
 * 
 * NOTE: We use the new method.
 *          D = A P1 P2 where S is a diagnonal matrix.
 *
 *          D P2^-1 P1^-1 = A 
 *          P1 P2 D^-1  = A^-1
 *
 *      D^-1 is cheap to compute since it is a diagonal matrix. We are left with 3 multiplications.
 *
 */
/* ----------------------------------------------------------------------------*/
Eigen::MatrixXd invert_horribly_slow( const Eigen::MatrixXd& mat )
{
    Eigen::MatrixXd m(mat);
    const size_t N = m.rows();

    // We have to turn the matrix to column reduced echleon form. 
    Eigen::MatrixXd res = Eigen::MatrixXd::Identity(N, N);
    for (size_t i = 0; i < N; i++) 
    {
        double p = m(i, i);
        if( p == 0.0 )
            continue;

        Eigen::MatrixXd e = Eigen::MatrixXd::Identity(N, N);
        for (size_t ii = 0; ii < N; ii++) 
        {
            if( i == ii )
                continue;
            double s = - m(i,ii) / m(i,i);
            if( s == 0.0)
                continue;
            assert( s != 0 );
            m.col(ii) += s * m.col(i);
            e(i, ii) = s;
        }

        res *= e;
    }

    for (size_t i = 0; i < N; i++) 
    {
        if( m(i,i) != 1.0 && m(i,i) != 0 )
            res.col(i) /= m(i,i);
    }
    return res;
}


#endif /* end of include guard: COLUMN_OP_H */
