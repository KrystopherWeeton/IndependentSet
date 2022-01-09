CCX=gcc 

# Include lib/ folder for library imports in files and use c++11
FLAGS=-I lib -std=c++11


all: main utility

utility: serialization

main: main.cpp
	$(CCX) $(FLAGS) main.cpp -o build/main.out

serialization: utility/serialization.cpp
	$(CCX) $(FLAGS) utility/serialization.cpp -o build/serialization.out

clean:
	rm -r build/*.out