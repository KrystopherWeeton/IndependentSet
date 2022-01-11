#ifndef _SOLUTION_SPACE_
#define _SOLUTION_SPACE_

#include "solution.hpp"
#include "instance.hpp"
#include "simple_cache.hpp"
#include "utility/random.cpp"

#include <utility>
#include <tuple>
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
* *NOTE*: Set these capacities to <= 0 to disable them entirely
*   
*  *S*: The solution class for the specified instance
*/

using namespace std;
template <class S>
class SolutionSpace {
    private:

        Instance<S> instance;
        int edge_cache_capacity;
        int neighborhood_cache_capacity;

        SimpleCache< pair<S, S>, bool >* edge_cache;
        SimpleCache< S, set<S> >* neighborhood_cache;

    public:

        SolutionSpace(
            Instance<S> instance, 
            int edge_cache_capacity, 
            int neighborhood_cache_capacity)
         {
            this->instance = instance;
            this->edge_cache_capacity = edge_cache_capacity;
            this->neighborhood_cache_capacity = neighborhood_cache_capacity;


            // Instantiate the appropriate caches for this solution space
            if (this->edge_cache_capacity > 0) {
                this->edge_cache = new SimpleCache< pair<S, S>, bool>(edge_cache_capacity);
            }
            if (this->neighborhood_cache_capacity > 0) {
                this->neighborhood_cache = new SimpleCache< S, set<S> >(neighborhood_cache_capacity);
            }
        }

        bool edge_exists(S v1, S v2) {
            if (!this->edge_cache) { return this->instance.edge(v1, v2); }
            try {
                return this->edge_cache.query(pair<S, S>(v1, v2));
            } catch (CacheMissException& e) {
                bool response = this->instance.edge(v1, v2);
                this->edge_cache.add(pair<S, S>(v1, v2), response);
                return response;
            }
        }

        set<S> neighbors(S v) {
            if (!this->neighborhood_cache) { return v.neighbors(); }
            try {
                return this->neighborhood_cache.query(v);
            } catch (CacheMissException& e) {
                neighbors = v.neighbors();
                this->neighborhood_cache.add(v, neighbors);
                return neighbors;
            }
        }

        set<S> sample_neighbors(S v, float probability_included) {
            set<S> response = set<S>();
            for (auto it = v.neighbors_begin(); it != v.neighbors_end(); ++it) {
                if (random_func::flip_coin(probability_included)) {
                    Solution neighbor = **it;
                    response.insert(neighbor);
                }
            }
            return response;
        }

        ~SolutionSpace() {
            if (this->edge_cache) {
                delete this->edge_cache;
            }
            if (this->neighborhood_cache) {
                delete this->neighborhood_cache;
            }
        }
};


#endif