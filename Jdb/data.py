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

from .mydeque import Deque
from .csvbase import csv_b64cen, csv_b64cde, csv_b85cen, csv_b85cde


class base:

    @classmethod
    def _64enb(cls, x):
        return csv_b64cen(cls.to_bytes(x))

    @classmethod
    def _64deb(cls, x):
        return csv_b64cde(x)

    @classmethod
    def _85enb(cls, x):
        return csv_b85cen(cls.to_bytes(x))

    @classmethod
    def _85deb(cls, x):
        return csv_b85cde(x)

    _enb = _85enb
    _deb = _85deb

    def __init__(self, place, name='', Inet=False):
        pl = os.path.abspath(place)
        if os.path.exists(pl):
            self.pl = pl
            self.name = name
            self.file = os.path.join(self.pl, '{}.Jdb'.format(name))
        else:
            raise FileNotFoundError('No such directory')
        self.de = Deque()
        self.__adds = deque()

        def _unix(self):
            self._sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
            self._sockr = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        
            self._sock_path = os.path.join(self.pl, './.J{}.d'.format(name))
            if os.path.exists(self._sock_path):
                os.unlink(self._sock_path)

        def _inet(self):
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._sockr = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
            self._sock_path = ('localhost', 10001)

        if Inet:
            _inet(self)
        else:
            try:
                _unix(self)
            except:
                _inet()

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
                    self.__adi()
            except: pass

    def __adi(self):
        l = self.__adds.popleft()
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
        self.__adds.append(args)
        # self._sock.send(b's')
        self._sock.sendto(b's', self._sock_path)  # for udp connection

    def add_all(self, li_tup):
        self.__adds.extend(li_tup)
        for _ in li_tup:
            self._sock.sendto(b's', self._sock_path)
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
        with bz2.open(self.file, 'wb', 9) as f:
            return f.write(self._bytes())

    def deepsearch(self, exp, col=None):
        de = self.de.copy()
        exp = self._enb(exp)
        res = deque()

        async def find(d, r):
            while 1:
                try:
                    o = d.pop()
                    out = o[1]
                    if (exp == out[col] if (col is not None) else (exp in out)):
                        r.append((o[0], self._org(out)))
                except:
                    return 0
        li = [find(de, res) for _ in range(5)]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(li))
        return res

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
        if isinstance(b, base):
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
        try:
            sockname = os.path.basename(self._sock_path)
            while sockname in os.listdir(self.pl):
                os.remove(self._sock_path)  # remove socket use file
            self._sock.shutdown(socket.SHUT_RDWR)
            self._sockr.shutdown(socket.SHUT_RDWR)
            self.update()
            return 0
        except:
            return 1

    def __str__(self):
        return repr(self._bytes())[2:-1]

    def init(self):
        if not os.path.exists(self.file):
            codecs.open(self.file, 'x').close()
            return None

        with bz2.open(self.file, 'rb') as f:
            def lines():
                l = b''
                e = 0
                while 1:
                    l += f.readline()
                    if not l:
                        e += 1
                        if e > 2:
                            break
                        else:
                            continue
                    if l.endswith(b'YZ\n') or l.endswith(b'YZ'):
                        yield lzma.decompress(l.strip())
                        l = b''
                        e = 0

            for l in lines():
                self.de.append(deque(l.split(b',')))

    def _bytes(self):
        async def c(s):
            return lzma.compress(s)
        s = tuple(b','.join(each) for each in self.de)
        fs = [c(i) for i in s]
        loop = asyncio.get_event_loop()
        rs = loop.run_until_complete(asyncio.gather(*fs))
        return b'\n'.join(rs)

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
