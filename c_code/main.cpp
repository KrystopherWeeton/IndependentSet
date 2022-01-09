#include <fstream>
#include "lib/cereal/archives/binary.hpp"

using namespace std;

int main() {
    std::ofstream os("out.cereal", std::ios::binary);
    cereal::BinaryOutputArchive archive = cereal::BinaryOutputArchive(os);
    std::string s1 = "Hello World!";
    archive(s1);
    return 0;
}