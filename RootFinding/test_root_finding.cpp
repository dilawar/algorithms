/*
 * =====================================================================================
 *
 *       Filename:  test_root_finding.cpp
 *
 *    Description:  Test my root finding algorithm.
 *
 *        Version:  1.0
 *        Created:  04/14/2016 11:44:21 AM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Dilawar Singh (), dilawars@ncbs.res.in
 *   Organization:  NCBS Bangalore
 *
 * =====================================================================================
 */

#include <iostream>
#include <array>

#include "multi_dimensional_root_finding.hpp"
int main( )
{
    const size_t systemSize = 2;

    // Declare equations of system.

    NonlinearSystem<systemSize> sys;
    equation_type eq1 = []( const vector_type& x) {
        return 1.0 - x[0];
    };
    sys.assign_equation( eq1, 0);
    equation_type eq2 = []( const vector_type& x) {
        return 10 * (x[1] - x[0] * x[0] );
    };
    sys.assign_equation( eq2, 1 );

    // Now intialize the system with initial input vector x..
    array<double, systemSize> init = { -10, -5 };
    sys.initialize( init );

    cout << sys.to_string() << endl;
    sys.find_roots_gnewton( );
    cout << sys.to_string() << endl;
    

    // Another system
    eq1 = []( const vector_type& x) {
        return 1.0 - sin(x[0]);
    };
    sys.assign_equation( eq1, 0);
    eq2 = []( const vector_type& x) {
        return 10 * cos(x[1]);
    };
    sys.assign_equation( eq2, 1 );

    // Now intialize the system with initial input vector x..
    init = { -10, -5 };
    sys.initialize( init );

    cout << sys.to_string() << endl;
    sys.find_roots_gnewton( );
    cout << sys.to_string() << endl;

    return 0;
}

