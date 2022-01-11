#ifndef PC_INSTANCE
#define PC_INSTANCE

#include "utility/models/instance.hpp"
#include "pc_solution.hpp"

class PCInstance: public Instance<PCSolution>{
    public:

        PCInstance() {
        }

        static PCInstance generate_instance() {

        }


        bool edge(PCSolution source, PCSolution dest) {
            return false;
        }
};


#endif