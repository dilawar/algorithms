/*
 * =====================================================================================
 *
 *       Filename:  push_relabel.cc
 *
 *    Description:  Function to calculate max-flow in a given network flow
 *    graph. It works on a boost-graph.
 *    
 *
 *    See global.h for declaration.
 *
 *        Version:  1.0
 *        Created:  Tuesday 19 March 2013 12:05:42  IST
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Dilawar (Pyro Villainicus), dilawar@ee.iitb.ac.in
 *   Organization:  
 *
 * =====================================================================================
 */


#include <iostream>
#include <iomanip>
#include <sstream>
#include <queue>
#include <boost/graph/graphviz.hpp>
#include <boost/format.hpp>
#include <boost/graph/graphml.hpp>
#include <boost/graph/adjacency_iterator.hpp>
#include "global.h"

using namespace boost;
using namespace std;

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  printDebug
 *  Description:  This function prints debug message if and only if DEBUG macro
 *  is on.
 * =====================================================================================
 */
string printDebug(string msg, string prefix, int level)
{

#ifdef  DEBUG
  stringstream ss;
  ss << format("[%|5|] ") % prefix;
  if(level == 0)
    ss << "| ";
  else 
  {
    for(int i = 0; i < level; i++)
      ss << "+";
  }
  ss << msg;
  return ss.str();
#else      /* -----  not DEBUG  ----- */
 return "";   
#endif     /* -----  not DEBUG  ----- */
}


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  computeMaxFlowPushRelabel
 *  Description:  
 *
 *  Compute max-flow using PUSH_RELABEL method.
 * =====================================================================================
 */
template<typename GraphT>
long computMaxFlowPushRelabel(GraphT& graph, typename GraphT::vertex_descriptor src
    , typename GraphT::vertex_descriptor sink)
{
  long flow = 0;
  stringstream ss;

  /* Initialize the flow. */
  typename GraphT::vertex_iterator ve, ve_end;
  for(tie(ve, ve_end) = vertices(graph); ve != ve_end; ve++)
    graph[*ve].height = 0;

  typename GraphT::edge_iterator ei, ei_end;
  for(tie(ei, ei_end) = edges(graph); ei != ei_end; ei++)
  {
    graph[*ei].flow = 0;
    graph[*ei].rev = 0;
  }

  /* Set the height of source vertices. */
  graph[src].height = num_vertices(graph);

  /* Initialize perflow. */
  typename GraphT::out_edge_iterator oe, oe_end;
  for(tie(oe, oe_end) = out_edges(src, graph); oe != oe_end; oe++)
  {
    auto node = target(*oe, graph);
    ss.str("");
    ss << "Push flow to node " << graph[node].name 
      << " : " << graph[*oe].capacity << " units. " << endl;
    
    cerr << printDebug(ss.str(), "PUSH", 0);

    graph[*oe].flow = graph[*oe].capacity;
    graph[node].capacity += graph[*oe].flow;
    graph[src].capacity -= graph[*oe].flow;
  }

  cerr << printDebug(printFlowNetwork(graph), "PRNT", 0);


  return flow;
}


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  write_graph
 *  Description:  Dump the graph to a graphml file.
 * =====================================================================================
 */
template<typename GraphT>
void write_graph(GraphT& graph, string filePath)
{
  dynamic_properties dp;
  dp.property("name", get(&vertex_info_flow::name, graph));
  dp.property("capacity", get(&vertex_info_flow::capacity, graph));
  dp.property("ecap", get(&edge_info_flow::capacity, graph));
  dp.property("flow", get(&edge_info_flow::flow, graph));

  fstream fl;
  fl.open(filePath, ios::out);
  write_graphml(fl, graph, dp);
  fl.close();
}


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  computeMaxFlowRelabelToFront
 *  Description:  This algorithm is a variation of generic PUSH_RELABEL method.
 *
 *  For details, see Cormen, Leiserson et al. Introduction to algorithm.
 *
 *  NOTE : We may not be implemeting the same algorithm as mentioned in book.
 *  This algorithm has the capability to send back the flow to source node if it
 *  can not discharge it some other nodes. It does it when height of node is
 *  larger than height of source node.
 *-----------------------------------------------------------------------------*/
