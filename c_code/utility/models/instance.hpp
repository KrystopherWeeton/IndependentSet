#ifndef _INSTANCE_
#define _INSTANCE_

#include "solution.hpp"

#include <set>


/*[markdown]
* The *abstract* parent class for a problem "instance", which defines generation, and search space
* structure for a problem.

* NOTE: If a separate search space structure is requested for a particular problem, you can subclass
* the appropriate Instance subclass and override the 'neighbors' function, as well as the 'solution'
* generic.

* *S*: The solution class for this specific instance
*/
template <class S>
class Instance {
    public:

        Instance() {
            /* Static assertion to verify S is valid solution subclass */
            static_assert(std::is_base_of<Solution, S>::value, "template S is not subclass of Solution");
        }

        virtual void generate_instance();
        virtual bool seed();
        virtual std::set<S> neighbors(S s);
        virtual std::iterator<std::output_iterator_tag, S> neighbors_iterator(S s);

};

#endif