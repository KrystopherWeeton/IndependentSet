#include <fstream>
#include "lib/cereal/archives/binary.hpp"

using namespace std;

int main() {
    {
        std::ofstream os("out.cereal", std::ios::binary);
        cereal::BinaryOutputArchive archive(os);
        int x = 1;
        archive(x);
    }
    return 0;
}