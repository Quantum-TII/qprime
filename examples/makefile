all: eigen.so

eigen.so: eigen.cc
	g++ -O3 -shared -fopenmp -fPIC `python3 -m pybind11 --includes` `pkg-config eigen3 --cflags` $^ -o $@ -lquadmath

clean:
	rm eigen.so