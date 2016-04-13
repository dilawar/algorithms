/*
 * =====================================================================================
 *
 *       Filename:  multi_dimensional_root_finding_using_boost.cpp
 *
 *    Description:  Compute root of a multi-dimensional system using boost
 *    libraries.
 *
 *        Version:  1.0
 *        Created:  04/13/2016 11:31:37 AM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Dilawar Singh (), dilawars@ncbs.res.in
 *   Organization:  NCBS Bangalore
 *
 * =====================================================================================
 */

#include <boost/math/tools/roots.hpp>
#include <iostream>
#include <array>


using namespace std;
namespace  bmt = boost::math::tools;

// A sysmte of non-linear equations. Store the values in result.
template< typename ValueType, size_t SystemSize>
class NonlinearSystem
{
public:

    NonlinearSystem( const ValueType& x) 
    {
        init = x;
    }

    ValueType operator()(ValueType const& x)
    {
        result[0] = sin( x ) + 1.0;
        result[1] = cos( x );
        return result;
    }

    ValueType init;
    size_t size = SystemSize;
    array<ValueType, SystemSize> result;
};

template< typename ValueType, size_t N >
void find_roots( const NonlinearSystem<ValueType, N>& sys 
        , const ValueType& a
        , const ValueType& b
        , unsigned int eps_tolerance = 20
        , const unsigned int max_iters = 50
        )
{
    boost::math::tools::eps_tolerance< double > tol(eps_tolerance);

    cerr << "We are here" << endl;
}

int main( )
{
    cerr << "This program computes the root of system described here "
        << "https://Filenamew.gnu.org/software/gsl/manual/html_node/Example-programs-for-Multidimensional-Root-finding.html#Example-programs-for-Multidimensional-Root-finding"
        << endl;

    double init = 2.0;
    const size_t systemSize = 2;
    NonlinearSystem<double, systemSize> sys(init);
    find_roots<double, systemSize>(sys, 1.0, 2.0);
    cerr << "All done" << endl;
    return 0;
}
