#ifndef __SUBSET__
#define __SUBSET__

#include <string>
#include <set>
#include <stdexcept>
#include <stdio.h>

using namespace std;

/*
* Efficient way to track a subset of {0, 1, 2, ..., N-1} for some maximum value N.
*/
class Subset {
    private:
        int N;
        int* indicator_arr = nullptr;
        int* element_arr = nullptr;
        int size;

        void free() {
            delete[] indicator_arr;
            delete[] element_arr;
            indicator_arr = nullptr;
            element_arr = nullptr;
        }

        void alloc(int N) {
            this->N = N;
            indicator_arr = new int[ N ];
            element_arr = new int [ N ];
        }

    public:


        Subset(int N) {
            alloc(N);
            empty();
        }

        ~Subset() {
            free();
        }

        Subset(const Subset &old_obj) {
            alloc(N);
            for (int i = 0; i < this->N; i++) {
                this->indicator_arr[i] = old_obj.indicator_arr[i];
                this->element_arr[i] = old_obj.element_arr[i];
            }
            this->size = old_obj.size;
        }

        Subset& operator=(const Subset &other) {
            if (this == &other) return *this;
            free();
            alloc(N);
            for (int i = 0; i < this->N; i++) {
                this->indicator_arr[i] = other.indicator_arr[i];
                this->element_arr[i] = other.element_arr[i];
            }
            this->size = other.size;
            return *this;
        }

        /* Testing / query functions */
        int is_empty() { return this->size == 0; }
        int get_size() { return this->size; } 
        bool is_in_subset(int i);

        /* Modification functions */
        void empty();
        void set_value(set<int> subset);
        bool add(int i);
        bool remove(int j);
        bool swap(int to_add, int to_remove);
};


void Subset::empty() {
    /* Zero out entire memory segment for appropriate arrays */
    for (int i = 0; i < N; i++) {
        this->indicator_arr[i] = -1;
        this->element_arr[i] = -1;
    }
    this->size = 0;
}

void Subset::set_value(set<int> subset) {
    this->empty();
    for (int i : subset) {
        this->add(i);
    } 
}


bool Subset::is_in_subset(int i) {
    if (i < 0 || i >= this->N) {
        throw std::out_of_range("Subset query out of bounds");
    }
    return this->indicator_arr[i] >= 0;
}


bool Subset::add(int i) {
    if (this->is_in_subset(i)) {
        return false;
    }
    // There should be space becaise i not in subset
    this->element_arr[this->size] = i;      // Add to list of elements
    this->indicator_arr[i] = this->size;    // Indicate position in list in ind-arr
    this->size++;                           // Update appropriate size
    return true;
}


bool Subset::remove(int j) {
    if (!this->is_in_subset(j)) {
        return false;
    }
    int j_loc = this->indicator_arr[j];
    this->indicator_arr[j] = -1;
    // Remove from list of elements
    if (this->size == 1) {
        // This is the last element, 
        // lazily clear out list by just setting size
        this->size = 0;
    } else {
        // Move element at end of list to j's location in list
        // then update indicator arr for last element and lazily
        // remove j by reducing size.
        int last_element = this->element_arr[this->size - 1];
        this->element_arr[j_loc] = last_element;
        this->indicator_arr[last_element] = j_loc;
        this->size--;
    }
    return true;
}


bool Subset::swap(int to_add, int to_remove) {
    return this->add(to_add) && this->remove(to_remove);
}

#endif