template<typename GraphT>
long computeMaxFlowRelabelToFront(GraphT& graph
    , typename GraphT::vertex_descriptor source 
    , typename GraphT::vertex_descriptor sink)
{
  cout << "Using relabel to front method. "<< endl;
  time_t t = clock();

  /* Initialize the storehouse */
  vector<typename GraphT::vertex_descriptor> vList; /* List of vertices  */

  typename GraphT::vertex_iterator ve, ve_end;
  for(tie(ve, ve_end) = vertices(graph); ve != ve_end; ve++)
  {
    if(*ve == source || *ve == sink)
    {
    }
    else 
    {
      vList.push_back(*ve);
    }
  }
  /* Initialize the source */
  graph[source].height = num_vertices(graph);
  typename GraphT::out_edge_iterator oe, oe_end;
  for(tie(oe, oe_end) = out_edges(source, graph); oe != oe_end; oe++)
  {
    graph[*oe].flow = graph[*oe].capacity;
    graph[source].capacity -= graph[*oe].flow;
    graph[target(*oe, graph)].capacity = graph[*oe].flow;
  }

  typename GraphT::vertex_descriptor currentNode;
  currentNode = vList.front();

  unsigned loopCout = 0;
  while(currentNode != GraphT::null_vertex() && loopCout < 4*num_vertices(graph)+2)
  {
    currentNode = dischargeNode(currentNode, graph, vList, source);
    loopCout++;
  }

  stringstream ss;
  ss << "Terminating after " << loopCout << " loops " << endl;
  ss << "== Time taken " << (float)(clock() - t)/CLOCKS_PER_SEC << endl;
  cerr << printDebug(ss.str(), "END", 0) << endl;
  cout << ss.str();
  cout << "== Max flow is : " << graph[sink].capacity << endl;
  cout << "== Final flow network. " << endl;
  cout << printFlowNetwork(graph);

  /* Store the graph  */
  write_graph(graph,  "maxflow.gml");

  return graph[sink].capacity;
}


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  dischargeNode
 *  Description:  This is 
 *  It discharges a node and push it back to the front of queue if
 *  height of the node is changed. Else position of node is unchanged in the
 *  queue. 
 *  
 *  Return the next node which should be discharged.
 *-----------------------------------------------------------------------------*/
