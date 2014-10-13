from setuptools import setup, find_packages
import sys

extra_packages = []

#if sys.platform == "darwin":
    #extra_packages = ["copengl/macosx/py27/copengl.so"] # no dice. the last dot gets converted to /
# elif sys.platform == "win32" :
# elif sys.platform == "linux2":
# else:
#     raise RuntimeError("platform %s not supported" % (sys.platform))

#print find_packages() # damn this doesn't find ANY of my prebuilt extensions..

setup(
    name         = "copengl",
    version      = "1.0.0",
    license      = "MIT",
    description  = "fast and limited legacy opengl wrapper for python",
    #long_description  = """ """,
    keywords     = "opengl python wrapper",
    #packages     = ["copengl"],
    packages     = extra_packages + find_packages(),
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
    scripts=["copengl/__init__.py"],
    )
