
#from mrasyncmc import __version__
from setuptools import setup, Extension, find_packages

m1 = Extension(
    'mrasyncmc.internals',
     sources = [
      './src/mrasyncmc/internals/city.c',
      './src/mrasyncmc/internals/module.c',
      './src/mrasyncmc/internals/memcachedclient.c',
      #'./src/mrhttp/internals/hash/city.c',
      #'./src/mrhttp/internals/hash/assoc.c',
      #'./src/mrhttp/internals/utils.c',
     ],
     include_dirs = ['./src/mrhttp/internals'],
     extra_compile_args = ['-msse4.2', '-mavx2', '-mbmi2', '-Wunused-variable','-std=c99','-Wno-discarded-qualifiers', '-Wno-unused-variable','-Wno-unused-function'],
     extra_link_args = [],
     #extra_link_args = ['-lasan'],
     define_macros = [('DEBUG_PRINT',1)]
)

setup(
    name='mrasyncmc',
    version="1.0.0",
    description='Python asyncio memcached client',
    long_description='Asyncio based Python client for memcached',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
        ],
    url='https://github.com/MarkReedZ/mrasyncmc',
    author='Mark Reed',
    author_email='mark@untilfluent.com',
    license='MIT License',
    ext_modules = [m1],
    package_dir={'':'src'},
    packages=find_packages('src'),# + ['prof'],
    #packages=['mrasyncmc'],
    zip_safe=True,
)
