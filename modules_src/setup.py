
#
# python setup.py build
#
#
# macosx:
#
#   to prevent errors like this: (for versions before yosemite)
#
#     /usr/libexec/gcc/powerpc-apple-darwin10/4.0.1/as: assembler (/usr/bin/../libexec/gcc/darwin/ppc/as or /usr/bin/../local/libexec/gcc/darwin/ppc/as) for architecture ppc not installed
#     Installed assemblers are:
#     /usr/bin/../libexec/gcc/darwin/x86_64/as for architecture x86_64
#     /usr/bin/../libexec/gcc/darwin/i386/as for architecture i386
#
#   disable ppc support:
#
#     export ARCHFLAGS="-arch i386 -arch x86_64"; python setup.py build
#
# random note: python setup.py build > log.txt 2>&1
#              python setup.py build -c mingw32
#

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

from subprocess import getstatusoutput
import sys


# disable creation of file "xxx-py2.6.egg-info"
#from distutils.command.install import install
#install.sub_commands = [('install_lib', install.has_lib)]

libraries = []
extra_compile_args = []
extra_link_args = []

if sys.platform == "darwin":
    # negate the -g debugging flag that got always added in macosx by default
    extra_compile_args = ["-g0"]
    extra_link_args = ['-framework', 'OpenGL']
elif sys.platform == "win32" :
    libraries = ["OpenGL32"]
elif sys.platform == "linux":
    extra_link_args = [getstatusoutput("pkg-config --cflags --libs gl")[1].strip()]
else:
    raise RuntimeError(f"platform {sys.platform} not supported")


ext_copengl = Extension(
    "copengl",
    language="c",
    sources=["copengl.pyx"],
    include_dirs=["src"],
    library_dirs=[],
    libraries=libraries,
    #define_macros=[],
    extra_link_args=extra_link_args,
    extra_compile_args=extra_compile_args,
    #depends=[],
    )

setup(
    name         = "copengl",
    version      = "0.2.0",
    license      = "MIT",
    description  = "fast and limited opengl wrapper for python",
    #long_description  = """ """,
    keywords     = "",
    author       = "",
    author_email = "",
    url          = "",
    classifiers  = [],
    ext_modules  = [ext_copengl],
    cmdclass     = {'build_ext': build_ext}
    )


# the setup.py "clean" command is not working completely for cython. we'll do it ourselves.

if "clean" in sys.argv:
    import os
    import shutil
    for p in ["copengl.c", "c_copengl.pxd", "copengl.pyx"]:
        print("deleting", p)
        try:    os.remove(p)
        except: pass
    shutil.rmtree("build", True)
