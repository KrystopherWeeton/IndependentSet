

/*[markdown]
* The *abstract* parent class for a problem "solution", which defines the expected format for
* a solution for a specified instance.

*/
class Solution {
    public:
        /* Function to provide score for a specified solution */
        virtual float score() const;

        /* Operators to support equality / inequality using the 'equal_to' functionality*/
        bool operator ==(const Solution& s) const { return equal_to(s); }
        bool operator !=(const Solution& s) const { return !equal_to(s); }

    protected:
        /* Function to validate that a score lies within the expected bounds */
        virtual bool validate_score(float score) const;

        /* Function to determine equality of Solutions */
        virtual bool equal_to(const Solution& s) const;

};