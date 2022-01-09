#include <fstream>
#include "lib/cereal/archives/binary.hpp"
#include <boost/lambda/lambda.hpp>
#include <iostream>
#include <iterator>
#include <algorithm>

using namespace std;

int main() {
    {
        std::ofstream os("out.cereal", std::ios::binary);
        cereal::BinaryOutputArchive archive(os);
        int x = 1;
        archive(x);
    }

    using namespace boost::lambda;
    typedef std::istream_iterator<int> in;

    std::for_each(
        in(std::cin), in(), std::cout << (_1 * 3) << " " );

    return 0;
}