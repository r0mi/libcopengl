from setuptools import setup, find_packages
import sys

extra_packages = []

if sys.platform == "darwin":
    extra_package_data = {"copengl": ["macosx/py27/copengl.so"]}
elif sys.platform == "linux2":
    extra_package_data = {"copengl": ["linux/py27_64/copengl.so", "linux/py27_32/copengl.so"]}
elif sys.platform == "win32" :
    extra_package_data = {"copengl": ["windows/copengl.dll"]}
else:
    raise RuntimeError("platform %s not supported" % (sys.platform))


import distutils.util
print(distutils.util.get_platform())

setup(
    name         = "copengl",
    version      = "1.0.0",
    license      = "MIT",
    description  = "fast and limited legacy opengl wrapper for python",
    #long_description  = """ """,
    keywords     = "opengl python wrapper",
    #packages     = ["copengl"],
    packages     = find_packages(),
    package_data = extra_package_data,
    author       = "Elmo Trolla",
    author_email = "fdfdkz@gmail.com",
    url          = "https://github.com/fdkz/libcopengl",
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers  = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Graphics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",],
)
