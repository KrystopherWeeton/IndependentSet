#ifndef __PC_SOLUTION__
#define __PC_SOLUTION__

#include "utility/models/solution.hpp"
#include <set>

using namespace std;

class PCSolution : public Solution {
    private:
        

    public:

        PCSolution() {

        }

        /* Function to provide score for a specified solution */
        float score() const {

        }

        /* Operators to support equality / inequality using the 'equal_to' functionality*/
        bool operator ==(const Solution& s) const { return equal_to(s); }
        bool operator !=(const Solution& s) const { return !equal_to(s); }

    protected:
        /* Function to validate that a score lies within the expected bounds */
        bool validate_score(float score) const {

        }

        /* Function to determine equality of Solutions */
        bool equal_to(const Solution& s) const {

        }

        set<Solution> neighbors() {

        }

        iterator<output_iterator_tag, Solution> neighbors_begin() {

        }

        iterator<output_iterator_tag, Solution> neighbors_end() {

        }
};


#endif