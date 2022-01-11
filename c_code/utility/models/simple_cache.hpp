#ifndef _SIMPLE_CACHE_
#define _SIMPLE_CACHE_

#include <queue>
#include <unordered_map>
#include <stdexcept>

using namespace std;


class CacheMissException : public std::exception {
};


/*[markdown]
* A simple FIFO cache which allows for membership queries.
* **max_size**: The maximum number of elements which should be stored.
*/
template< typename K, typename V>
class SimpleCache {
    private:
        int max_size;

        queue<K> fifo_queue;
        unordered_map<K, V> map;

    public:

        SimpleCache(int max_size) {
            this->max_size = max_size;
            this->fifo_queue();
            this->map();

            /* Edge case validation */
            if (this->map.max_size() < this->max_size) {
                throw runtime_error("Max size for simple cache can not be larger than max storable size.");
            }
        }

        /*
        * Adds the requested element to the cache, removing an element and returning it if necessary. If no
        * element is removed, a nullptr is returned instead.
        */
        bool add(K key, V value) {
            this->fifo_queue.push(key);
            this->map[key] = value;
            K front_key = nullptr;
            if (this->max_size > 0 && this->membership_set.size() > this->max_size) {
                front_key = this->fifo_queue.front();
                this->fifo_queue.pop();
                this->map.erase(front_key);
            }
            return front_key;
        }

        /* Returns cached value for K, and nullptr otherwise */
        V query(K key) {
            auto itr = this->map.find(key);
            if (itr == this->map.end()) {
                throw CacheMissException();
            }
            return **itr;
        }

        void clear() {
            // This could be a really bad way to implement this. No cleanup whatsoever
            this->fifo_queue();
            this->map.clear();
        }

        int capacity() {
            return this->max_size;
        }

};

#endif