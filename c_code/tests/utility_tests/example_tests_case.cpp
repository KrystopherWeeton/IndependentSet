#ifndef __EXAMPLE_TESTS__
#define __EXAMPLE_TESTS__

#define BOOST_TEST_MAIN
#define BOOST_TEST_MODULE Example Test Suite
#include <boost/test/unit_test.hpp>

BOOST_AUTO_TEST_SUITE(example_test_suite)

BOOST_AUTO_TEST_CASE(simple_test) {
  BOOST_CHECK_EQUAL(2+2, 4);
}

BOOST_AUTO_TEST_CASE(simple_test_2) {
    BOOST_CHECK_EQUAL(2-2, 4);
}

BOOST_AUTO_TEST_SUITE_END()

#endif