/***
 *    Description:  Column operations.
 *
 *        Created:  2018-09-03

 *         Author:  Dilawar Singh <dilawars@ncbs.res.in>
 *   Organization:  NCBS Bangalore
 *        License:  MIT License
 */

#include <iostream>
#include <tuple>
#include <ctime>
#include <Eigen/Dense>
#include "column_op.hpp"

using namespace std;
using namespace Eigen;

int test( )
{
    MatrixXd m(4,4);
    m << 1,2,3,4, 0,1,0,0, 3,0,1,0 ,0,0,0,1;
    auto m1 = m;

    // A column operator.
    column_op_t p1 = {2, 1, -1.5 };
    column_op_t p2 = {0, 2, -0.5 };

    apply_column_operations( m, { p1, p2 } );
    MatrixXd expected(4,4);
    expected << 1,2,0,4,  0.75,1,-1.5,0,  2.5,0,1,0,  0,0,0,1;

    if( expected != m )
    {
        cerr << "Warn: test failed" << endl;
        cerr << "Got " << endl << m << endl << " expected " << endl << expected << endl;
    }

    // Invert a matrix.
    auto m11 = invert2( m1 );
    cout << "testing inverse ";
    if( m11 != m1.inverse() )
    {
        cout << "Expected\n" << m1.inverse() << endl
            << "Got\n" << m11 << endl;
        throw;
    }
    cout << "     ... PASSED!" << endl;
    
    return 0;
}

void benchmark( )
{
    for (size_t i = 1; i < 12; i++) 
    {
        const size_t N = (size_t)pow(2, i);
        Eigen::MatrixXd m = MatrixXd::Random(N, N);

        clock_t t0 = clock();
        auto mInv = m.inverse();
        clock_t t1 = clock();
        double eigenT = (double)(t1-t0)/CLOCKS_PER_SEC;

        MatrixXd m1(m);
        t0 = clock();
        invert( m1 );
        t1 = clock();

        if( (m1-mInv).norm() > 1e-6 )
        {
            cout << "Got " << endl << m1 << endl;
            cout << "Expected " << endl << mInv << endl;
            cout<< "Error : " << endl << (m1 - mInv).norm() << endl;
            throw;
        }

        cout << N << ' ' << (double)(t1-t0) / CLOCKS_PER_SEC <<  ' ' << eigenT << endl;
    }

}

int main(int argc, const char *argv[])
{
    test( );
    benchmark( );
    return 0;
}
