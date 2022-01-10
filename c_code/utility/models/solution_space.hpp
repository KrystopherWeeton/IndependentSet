#ifndef _SOLUTION_SPACE_
#define _SOLUTION_SPACE_

#include "solution.hpp"
#include "instance.hpp"

#include <set>


/*[markdown]
* Class for a dynamic solution space graph that generates vertices as they are queried. Maintains
* a 'cache' which can be set to unlimited size for (attempted) complete mapping. Uses the following
* caching techniques.
* 
* *Vertices*: Cache of vertices which exist within the solution space.
* *Edges*: Cache of both positive and negative edge queries within the solution space.
* *Neighborhood*: Cache of **Complete** neighborhoods of vertices within the solution space.
*   - Probably want to keep this to minimal, as average degree in most solution spaces is extremely large
*   
*  *S*: The solution class for the specified instance
*/
template <class S>
class SolutionSpace {
    private:

        Instance<S> instance;
        int vertex_cache_size;
        int edge_cache_size;
        int neighborhood_cache_size;

    public:

        SolutionSpace(
            Instance<S> instance, 
            int vertex_cache_size, 
            int edge_cache_size, 
            int neighborhood_cache_size)
         {
            this->instance = instance;
            this->vertex_cache_size = vertex_cache_size;
            this->edge_cache_size = edge_cache_size;
            this->neighborhood_cache_size = neighborhood_cache_size;


            // Instantiate the appropriate caches for this solution space
        }

        bool edge_exists(S v1, S v2) {
            return false;
        }

        std::set<S> neighbors(S v) {

        }

        std::set<S> neighbors_sample(S v, int num_samples) {

        }

};


#endif