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
#include <limits>
#include <array>


// Boost ublas library of matrix algebra.
#include <boost/numeric/ublas/matrix.hpp>
#include <boost/numeric/ublas/lu.hpp>
#include <boost/numeric/ublas/vector.hpp>
#include <boost/numeric/ublas/io.hpp>

using namespace std;
using namespace boost::numeric;

typedef double value_type;
typedef ublas::vector<value_type> vector_type;
typedef ublas::matrix<value_type> matrix_type;
typedef function<value_type( const vector_type&  )> equation_type;

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


    NonlinearSystem( ) 
    {
        value.resize( SystemSize, 0);
        jacobian.resize( SystemSize, SystemSize, 0);
        invJacobian.resize( SystemSize, SystemSize, 0);
    }

    /**
     * @brief Assign a std::function as equation of system.
     *
     * @param eq  std::function 
     * @param index Which equation of system.
     */
    void assign_equation( const equation_type& eq, size_t index)
    {
        if( index >= SystemSize )
        {
            cerr << "Fatal: This system is initialized with " << SystemSize 
                << " equations. " << endl;
            cerr << "|| You are trying to assign at index " << index << endl;
            exit(1);
        }

        system[index] = eq;
    }


    vector_type compute_at(const vector_type& x)
    {
        vector_type result(SystemSize);
        result[0] = system[0](x);
        result[1] = system[1](x);
        return result;
    }

    void compute_jacobian( const vector_type& x )
    {

#ifdef  DEBUG
        cout  << "Debug: computing jacobian at " << x << endl;
#endif     /* -----  not DEBUG  ----- */
        for( size_t i = 0; i < SystemSize; i++)
            for( size_t j = 0; j < SystemSize; j++)
            {
                vector_type temp = x;
                temp[j] += step;
                value_type dvalue = (system[i]( temp ) - system[i]( x ))/ step;
                jacobian(i, j) = dvalue;
            }

        // Keep the inverted jacobian ready
        inverse( jacobian, invJacobian );

#ifdef  DEBUG
        cout  << "Debug: " << to_string( ) << endl;
#endif     /* -----  not DEBUG  ----- */
    }

    template<typename T>
    void initialize( const T& x )
    {
        vector_type init;
        init.resize(SystemSize, 0);

        for( size_t i = 0; i < SystemSize; i++)
            init[i] = x[i];

        argument = init;
        value = compute_at( init );
        compute_jacobian( init );
    }

    string to_string( )
    {
        stringstream ss;

        ss << "=======================================================";
        ss << endl << setw(25) << "State of system: " ;
        ss << " Argument: " << argument << " Value : " << value;
        ss << endl << setw(25) << "Jacobian: " << jacobian;
        ss << endl << setw(25) << "Inverse Jacobian: " << invJacobian;
        ss << endl;
        return ss.str();
    }


    /**
     * @brief Find roots using Newton-Raphson method.
     *
     * @param tolerance  Default to 1e-12
     * @param max_iter  Maximum number of iteration allowed , default 100
     *
     * @return  If successful, return true. Check the variable `argument` at
     * which the system value is close to zero (within  the tolerance).
     */
    bool find_roots_gnewton( 
            double tolerance = 1e-12
            , size_t max_iter = 100
            )
    {
        size_t iter = 0;
        while( ublas::norm_2(value) > tolerance and iter <= max_iter)
        {
            compute_jacobian( argument );
            iter += 1;
            value = compute_at( argument );
            ublas::vector<value_type> s = argument - ublas::prod( invJacobian, value );
#ifdef DEUBG
            cerr << "Previous " << argument << " Next : " << s << endl;
#endif
            argument = s;
        }

        if( iter > max_iter )
        {
            cerr << "[WARN] Could not find roots of system." << endl;
            cerr <<  "\tTried " << iter << " times." << endl;
            cerr << "\tIteration limits reached" << endl;
            return false;
        }

        cerr << "Info: Computed roots succesfully in " << iter 
            << " iterations " << endl;
        return true;
    }


    /**
     * @brief Stores the equations of system in an array. Each equation is a
     * lambda expression.
     */
    std::array< equation_type, SystemSize > system;
    vector_type value;
    vector_type argument;
    matrix_type jacobian;
    matrix_type invJacobian;
    double step = sqrt(numeric_limits<double>::epsilon());
    const size_t size = SystemSize;
};