template<typename GraphT>
typename GraphT::vertex_descriptor dischargeNode(typename GraphT::vertex_descriptor node
    , GraphT& graph 
    , vector<typename GraphT::vertex_descriptor> vList
    , typename GraphT::vertex_descriptor src)
{

  stringstream ss;
  cerr << printDebug( printFlowNetwork(graph), "PRNT", 1);
  ss << "Discharging : " << graph[node].name << " with height " << graph[node].height 
    << " and capacity " << graph[node].capacity << endl;
  cerr << printDebug(ss.str(), "DSCH", 1);

#ifdef TEST
  BOOST_ASSERT_MSG(isKCLSatisfied(node, graph), "KCL is not satisfied");
#endif

  /* If any of the out-neighbour has height higher than this node then we must
   * set the height of this node equal to max(height(out-neighbour)) + 1. 
   */ 
  unsigned oldHeight = graph[node].height;

  typename GraphT::out_edge_iterator oe, oe_end;
  typename GraphT::in_edge_iterator ie, ie_end;

  vector<typename GraphT::vertex_descriptor> outNeighbour;
  vector<typename GraphT::vertex_descriptor> inNeighbour;
  
  for(tie(oe, oe_end) = out_edges(node, graph); oe != oe_end; oe++)
    outNeighbour.push_back(target(*oe, graph));
  
  for(tie(ie, ie_end) = in_edges(node, graph); ie != ie_end; ie++)
    inNeighbour.push_back(source(*ie, graph));

  /* Sort these neighbour list */

  while(!outNeighbour.empty())
  {
    auto n = findMinheightNeighbourAndDeleteIt(outNeighbour, graph);
    ss.str("");
    ss << "Trying neighbour " << graph[n].name << " with height " 
      << graph[n].height << endl;
    cerr << printDebug(ss.str(), "INFO", 2);
    if(graph[node].capacity > 0)
    {
      if(graph[node].height <= graph[n].height)
      {
        ss.str("");
        ss << "Increasing the height of " << graph[node].name 
          << " : neighbour is : " << graph[n].name 
          << " with height " << graph[n].height << endl;
        cerr << printDebug(ss.str(), "HGHT", 2);
        graph[node].height = graph[n].height + 1;
      }

      unsigned availableFlow = graph[node].capacity;
      pair<typename GraphT::edge_descriptor, bool> e = edge(node, n, graph);
      BOOST_ASSERT_MSG(e.second, "== Outedge is not found,");

      unsigned maxPossiblePush = graph[e.first].capacity - graph[e.first].flow;

      if(availableFlow < maxPossiblePush)
        maxPossiblePush = availableFlow;

      graph[node].capacity -= maxPossiblePush;
      graph[e.first].flow += maxPossiblePush;
      graph[n].capacity += maxPossiblePush;

      ss.str("");
      ss << "Pushing flow " << maxPossiblePush << " towards node " 
        << graph[n].name << endl;
      cerr << printDebug(ss.str(), "BACK", 2);
    }
  }

  if(graph[node].capacity > 0)
  {
    ss.str("");
    ss << " Node is overflowing with amount  : " << graph[node].capacity << endl;
    cerr << printDebug(ss.str(), "OVFL", 1);
    
    /* If this node is higher than source node and there is an incoming edge
     * from source node then we should discharge it back to source 
     */
    if(graph[node].height > graph[src].height)
    {
      typename GraphT::in_edge_iterator ie, ie_end;
      typename GraphT::vertex_descriptor inNode = node;
      unsigned nodCap = graph[inNode].capacity;
      graph[inNode].capacity = 0;
      while(inNode != src)
      {
        for(tie(ie, ie_end) = in_edges(inNode, graph); ie != ie_end; ie++)
        {
          inNode = source(*ie, graph);
          ss.str("");
          ss << "Pushing back to " << graph[inNode].name 
            << " flow : " << nodCap << endl;
          cerr << printDebug(ss.str(), "BACK", 2);
          graph[*ie].flow -= nodCap;
          break;
        }
      }
    }

    while(!inNeighbour.empty())
    {
      typename GraphT::vertex_descriptor n = findMinheightNeighbourAndDeleteIt(inNeighbour, graph);

      if(graph[node].capacity > 0)
      {
        ss.str("");
        ss << "Trying to push back to " << graph[n].name << " with height " 
          << graph[n].height;
        cerr << printDebug(ss.str(), "BACK", 2);
        if(graph[node].height < graph[n].height)
          graph[node].height = graph[n].height + 1;

        pair<typename GraphT::edge_descriptor, bool> e = edge(n, node, graph);
        BOOST_ASSERT_MSG(e.second, "IN-EDGE not found.");
        long flowToSendBack = graph[e.first].flow;

        if(graph[node].capacity < flowToSendBack)
          flowToSendBack = graph[node].capacity;
        
        graph[node].capacity -= flowToSendBack;
        graph[n].capacity += flowToSendBack;
        
        graph[e.first].flow -= flowToSendBack;
      }
    }
  }
  BOOST_ASSERT_MSG(graph[node].capacity == 0, "|- Node still overflowing.");

  unsigned newHeight = graph[node].height;
  auto itr = find(vList.begin(), vList.end(), node);
  
  if(newHeight != oldHeight) 
  {
    ss.str("");
    ss << "Relabeling node : " << graph[node].name << endl;
    cerr << printDebug(ss.str(), "RLBL", 0);
    vList.erase(itr);
    vList.insert(vList.begin(), 1, node);
    return vList[1];                            /* second element */
  }
  else 
  {
    /* check if there is a node left with excess flow. */
    auto itr = find(vList.begin(), vList.end(), node);
    if(*itr != vList.back())                     /* Not at the last element */
    {
      itr++;
      ss.str("");
      ss << "Fetching next node : " << graph[*(itr)].name << endl;
      cerr << printDebug(ss.str(), "LOOP", 0);
      return *(itr);
    }
    else 
    {
      ss.str("");
      ss << "Terminating at node " << graph[*itr].name << endl;
      cerr << printDebug(ss.str(), "INFO", 0);
      return GraphT::null_vertex();
    }
  }

}


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  isKCLSatisfied
 *  Description:  Test function 
 *
 *  It makes sure that KCL is satisfied at the given node.
 * =====================================================================================
 */
