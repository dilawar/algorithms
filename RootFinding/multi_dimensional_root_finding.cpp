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
#include <functional>
#include <iomanip>

// Boost ublas library of matrix algebra.
#include <boost/numeric/ublas/matrix.hpp>
#include <boost/numeric/ublas/lu.hpp>
#include <boost/numeric/ublas/vector.hpp>
#include <boost/numeric/ublas/io.hpp>

using namespace std;
using namespace boost::numeric;

typedef double value_type;


/* Matrix inversion routine.
   Uses lu_factorize and lu_substitute in uBLAS to invert a matrix */
template<class T>
bool inverse(const ublas::matrix<T>& input, ublas::matrix<T>& inverse) 
{
    using namespace boost::numeric::ublas;
    typedef permutation_matrix<std::size_t> pmatrix;
    // create a working copy of the input
    matrix<T> A(input);
    // create a permutation matrix for the LU-factorization
    pmatrix pm(A.size1());

    // perform LU-factorization
    int res = lu_factorize(A,pm);
    if( res != 0 ) return false;

    // create identity matrix of "inverse"
    inverse.assign(ublas::identity_matrix<T>(A.size1()));

    // backsubstitute to get the inverse
    lu_substitute(A, pm, inverse);

    return true;
}

// A sysmte of non-linear equations. Store the values in result.
template< size_t SystemSize>
class NonlinearSystem
{
public:

    typedef ublas::vector<value_type> vector_type;
    typedef ublas::matrix<value_type> matrix_type;

    typedef function<value_type( const vector_type&  )> equation_type;

    NonlinearSystem( ) 
    {

    }

    NonlinearSystem( const vector_type& x) : state( x )
    {
        state.resize( SystemSize, 0);
        jacobian.resize( SystemSize, SystemSize, 0);
        invJacobian.resize( SystemSize, SystemSize, 0);

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
        vector_type result(SystemSize);
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
        double step = 0.0001;
        for( size_t i = 0; i < SystemSize; i++)
            for( size_t j = 0; j < SystemSize; j++)
            {
                vector_type temp = state;
                temp[j] += step;
                value_type dvalue = (system[i]( temp ) - system[i]( state ))/ step;
                jacobian(i, j) = dvalue;
            }

        // Keep the inverted jacobian ready
        inverse( jacobian, invJacobian );
    }

    string to_string( )
    {
        stringstream ss;

        ss << "=======================================================";
        ss << endl << setw(25) << "State of system: " << ( state );
        ss << endl << setw(25) << "Value of system: " << compute_at( state );
        ss << endl << setw(25) << "Jacobian: " << jacobian;
        ss << endl << setw(25) << "Inverse Jacobian: " << invJacobian;
        ss << endl;
        return ss.str();
    }

    /**
     * @brief Stores the equations of system in an array. Each equation is a
     * lambda expression.
     */
    std::array< equation_type, SystemSize > system;
    vector_type state;
    matrix_type jacobian;
    matrix_type invJacobian;
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
    double tolerance = 1e-20;
    sys.compute_jacobian();
    double norm2OfDiff = 1.0;
    size_t iter = 0;
    while( norm2OfDiff > tolerance && iter <= max_iter)
    {
        iter += 1;
        ublas::vector<value_type> s = sys.state -
            ublas::prod( sys.invJacobian, sys.compute_at( sys.state) );
        norm2OfDiff = ublas::norm_2(s - sys.state);
        sys.state = s;
    }

    cerr << "[INFO] Finished computing zeros in " << iter << " steps " << endl;
    cerr << "[INFO] System at this state " << endl;
    cerr << sys.to_string();
}

int main( )
{
    cerr << "This program computes the root of system described here "
        << "https://Filenamew.gnu.org/software/gsl/manual/html_node/Example-programs-for-Multidimensional-Root-finding.html#Example-programs-for-Multidimensional-Root-finding"
        << endl;

    const size_t systemSize = 2;
    ublas::vector<double> init( systemSize );
    init[0] = 2.0;
    init[1] = 10.0;

    NonlinearSystem<systemSize> sys(init);
    find_roots<systemSize>(sys, 1.0, 2.0);

    return 0;
}
