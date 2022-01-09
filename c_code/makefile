CCX=gcc 
FLAGS=-I lib/

all: main utility

utility: serialization

main: main.cpp
	$(CCX) $(FLAGS) main.cpp -o build/main.out

serialization: utility/serialization.cpp
	$(CCX) $(FLAGS) utility/serialization.cpp -o build/serialization.out

clean:
	rm -r build/*.out