from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='server',
    packages=['server'],
    ext_modules = cythonize("./audio/samplerbox_audio.pyx"),
)