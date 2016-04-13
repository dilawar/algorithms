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

#include <iostream>
#include <sstream>
#include <array>
#include <iomanip>
#include <functional>


using namespace std;

typedef double value_type;

// A sysmte of non-linear equations. Store the values in result.
template< size_t SystemSize>
class NonlinearSystem
{
public:

    typedef std::array<value_type, SystemSize> vector_type;
    typedef std::array<vector_type, SystemSize> matrix_type;

    typedef function<value_type( const vector_type&  )> equation_type;

    NonlinearSystem( ) {}

    NonlinearSystem( const vector_type& x) : state( x )
    {
        auto eq0 = [this]( const vector_type& y ) { 
            return 1.0 * (1.0 - y[0]);
        };
        auto eq1 = [this]( const vector_type& y ) {
            return 10 * ( y[1] - y[0] * y[0]);
        };
        system[0] = eq0;
        system[1] = eq1;
    }


    vector_type compute_at(const vector_type& x)
    {
        iter += 1;
        vector_type result;
        result[0] = system[0](x);
        result[1] = system[1](x);
        return result;
    }

    void apply( const vector_type& x)
    {
        state = compute_at( x );
    }

    void compute_jacobian( )
    {
        double step = 0.001;
        for( size_t i = 0; i < SystemSize; i++)
            for( size_t j = 0; j < SystemSize; j++)
            {
                vector_type temp = state;
                temp[j] += step;
                value_type dvalue = (system[i]( temp ) - system[i]( state ))/ step;
                jacobian[i][j] = dvalue;
            }
    }

    string to_string( )
    {
        stringstream ss;

        ss << "Iter: " << iter << " State: ";
        for ( auto v : state ) ss << v << ",";
        ss << endl << "Jacobian " << endl;
        for( auto v : jacobian )
        {
            for( auto vv : v )
                ss << setw(5) << vv;
            ss << endl;
        }

        return ss.str();
    }

    /**
     * @brief Stores the equations of system in an array. Each equation is a
     * lambda expression.
     */
    std::array< equation_type, SystemSize > system;
    vector_type state;
    matrix_type jacobian = {0};
    size_t iter = 0;
    const size_t size = SystemSize;
};

template< size_t N >
void find_roots( NonlinearSystem<N>& sys 
        , const value_type& a
        , const value_type& b
        , unsigned int eps_tolerance = 30
        , size_t max_iter = 100
        )
{
    cout << sys.to_string( ) << endl;
    sys.apply( sys.state );
    cout << sys.to_string( ) << endl;
    sys.compute_jacobian();
    cout << sys.to_string( ) << endl;

}

int main( )
{
    cerr << "This program computes the root of system described here "
        << "https://Filenamew.gnu.org/software/gsl/manual/html_node/Example-programs-for-Multidimensional-Root-finding.html#Example-programs-for-Multidimensional-Root-finding"
        << endl;

    const size_t systemSize = 2;
    array<value_type, systemSize> init { {2.0, 3.0 } }; 

    NonlinearSystem<systemSize> sys(init);
    find_roots<systemSize>(sys, 1.0, 2.0);

    return 0;
}