template<typename GraphT>
bool isKCLSatisfied(typename GraphT::vertex_descriptor node, GraphT& graph)
{
  unsigned inflow = 0;
  unsigned outflow = 0;
  unsigned nodecap = graph[node].capacity;

  typename GraphT::in_edge_iterator ie, ie_end;
  for(tie(ie, ie_end) = in_edges(node, graph); ie != ie_end; ie++)
    inflow += graph[*ie].flow;
  typename GraphT::out_edge_iterator oe, oe_end;
  for(tie(oe, oe_end) = out_edges(node, graph); oe != oe_end; oe++)
    outflow += graph[*oe].flow;
  if(inflow == (outflow + nodecap))
    return true;
  else 
  {
    cerr << " ++ KCL at node " << graph[node].name 
      << "(inflow = outflow + capacity) : " 
      << inflow << " =? " << outflow << "+" << nodecap << endl;
    return false;
  }
}

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  neighbourList
 *  Description:  
 *  Returns the list of neightbours of a node.
 * =====================================================================================
 */
template<typename GraphT>
vector<typename GraphT::vertex_descriptor> neighbourList(
    typename GraphT::vertex_descriptor node 
    , GraphT& graph)
{
  vector<typename GraphT::vertex_descriptor> vList;
  typename GraphT::out_edge_iterator oe, oe_end;
  typename GraphT::in_edge_iterator ie, ie_end;

  for(tie(oe, oe_end) = out_edges(node, graph); oe != oe_end; oe++)
    vList.push_back(target(*oe, graph));

  for(tie(ie, ie_end) = in_edges(node, graph); ie != ie_end; ie++)
    vList.push_back(source(*ie, graph));

  BOOST_ASSERT_MSG(vList.size() > 0, "This node does not have any neighbour.");
  return vList;
}


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  printANode
 *  Description:  Print a single node.
 * =====================================================================================
 */
template<typename GraphT>
string printANode(GraphT& graph, typename GraphT::vertex_descriptor v)
{
  stringstream ss;
  ss << setw(10) << graph[v].name << setw(5) 
    << graph[v].height << setw(5)
    << graph[v].capacity;
  return ss.str();
}


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  printFlowNetwork
 *  Description:  
 * =====================================================================================
 */
template<typename GraphT>
string printFlowNetwork( GraphT& graph )
{
  stringstream ss;
  ss << endl;
  set<typename GraphT::vertex_descriptor> nodes;
  typename GraphT::vertex_iterator ve, vee,  ve_end, vee_end;
  for(tie(ve, ve_end) = vertices(graph); ve != ve_end; ve++)
  {
    ss << printANode<GraphT>(graph, *ve);
    for(tie(vee, vee_end) = vertices(graph); vee != vee_end; vee++)
    {
      auto e = edge(*ve, *vee, graph);
      if(e.second)
        ss << "|" << setw(2) << graph[e.first].flow << "/" << setw(2) 
          << graph[e.first].capacity;
      else 
        ss << "|     ";
    }
  ss << endl;
  }

  return ss.str();
}


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  findMinheightNeighbourAndDeleteIt
 *  Description:  This function mimicks the priority_queue.
 *
 *  Find the smallest element and delete it from the list.
 *-----------------------------------------------------------------------------*/
