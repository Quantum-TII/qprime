all: eigen.so

eigen.so: eigen.cc
	g++ -O3 -shared -fopenmp -fPIC `pkg-config mpack --cflags` `python3 -m pybind11 --includes` `pkg-config eigen3 --cflags` $^ -o $@ -lquadmath `pkg-config mpack --libs`

clean:
	rm eigen.so