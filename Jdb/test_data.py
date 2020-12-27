import os
import io
import bz2
import time
import codecs
from faker import Faker
from timeit import timeit
from collections import deque

from .data import Base


class TestData:

    def test_add(self):
        data = Base(os.getcwd(), '1')
        print('test add f')
        data.add('line', 'row', 'hello', 'world')
        time.sleep(0.1)
        assert data.de, "No data in"
        ad = data._index(0)
        assert b'line' in ad or ad[-1] == b'world', "Data error, {}".format(str(ad))
        data.reset()


    def test_search(self):
        data = Base(os.getcwd(), '2')
        print('test search f')
        data.add('2', 'line2', 'rwo22')
        time.sleep(0.1)
        t = time.time()
        re = data.deepsearch('line2', 1)
        ut = time.time() - t
        print('use time', ut, 's')
        assert len(re) == 1, "No data? {}".format(re)
        print(re)
        re = re[0][1]
        assert re, 'search error'
        assert b'2' in re or re[-1] == b'rwo22', "Data error, {}".format(re)

    
    def test_reset(self):
        data = Base(os.getcwd(), '3')
        print('test reset f')
        data.reset()
        assert not data.de


    def test_many(self):
        data = Base(os.getcwd(), '4')
        print('test many f')
        fk = Faker()
        
        dts = [(fk.color().encode(), fk.name().encode(), fk.country().encode()) for _ in range(100)]

        t = time.time()
        for a in dts: data.add(*a)
        adt = time.time() - t
        
        print("add 100 use", adt)
        time.sleep(1)
        t = time.time()
        re = data.deepsearch(dts[-1][0], 0)
        srt = time.time() - t
        print('search time', srt)
        assert re, (re, data.de)
        re = re[-1][1]
        print("search result:", re, end='\n\n')
        
        assert dts[-1][1] in re or re[-1] == dts[-1][-1], str(tuple(map(data._org, data[-5:])))
        data.reset()
        del data


class TestEnDe:

    def t(self, x):
        sBase = Base
        e = sBase._64enb(x)
        assert not b',' in e
        o = sBase._64deb(e)
        assert o == x
        e = sBase._85enb(x)
        assert not b',' in e
        o = sBase._85deb(e)
        assert o == x

    def test_1(self):
        sBase = Base(os.getcwd(), '1')
        print('test ende f')
        fk = Faker()
        ns = [fk.name().encode() for a in range(200)]
        print('test ende making data f')
        list(map(self.t, ns))
        sBase.quit()
        sBase.reset()
        del sBase

class TestInit:
    def setup_class(self):
        print('test init init')
        self.d = Base(os.getcwd(), 'testinit')
        fk = self.fk = Faker()
        ns = [(fk.name(), fk.country()) for a in range(50)]
        adt = time.time()
        self.d.add_all(ns)
        while len(self.d) != 50: pass 
        ut = time.time() - adt
        print('add 50 use time', ut)
        upt = timeit(lambda:self.d.update(), number=1)
        print('update...write..in  use time', upt, '\bs')
        self.read()
        self.index()
        self._index()
        self.d.reset()

    def read(self):
        print('test read')
        b = Base(os.getcwd(), 'testinit')
        print('reading for TestInit')
        adt = time.time()
        b.init()
        while len(b) != 50: print(len(b)); time.sleep(0.05)
        ut = time.time() - adt
        print('init time use', ut)
        assert b.de == self.d.de, (str(b.de[5]), str(self.d.de[5]))
        b.quit()

    def index(self):
        print('test index f')
        print('index..', end='')
        i = deque()
        for d in self.d.de:
            assert not d in i
            i.append(d)
        print('.')

    def _index(self):
        d = Base(os.getcwd(), 'testinit')
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
        d = Base(os.getcwd(), 'testinit')
        d.quit()
        d.reset()

class My:
    def __str__(self):
        return ":MY"

def test_to_string():
    print('test to string f')
    ba = Base(os.getcwd(), 'testinit')
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
        b = Base('/hm/p/slo')
    except FileNotFoundError:
        pass

def test_remove():
    print('test rev')
    b = Base(os.getcwd(), 'tr')
    fk = Faker()
    dts = [(fk.name().encode(), ) for _ in range(10)]
    b.add_all(dts)
    while len(b) < 10:pass
    re = b.deepsearch(dts[1][0])
    assert re, (b.de, "No search res")
    i, v = re[0]
    assert tuple(v) == dts[1], (i, v)
    b.remove(i)
    assert len(b) == 9
    print(b[:], dts[:], sep='\n')
    b.reset()
    b.quit()
    del b

def test_writein():
    print('test init init')
    d = Base(os.getcwd(), 'testinit')
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
    d.reset()

