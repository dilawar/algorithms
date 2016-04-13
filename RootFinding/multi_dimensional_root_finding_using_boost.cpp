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
#include <vector>

using namespace std;

// A sysmte of non-linear equations. Store the values in result.
template< typename ValueType, size_t SystemSize>
class NonlinearSystem
{
public:

    typedef std::array<ValueType, SystemSize> state_type;

    NonlinearSystem( const state_type& x) : init( x )
    {
        cout << "Debug: Size is " << size << endl;
        cout << "Debug: Init ";
        for( auto v : init ) cout << v << ",";
        cout << endl;

        equations[0] = [this]( const ValueType& v ) { return 1.0 * (1.0 - v); };
        equations[1] = [this]( const ValueType& v ) { return 10.0 - state[1]; };

        // compute the state at this point.
        this->operator()( x );

        cout << "Info: Created a system with " << SystemSize << " equations " << endl;
    }

    // Compute the value of system at input x; return an array with output
    state_type operator()(const state_type& x)
    {
        for( size_t i = 0; i < SystemSize; i++ )
            state[i] = equations[i](x[i]);
        return state;
    }

    ValueType observe( const ValueType at, const size_t whichEquation )
    {
        return equations[whichEquation]( at );
    }


    /**
     * @brief Stores the equations of system in an array. Each equation is a
     * lambda expression.
     */
    array< function<ValueType(const ValueType&)>, SystemSize > equations;

    state_type init;
    state_type input;
    state_type state;
    const size_t size = SystemSize;
};

template< typename ValueType, size_t N >
void find_roots( NonlinearSystem<ValueType, N>& sys 
        , const ValueType& a
        , const ValueType& b
        , unsigned int eps_tolerance = 30
        , boost::uintmax_t max_iter = 100
        )
{
    boost::math::tools::eps_tolerance< double > tol(eps_tolerance);

    // Now compute the root of each equation.
    for( size_t i = 0; i < N; i++)
    {
        cout << "Info: Solving equation " << i << endl;
        auto t = sys.equations[ i ];
        auto r1 = boost::math::tools::toms748_solve(t, 0.0, 20.0, tol, max_iter);
        std::cout << "\troot bracketed: [ " << r1.first << " , " << r1.second <<  " ]" << std::endl;
        std::cout << "\tf("<< r1.first << ")=" << sys.observe(r1.first, 1) << std::endl;
        std::cout << "\tf("<< r1.second << ")=" << sys.observe(r1.second, 1) << std::endl;
        std::cout << "\tmax_iter=" << max_iter << std::endl;
    }
}

int main( )
{
    cerr << "This program computes the root of system described here "
        << "https://Filenamew.gnu.org/software/gsl/manual/html_node/Example-programs-for-Multidimensional-Root-finding.html#Example-programs-for-Multidimensional-Root-finding"
        << endl;

    const size_t systemSize = 2;
    array<double, systemSize> init { {2.0, 3.0 } }; 

    NonlinearSystem<double, systemSize> sys(init);
    find_roots<double, systemSize>(sys, 1.0, 2.0);
    return 0;
}
