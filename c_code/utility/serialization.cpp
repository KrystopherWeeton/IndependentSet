#include <fstream>
#include <../cereal/types/unordered_map.hpp>
#include <../cereal/types/memory.hpp>
#include <../cereal/types/binary.hpp>


int main() {
    std::ofstream os("out.cereal", std::ios::binary);
    cereal::BinaryOutput
}