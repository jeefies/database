import os, sys
from distutils.core import setup, Extension
from Cython.Build import cythonize

def main():
    if not '1' in sys.argv:
        f = os.path.abspath(__file__)
        os.system(f'python {f} build_ext 1')
    else:
        sys.argv.pop()
        setup(
            ext_modules = cythonize(
                Extension(
                    'data',
                    sources = ['_data.py']
                    )
                )
            )

if __name__ == "__main__":
    main()
