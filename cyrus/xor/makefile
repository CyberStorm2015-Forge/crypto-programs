all: xor

xor: xor.o
	g++ -Wall -w -std=c++11 xor.o -o xor

xor.o: xor.cc
	g++ -Wall -w -c xor.cc -std=c++11

clean:
	$(RM) xor.o
