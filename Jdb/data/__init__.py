import os
import shutil

base = os.path.dirname(os.path.abspath(__file__))
_li = os.listdir(f'{base}/build')
for f in _li:
    if f.startswith('lib'):
        path = os.path.join(base, 'build', f)
        break
_li = os.listdir(path)
shutil.copy(os.path.join(path, _li[0]), base)


try:
    from .data import Base
except Exception as e:
    print("Haven't setup for data, use \nfrom Jdb.data.setup_data import main\nmain()\nto setup\n(depends on cython)")
    from ._data import Base
