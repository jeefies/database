import os
import csv
import zlib
import bz2
import lzma
import codecs
import socket
import asyncio
from collections import deque
from threading import Thread

from .._mydeque import Deque
from ..csvbase import csv_b64cen, csv_b64cde, csv_b85cen, csv_b85cde
from ..coder import LZMACoder


class Base:
    _instance = {}

    def __new__(self, place, name='', Inet=False):
        ins = self._instance
        if place in ins:
            if name in ins[place]:
                return ins[place][name]
            else:
                ins[place][name] = super().__new__(self)
                return ins[place][name]
        else:
            ins[place] = {name: super().__new__(self)}
            return ins[place][name]

    @classmethod
    def _64enb(cls, x):
        return csv_b64cen(cls.to_bytes(x))

    @classmethod
    def _64deb(cls, x):
        return csv_b64cde(x)

    @classmethod
    def _85enb(cls, x, _e = 0):
        try:
            return csv_b85cen(cls.to_bytes(x))
        except Exception as e:
            if _e:
                print(x, '(encode Error::', e)
                raise e
            cls._85enb(x, _e)

    @classmethod
    def _85deb(cls, x):
        return csv_b85cde(x)

    _enb = _85enb
    _deb = _85deb

    def __init__(self, place, name='', coder=LZMACoder, Inet=False):
        self._sock_inet = Inet
        self._pl = place
        pl = os.path.abspath(place)
        if os.path.exists(pl):
            self.pl = pl
            self.name = name
            self.file = os.path.join(self.pl, '{}.Jdb'.format(name))
        else:
            raise FileNotFoundError('No such directory')
        self.de = Deque()
        self._adds = deque()
        self._coder = coder

        def _unix(self):
            assert not Inet
            self._sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            self._sockr = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        
            self._sock_path = os.path.join(self.pl, './.J{}.d'.format(name))
            if os.path.exists(self._sock_path):
                os.unlink(self._sock_path)

        def _inet(self):
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._sockr = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
            self._sock_path = ('localhost', 10000)

        try:
            _unix(self)
        except:
            _inet(self)

        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sockr.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sockr.bind(self._sock_path)


        self._add_thrs = [Thread(target=self._Addthr) for _ in range(5)]
        [x.setDaemon(True) for x in self._add_thrs]
        [x.start() for x in self._add_thrs]

    def _Addthr(self):
        _e = None
        while 1:
            try:
                # recvfrom for udp connection, recv for tcp
                r, a = self._sockr.recvfrom(1)
                if r == b's':
                    self._adi()
                else:
                    break
            except Exception as e:
                print(e)

    def _adi(self):
        l = self._adds.popleft()
        ai = self._anain(l)
        self.de.append(ai)

    def _anain(self, l):
        return deque(self._enb(a) for a in l)

    def _index(self, index):
        return self._org(self.de[index][1])

    def add(self, *args):
        self._add(args)
        return args

    def _add(self, args):
        self._adds.append(args)
        self._sock.sendto(b's', self._sock_path)

    def add_all(self, li_tup):
        self._adds.extend(li_tup)
        sp = self._sock_path
        sk = self._sock
        for _ in li_tup:
            sk.sendto(b's', sp)
        return li_tup

    def remove(self, index):
        return self.de.popi(index)

    def reset(self):
        self.de.clear()
        try:
            os.remove(self.file)
            return 0
        except:
            return 1

    def update(self):
        with bz2.open(self.file, 'wb', 2) as f:
            return f.write(self._bytes())

    def modify(self, index, vals):
        self.remove(index)
        self.add(index)

    def deepsearch(self, exp, col=None):
        exp = self._enb(exp)

        def find(d, r):
            ap = r.append
            org = self._org
            if col is None:
                cond = lambda o : exp in o
            else:
                cond = lambda o : exp == o[col]

            for i, val in d.iter():
                    if cond(val):
                        ap((i, org(val)))
            return r
        return find(self.de, deque())

    def _org(self, de):
        return deque(self._deb(i) for i in de)

    @classmethod
    def to_string(cls, s, encode='utf-8'):
        if isinstance(s, str):
            return s
        elif isinstance(s, bytes):
            try:
                return codecs.decode(s, encode)
            except:
                return codecs.decode(s)
        else:
            return str(s)

    @classmethod
    def to_bytes(cls, b, encode='utf-8'):
        if isinstance(b, (bytes, bytearray)):
            return b
        if isinstance(b, Base):
            return b._bytes()
        try:
            return codecs.encode(b, encode)
        except:
            try:
                return codecs.encode(b)
            except:
                pass
            return codecs.encode(cls.to_string(b), encode)

    def quit(self):
        _e = 0

        try:
            for a in range(5):
                self._sock.sendto(b'q', self._sock_path)
        except Exception as e:
            _e = 1

        try:
            if isinstance(self._sock_path, str):
                sockname = os.path.basename(self._sock_path)
        except Exception as e:
            _e = 1

        try:
            while sockname in os.listdir(self.pl):
                os.remove(self._sock_path)  # remove socket use file
        except Exception as e:
            _e = 1

        try:
            self._instance[self._pl].pop(self.name)
        except Exception as e:
            _e = 1

        try:
            self._sock.shutdown(socket.SHUT_RDWR)
            self._sockr.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            _e = 1

        try:
            self.update()
        except Exception as e:
            _e = 1

        return _e

    def init(self):
        if not os.path.exists(self.file):
            codecs.open(self.file, 'x').close()
            return None

        with bz2.open(self.file, 'rb') as f:
            for l in self._coder.decode(f):
                self.de.append(deque(l.split(b',')))

    def _bytes(self):
        return self._coder.encode(self.de)

    def __del__(self):
        return self.quit()

    @staticmethod
    def _de_slice(de, start=None, end=None, step=None):
        if not start:
            start = 0
        if not end:
            end = len(de)
        if not step:
            step = 1
        return deque(de[a] for a in range(start, end, step))

    def __getitem__(self, index):
        if isinstance(index, slice):
            r = self._de_slice(self.de, index.start, index.stop, index.step)
            return deque((i[0], self._org(i[1])) for i in r)
        else:
            return self._org(self.de[index][1])

    def __len__(self):
        return len(self.de)
