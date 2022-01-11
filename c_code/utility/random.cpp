#include <iostream>
#include <stdlib.h>


namespace random_func {

    /*
    * Generates a random float from 0 to 1
    */
    float random_float() {
        return static_cast<float>(rand()) / static_cast<float>(RAND_MAX);
    }

    /*
    * Generates a random coin flip with 'heads' (or success) probability provided.
    */
    bool flip_coin(float success_probability) {
        if (success_probability < 0 || success_probability > 1) {
            throw std::runtime_error("Invalid success probability provided");
        }
        return random_float() >= success_probability;
    }
}