template<typename GraphT>
typename GraphT::vertex_descriptor findMinheightNeighbourAndDeleteIt(
    vector<typename GraphT::vertex_descriptor>& vList 
    , GraphT& graph)
{
  unsigned oldLenght = vList.size();
  unsigned minHeight = 2<<30;
  auto loc = vList.begin();
  for(auto itr = vList.begin(); itr != vList.end(); itr++)
  {
    if(graph[*itr].height < minHeight)
    {
      minHeight = graph[*itr].height;
      loc = itr;
    }
  }

  typename GraphT::vertex_descriptor outNode = *loc;
  vList.erase(loc);
  BOOST_ASSERT_MSG(oldLenght == vList.size() + 1, "We must have deleted one element.");
  return outNode;
}

#ifndef  STATIC_LIB

int main()
{

  flow_graph_t flowGraph;

  flow_graph_t::vertex_descriptor s = add_vertex(flowGraph);
  flowGraph[s].capacity = 0;
  flowGraph[s].name = "s";
  flowGraph[s].height = 0;

#ifdef EX2                                     
  flow_graph_t::vertex_descriptor w = add_vertex(flowGraph);
  flowGraph[w].height = 0;
  flowGraph[w].capacity = 0;
  flowGraph[w].name = "w"; 
#endif

  flow_graph_t::vertex_descriptor x = add_vertex(flowGraph);
  flowGraph[x].height = 0;
  flowGraph[x].capacity = 0;
  flowGraph[x].name = "x";

  flow_graph_t::vertex_descriptor y = add_vertex(flowGraph);
  flowGraph[y].name = "y";
  flowGraph[y].capacity = 0;
  flowGraph[y].height = 0;

  flow_graph_t::vertex_descriptor z = add_vertex(flowGraph);
  flowGraph[z].name = "z";
  flowGraph[z].capacity = 0;
  flowGraph[z].height = 0;

  flow_graph_t::vertex_descriptor t = add_vertex(flowGraph);
  flowGraph[t].name = "t";
  flowGraph[t].capacity = 0;
  flowGraph[t].height = 0;

  typedef pair<flow_graph_t::edge_descriptor, bool> edge_t;

#ifdef EX2
  edge_t sw = add_edge(s, w, flowGraph);
  flowGraph[sw.first].capacity = 16;

  edge_t sy = add_edge(s, y, flowGraph);
  flowGraph[sy.first].capacity = 13;

  edge_t wx = add_edge(w, x, flowGraph);
  flowGraph[wx.first].capacity = 12;

  edge_t wy = add_edge(w, y, flowGraph);
  flowGraph[wy.first].capacity = 10;

  edge_t yw = add_edge(y, w, flowGraph);
  flowGraph[yw.first].capacity = 4;

  edge_t yz = add_edge(y, z, flowGraph);
  flowGraph[yz.first].capacity = 14;

  edge_t xy = add_edge(x, y, flowGraph);
  flowGraph[xy.first].capacity = 9;

  edge_t xt = add_edge(x, t, flowGraph);
  flowGraph[xt.first].capacity = 20;

  edge_t zx = add_edge(z, x, flowGraph);
  flowGraph[zx.first].capacity = 7;

  edge_t zt = add_edge(z, t, flowGraph);
  flowGraph[zt.first].capacity = 4;

#else    
  edge_t sx = add_edge(s, x, flowGraph);
  flowGraph[sx.first].capacity = 12;

  edge_t sy = add_edge(s, y, flowGraph);
  flowGraph[sy.first].capacity = 14;

  edge_t xy = add_edge(x, y, flowGraph);
  flowGraph[xy.first].capacity = 5;

  edge_t yz = add_edge(y, z, flowGraph);
  flowGraph[yz.first].capacity = 8;

  edge_t zt = add_edge(z, t, flowGraph);
  flowGraph[zt.first].capacity = 10;

  edge_t zx = add_edge(z, x, flowGraph);
  flowGraph[zx.first].capacity = 7;

  edge_t xt = add_edge(x, t, flowGraph);
  flowGraph[xt.first].capacity = 16;

#endif  

  write_graph(flowGraph, "flow.gml");

  //computeMaxFlowRelabelToFront<flow_graph_t>(flowGraph, s, t);

  computMaxFlowPushRelabel<flow_graph_t>(flowGraph, s, t);

  exit(0);
}
#endif     /* -----  not STATIC_LIB  ----- */
