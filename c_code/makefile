CCX=g++-11

# Include lib/ folder for library imports in files and use c++11
FLAGS=-I lib -I . -std=c++11


main: main.cpp utility
	$(CCX) $(FLAGS) main.cpp -o build/main.o

utility: random

random: utility/random.cpp
	$(CCX) $(FLAGS) -c utility/random.cpp -o build/random.o

clean:
	rm -r build/*.o

clean_cereal:
	rm -r *.cereal

reset:
	make clean
	make