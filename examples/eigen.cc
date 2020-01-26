#include <iostream>
#include <sstream>
#include <string>
#include <quadmath.h>
namespace std
{
inline __float128 sqrt(__float128 x) { return sqrtq(x); }
inline __float128 log(__float128 x) { return logq(x); }
inline __float128 log10(__float128 x) { return log10q(x); }
inline __float128 ceil(__float128 x) { return ceilq(x); }
inline __float128 isfinite(__float128 x) { return x - x == 0; }
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
#include <pybind11/eigen.h>
#include <Eigen/Dense>
#include <Eigen/Eigenvalues>
namespace Eigen
{
template <>
struct NumTraits<__float128>
{
  enum
  {
    IsInteger = 0,
    IsSigned = 1,
    IsComplex = 0,
    RequireInitialization = 1,
    ReadCost = 1,
    AddCost = 1,
    MulCost = 1
  };

  typedef __float128 Real;
  typedef typename internal::conditional<
      IsInteger,
      typename internal::conditional<sizeof(__float128) <= 2, float, double>::type,
      __float128>::type NonInteger;
  typedef __float128 Nested;
  typedef __float128 Literal;

  EIGEN_DEVICE_FUNC
  static inline Real epsilon()
  {
    return FLT128_EPSILON;
  }

  EIGEN_DEVICE_FUNC
  static inline int digits10()
  {
    return 33;
  }

  EIGEN_DEVICE_FUNC
  static inline Real dummy_precision()
  {
    // make sure to override this for floating-point types
    return 1e-33;
  }

  EIGEN_DEVICE_FUNC
  static inline __float128 highest()
  {
    return FLT128_MAX;
  }

  EIGEN_DEVICE_FUNC
  static inline __float128 lowest()
  {
    return -FLT128_MAX;
  }

  EIGEN_DEVICE_FUNC
  static inline __float128 infinity()
  {
    return 1.0q / 0.0q;
  }

  EIGEN_DEVICE_FUNC
  static inline __float128 quiet_NaN()
  {
    return nanq("nan");
  }
};
} // namespace Eigen

std::string entropy(const Eigen::MatrixXi &rho, int size)
{
  Eigen::SelfAdjointEigenSolver<Eigen::Matrix<__float128, Eigen::Dynamic, Eigen::Dynamic> > es;
  es.compute(rho.cast<__float128>());
  const auto w = es.eigenvalues();
  __float128 e = 0.0q;
  for (size_t i = 0; i < w.size(); i++)
  {
    if (w(i) > 0)
    {
      auto ww = w(i) / __float128(size);
      e -= ww * logq(ww);
    }
  }
  e /= logq(2);

  std::stringstream r("");
  r.precision(33);
  r << std::scientific;
  r << e;
  return r.str();
}

// ----------------
// Python interface
// ----------------
namespace py = pybind11;

PYBIND11_MODULE(eigen, m)
{
  m.doc() = "Eigen quad-precision implementation for entropy";
  m.def("entropy", &entropy);
}
