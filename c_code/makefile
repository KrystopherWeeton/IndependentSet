CCX=g++ 

# Include lib/ folder for library imports in files and use c++11
FLAGS=-I lib -std=c++11


main: main.cpp utility
	$(CCX) $(FLAGS) main.cpp -o build/main.o

utility: serialization

serialization: utility/serialization.cpp
	$(CCX) $(FLAGS) -c utility/serialization.cpp -o build/serialization.o

clean:
	rm -r build/*.o

clean_cereal:
	rm -r *.cereal

reset:
	make clean
	make