# to demonstrate ctypes

from ctypes import *
import ctypes
alm_obj = CDLL("./libalm.so")
libm_obj = CDLL("/usr/lib/x86_64-linux-gnu/libm.so.6")
alm_obj.connect()
libm_obj.connect()

alm_exp = alm_obj.amd_exp
libm_exp = libm_obj.exp

alm_exp.argtypes = [ctypes.c_double]
libm_exp.argtypes = [ctypes.c_double]

alm_exp.restype = ctypes.c_double
libm_exp.restype = ctypes.c_double

op = alm_exp(-744.14798321030048)
print (op)
op = libm_exp(-744.14798321030048)
print (op)
