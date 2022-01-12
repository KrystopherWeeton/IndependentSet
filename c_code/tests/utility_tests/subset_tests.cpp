#ifndef __SUBSET_TESTS__
#define __SUBSET_TESTS__

#include <boost/test/unit_test.hpp>
#include "utility/models/subset.hpp"

BOOST_AUTO_TEST_SUITE(subset_test_suite)

BOOST_AUTO_TEST_CASE(creator_destructor_test) {
    Subset subset2(100);            // Test direct constructor
    Subset subset3 = Subset(100);   // Test copy constructor
    // Repeatedly create to test for basic memory leaks
    for (int i = 0; i < 10; i++) {
        subset2 = Subset(100 - i);  // Test copy assignment
        subset3 = subset3;          // Test direct copying
    }
}

BOOST_AUTO_TEST_CASE(is_empty_test) {
    Subset subset = Subset(100);
    BOOST_ASSERT(subset.is_empty());
}

BOOST_AUTO_TEST_CASE(get_size_test_1) {
    Subset subset = Subset(100);
    BOOST_ASSERT(subset.get_size() == 0);
    subset.add(1);
    BOOST_ASSERT(subset.get_size() == 1);
}

BOOST_AUTO_TEST_CASE(get_size_test_2) {
    Subset subset = Subset(100);
    subset.remove(1);
    BOOST_ASSERT(subset.get_size() == 0);
    subset.add(1);
    BOOST_ASSERT(subset.get_size() == 1);
}

BOOST_AUTO_TEST_CASE(get_size_test_3) {
    Subset subset = Subset(100);
    for (int i = 0; i < 100; i++) {
        subset.add(i);
        BOOST_ASSERT(subset.get_size() == i + 1);
    }
    subset.add(1);
    BOOST_ASSERT(subset.get_size() == 100);
}

BOOST_AUTO_TEST_CASE(is_in_subset_test) {
    Subset subset(100);
    BOOST_ASSERT(!subset.is_in_subset(1));
    subset.add(1);
    BOOST_ASSERT(subset.is_in_subset(1));
    BOOST_ASSERT(!subset.is_in_subset(2));
    subset.remove(1);
    BOOST_ASSERT(!subset.is_in_subset(1));
}

BOOST_AUTO_TEST_CASE(empty_test) {
    Subset subset(100);
    for (int i = 0; i < 100; i++) {
        subset.add(i);
    }
    BOOST_ASSERT(subset.get_size() == 100);
    subset.empty();
    BOOST_ASSERT(subset.get_size() == 0);
    BOOST_ASSERT(subset.is_empty());
    BOOST_ASSERT(!subset.is_in_subset(1));
}

BOOST_AUTO_TEST_CASE(set_value_test) {
    Subset subset(100);
    for (int i = 0; i < 100; i++) {
        subset.add(i);
    }
    subset.set_value({1, 3, 5});
    BOOST_ASSERT(subset.is_in_subset(1));
    BOOST_ASSERT(subset.is_in_subset(3));
    BOOST_ASSERT(subset.is_in_subset(5));
    BOOST_ASSERT(!subset.is_in_subset(4));
    BOOST_ASSERT(subset.get_size() == 3);
}

BOOST_AUTO_TEST_SUITE_END()
#endif