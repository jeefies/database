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
    dts = [(fk.name(), randint(1, 500)) for _ in range(100)]
    b.add_all(dts)
    time.sleep(0.5)
    assert len(b) == 100
    re = b.search(dts[-1][0])[0]
    r = re[1]
    print(re, r)
    assert r['name'] == dts[-1][0] and r['key'] == dts[-1][1], (re, r)
    assert r == b[re[0]]
