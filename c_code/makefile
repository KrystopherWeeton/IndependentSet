CCX=g++

# Include lib/ folder for library imports in files and use c++11
FLAGS=-I lib -I . -std=c++11
LDFLAGS=-L/usr/local/lib -I /usr/local/include/

main: main.cpp utility
	$(CCX) $(FLAGS) main.cpp -o build/main.o

utility: random

random: utility/random.cpp
	$(CCX) $(FLAGS) -c utility/random.cpp -o build/random.o


tests: tests/utility_tests/*.cpp
	$(CCX) $(FLAGS) $(LDFLAGS) -DBOOST_TEST_DYN_LINK -lboost_unit_test_framework tests/utility_tests/*.cpp -o build/tests.o

clean:
	rm -r build/*.o

clean_cereal:
	rm -r *.cereal

reset:
	make clean
	make