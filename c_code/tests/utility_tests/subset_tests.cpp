#include <boost/test/unit_test.hpp>

BOOST_AUTO_TEST_SUITE(subset_test_suite)

BOOST_AUTO_TEST_CASE(subset_test_1) {
  BOOST_CHECK_EQUAL(2+2, 4);
}

BOOST_AUTO_TEST_CASE(subset_test_2) {
    BOOST_CHECK_EQUAL(2+2, 5);
}

BOOST_AUTO_TEST_SUITE_END()