#include <iostream>
#include <sstream>
#include <string>
#include <quadmath.h>
namespace std
{
inline std::ostream &operator<<(std::ostream &out, __float128 f)
{
  char buf[200];
  std::ostringstream format;
  format << "%." << (std::min)(190L, out.precision()) << "Qe";
  quadmath_snprintf(buf, 200, format.str().c_str(), f);
  out << buf;
  return out;
}
} // namespace std

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <mpack/mblas___float128.h>
#include <mpack/mlapack___float128.h>

namespace py = pybind11;

std::string entropy(const py::array_t<int, py::array::c_style> &rho, int size)
{
  py::buffer_info buf1 = rho.request();
  mpackint n = buf1.shape[0];
  __float128 *w = new __float128[n];
  //work space query
  mpackint lwork = -1, info;
  __float128 *work = new __float128[1];
  __float128 *A = new __float128[buf1.size];
  for (int i = 0; i < buf1.size; i++) A[i] = (__float128)((int*)buf1.ptr)[i];
  Rsyev("N", "U", n, A, n, w, work, lwork, &info);
  lwork = (int) work[0];
  delete[] work;
  work = new __float128[std::max((mpackint) 1, lwork)];
  //inverse matrix
  Rsyev("N", "U", n, A, n, w, work, lwork, &info);
  delete[] work;

  __float128 e = 0.0q;
  for (size_t i = 0; i < n; i++)
  {
    if (w[i] > 0)
    {
      auto ww = w[i] / __float128(size);
      e -= ww * logq(ww);
    }
  }
  e /= logq(2);

  delete[] w;
  delete[] A;

  std::stringstream r("");
  r.precision(33);
  r << std::scientific;
  r << e;
  return r.str();
}

// ----------------
// Python interface
// ----------------

PYBIND11_MODULE(eigen, m)
{
  m.doc() = "Eigen quad-precision implementation for entropy";
  m.def("entropy", &entropy);
}
