from distutils.core import setup
from Cython.Build import cythonize
import numpy
import numba

setup(
    ext_modules=cythonize("compute_theta.pyx"),
    include_dirs=[numpy.get_include()]
)