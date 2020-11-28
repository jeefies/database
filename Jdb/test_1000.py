import time, os
from timeit import timeit
from threading import Thread

from faker import Faker

from .data import base

def test():
    b = base(os.getcwd(), Inet=1)
    b.reset()

    fk = Faker()
    dts = [(fk.name().encode(), fk.color().encode()) for _ in range(1000)]

    b.add_all(dts)

    def w():
        while len(b) != 1000:
            pass

    aut = timeit(w, number=1)
    print('add 1000 with no error use', aut, 's')

    def d():
        global a
        a = b.deepsearch(dts[-1][0], 0)

    ut = timeit(d, number=1)
    print('search use', ut, 's')
    print('result', a)
    assert a
    print('getting str')
    s = str(b)
    print('ok')
    b.init()
    print('create new file')

