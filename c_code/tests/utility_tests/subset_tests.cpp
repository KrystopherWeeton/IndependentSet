#ifndef __SUBSET_TESTS__
#define __SUBSET_TESTS__

#include <boost/test/unit_test.hpp>

#include "utility/models/subset.hpp"

BOOST_AUTO_TEST_SUITE(subset_test_suite)

BOOST_AUTO_TEST_CASE(creation_test) {

  BOOST_CHECK_EQUAL(2+2, 4);
}

BOOST_AUTO_TEST_CASE(subset_test_2) {
    BOOST_CHECK_EQUAL(2+2, 5);
}

BOOST_AUTO_TEST_SUITE_END()

#endif