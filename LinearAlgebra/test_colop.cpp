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
    m << 1, 2, 3, 4
        , 0, 1, 0, 0
        , 0, 0, 1, 0
        , 0, 0, 0, 1;

    // A column operator.
    column_op_t p1 = {2, 1, -1.5 };

    cout << "Matrix before " << endl << m << endl;
    apply_column_operation( m, p1 );
    cout << "Matrix after " << endl << m << endl;


    
    return 0;
}
