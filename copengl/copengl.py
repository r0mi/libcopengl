import sys

_64bit = sys.maxsize == 0x7fffffffffffffff

if 0x3080300 <= sys.hexversion:
    if   sys.platform == "linux" and _64bit:
        from .linux.py3_64.copengl import *
    elif sys.platform == "linux" and not _64bit:
        from .linux.py3_32.copengl import *
    elif sys.platform == "darwin":
        from .macosx.py3.copengl import *
    elif sys.platform == "win32":
        from .windows.py3.copengl import *
    else:
        raise RuntimeError(f"Unsupported platform '{sys.platform}'")
else:
    print(f"Error importing 'copengl' module: Python version 3.8.3+ required, you have {sys.version}")
    raise ImportError
