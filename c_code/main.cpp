#include <fstream>
#include "lib/cereal/archives/binary.hpp"
#include <boost/lambda/lambda.hpp>
#include <iostream>
#include <iterator>
#include <algorithm>

#include "utility/models/solution.hpp"
#include "utility/models/instance.hpp"
#include "utility/models/solution_space.hpp"

using namespace std;

int main() {
    {
        std::ofstream os("out.cereal", std::ios::binary);
        cereal::BinaryOutputArchive archive(os);
        int x = 1;
        archive(x);
    }
}