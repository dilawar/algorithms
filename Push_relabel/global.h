/*
 * =====================================================================================
 *
 *       Filename:  global.h
 *
 *    Description:  This contains all global declarations.
 *
 *        Version:  1.0
 *        Created:  Wednesday 03 October 2012 01:16:13  IST
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Dilawar Singh, dilawar@ee.iitb.ac.in
 *   Organization:  EE, IIT Bombay 
 *
 * =====================================================================================
 */

#ifndef  global_INC
#define  global_INC

#include <string>
#include <iostream>
#include <boost/graph/adjacency_list.hpp>
#include <boost/assert.hpp>



/*-----------------------------------------------------------------------------
 *  Vertex and edge datastructure for flow_graph_t
 *-----------------------------------------------------------------------------*/
struct vertex_info_flow
{
  std::string name;                             /* Name of the node */
  long capacity;                                /* Capacity of node. */
  unsigned height;                              /* Height or distance of node */
};

struct edge_info_flow
{
  std::string name;
  long capacity;                                /* Max capacity of edge */
  long flow;                                    /* Flow on edge */
  long rev;                                     /* Reverse flow. Not used! */
};


typedef boost::adjacency_list<boost::vecS, boost::vecS, boost::bidirectionalS
  , vertex_info_flow, edge_info_flow > flow_graph_t;


#endif   /* ----- #ifndef global_INC  ----- */
