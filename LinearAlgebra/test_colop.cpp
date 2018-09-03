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
#include <Eigen/Dense>
#include "column_op.hpp"

using namespace std;
using namespace Eigen;

int main(int argc, const char *argv[])
{
    MatrixXd m(4,4);
    m << 1,2,3,4, 0,1,0,0, 3,0,1,0 ,0,0,0,1;

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
    
    return 0;
}
