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
    n = 50
    dts = {i:(fk.name(), randint(1, 500)) for i in range(n)}
    b.add_all(dts)
    while len(b) < n: pass
    print(len(b))
    print(b._org(b.de[0]))
    print(b._org(b.de[2]))
    print(b._org(b.de[1]))
    print('searching...', end='', flush=True)
    re = b.search(dts[n - 1][0])
    print('finish', re)
    re = re[-1]
    print(re)
    r = re[1]
    assert r['name'] == dts[n - 1][0] and r['key'] == dts[n - 1][1], (re, r)
    assert r == b[re[0]]
    b.reset()

def testindex():
    b = My(os.getcwd(), 'model')
    fk = Faker()
    n = 50
    dts = {fk.name(): (fk.country(), randint(1, 500)) for _ in range(n)}
    b.add_all(dts)
