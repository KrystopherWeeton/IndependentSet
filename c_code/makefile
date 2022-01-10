CCX=g++ 

# Include lib/ folder for library imports in files and use c++11
FLAGS=-I lib -std=c++11


main: main.cpp
	$(CCX) $(FLAGS) main.cpp -o build/main.o

clean:
	rm -r build/*.o

clean_cereal:
	rm -r *.cereal

reset:
	make clean
	make