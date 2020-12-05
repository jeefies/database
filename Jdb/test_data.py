import os
import io
import bz2
import time
import codecs
from faker import Faker
from timeit import timeit
from collections import deque

from .data import base


class TestData:
    def setup(self):
        self.data = base(os.getcwd())

    def test_add(self):
        print('test add f')
        self.data.add('line', 'row', 'hello', 'world')
        time.sleep(0.1)
        assert self.data.de, "No data in"
        ad = self.data._index(0)
        assert b'line' in ad or ad[-1] == b'world', "Data error, {}".format(str(ad))


    def test_search(self):
        print('test search f')
        self.data.add('2', 'line2', 'rwo22')
        time.sleep(0.1)
        t = time.time()
        re = self.data.deepsearch('line2', 1)
        ut = time.time() - t
        print('use time', ut, 's')
        assert len(re) == 1, "No data? {}".format(re)
        print(re)
        re = re[0][1]
        assert re, 'search error'
        assert b'2' in re or re[-1] == b'rwo22', "Data error, {}".format(re)

    
    def test_reset(self):
        time.sleep(0.2)
        print('test reset f')
        self.data.reset()
        assert not self.data.de


    def test_many(self):
        print('test many f')
        fk = Faker()
        
        dts = [(fk.color().encode(), fk.name().encode(), fk.country().encode()) for _ in range(100)]

        t = time.time()
        for a in dts: self.data.add(*a)
        adt = time.time() - t
        
        print("add 100 use", adt)
        time.sleep(1)
        t = time.time()
        re = self.data.deepsearch(dts[-1][0], 0)
        srt = time.time() - t
        print('search time', srt)
        assert re, (re, self.data.de)
        re = re[-1][1]
        print("search result:", re, end='\n\n')
        
        assert dts[-1][1] in re or re[-1] == dts[-1][-1], str(tuple(map(self.data._org, self.data[-5:])))
        self.data.reset()
        del self.data


class TestEnDe:
    def setup(self):
        self.base = base(os.getcwd())

    def t(self, x):
        e = self.base._64enb(x)
        assert not b',' in e
        o = self.base._64deb(e)
        assert o == x
        e = self.base._85enb(x)
        assert not b',' in e
        o = self.base._85deb(e)
        assert o == x

    def test_1(self):
        print('test ende f')
        fk = Faker()
        ns = [fk.name().encode() for a in range(200)]
        print('test ende making data f')
        list(map(self.t, ns))
        self.base.quit()
        del self.base

class TestInit:
    def setup_class(self):
        print('test init init')
        self.d = base(os.getcwd(), 'testinit')
        fk = self.fk = Faker()
        ns = [(fk.name(), fk.country()) for a in range(50)]
        adt = time.time()
        self.d.add_all(ns)
        while len(self.d) != 50: pass 
        ut = time.time() - adt
        print('add 50 use time', ut)
        upt = timeit(lambda:self.d.update(), number=1)
        print('update...write..in  use time', upt, '\bs')

    def test_read(self):
        print('test read')
        b = base(os.getcwd(), 'testinit')
        print('reading for TestInit')
        adt = time.time()
        b.init()
        while len(b) != 50: print(len(b)); time.sleep(0.05)
        ut = time.time() - adt
        print('init time use', ut)
        assert b.de == self.d.de, (str(b.de[5]), str(self.d.de[5]))
        b.quit()

    def test_index(self):
        print('test index f')
        print('index..', end='')
        i = deque()
        for d in self.d.de:
            assert not d in i
            i.append(d)
        print('.')

    def test__index(self):
        d = base(os.getcwd(), 'testinit')
        d.init()
        while len(d.de) != 50: pass
        assert d[1]
        assert d[1:]
        assert d[-5:]
        assert d[1:10]
        assert d[1::2]
        d.quit()

    def teardown_class(self):
        print('TestInit class teardown')
        d = base(os.getcwd(), 'testinit')
        d.quit()

class My:
    def __str__(self):
        return ":MY"

def test_to_string():
    print('test to string f')
    ba = base(os.getcwd(), 'testinit')
    ba.init()
    db = ba.to_bytes(ba)
    assert ba.to_bytes(ba) == ba._bytes()
    ba.__del__()

    o = 'string'
    b = ba.to_bytes(o)
    assert o == ba.to_string(o)
    s = ba.to_string(b)
    assert s == o, type(s)
    assert ba.to_bytes(My()) == b":MY"
    assert ba.to_string(My()) == ":MY"
    assert ba.to_string(b":MY", 'hex') == ":MY"

def test_path():
    print('test path')
    try:
        b = base('/hm/p/slo')
    except FileNotFoundError:
        pass

def test_remove():
    print('test rev')
    b = base(os.getcwd(), 'tr')
    fk = Faker()
    dts = [(fk.name().encode(), ) for _ in range(10)]
    b.add_all(dts)
    time.sleep(0.2)
    i, v = b.deepsearch(dts[1][0])[0]
    assert v, (b.de, "No search res")
    assert tuple(v) == dts[1], (i, v)
    b.remove(i)
    assert len(b) == 9
    print(b[:], dts[:], sep='\n')
    b.reset()
    b.quit()
    del b

def test_writein():
    print('test init init')
    d = base(os.getcwd(), 'testinit')
    fk = Faker()
    ns = [(fk.name(), fk.country()) for a in range(50)]
    adt = time.time()
    d.add_all(ns)
    while len(d) != 50: pass 
    ut = time.time() - adt
    print('use time', ut)
    d.update()
    print('update...write..in')
    d.quit()

