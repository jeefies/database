import os
import time
from random import randint

from faker import Faker

from .model import Model


class My(Model):
    __cols__ = ('name', ('key', int))

def testmy():
    b = My(os.getcwd(), 'model')
    fk = Faker()
    n = 99
    dts = [(fk.name(), randint(1, 500)) for _ in range(n)]
    b.add_all(dts)
    while len(b) < n: pass
    print(len(b))
    print(*[b._deb(i) for i in b.de[-1][1]])
    print(*[b._deb(i) for i in b.de[-3][1]])
    print(*[b._deb(i) for i in b.de[-2][1]])
    re = b.search(dts[-1][0])
    re = re[-1]
    r = re[1]
    print(re, r)
    assert r['name'] == dts[-1][0] and r['key'] == dts[-1][1], (re, r)
    assert r == b[re[0]]
    b.reset()
