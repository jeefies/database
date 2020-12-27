from collections import deque

from .data import Base
from ._mydeque import MDeque

class Model(Base):
    __cols__ = ()
    __support_type = (int, float, complex, 
            str, bytes, bytearray)

    def __init__(self, workplace, workname):
        super(Model, self).__init__(workplace, workname)
        self.__anacols()
        self.de = MDeque()

    def __anacols(self):
        self.__cols = deque()
        self.__cols_type = deque()
        for col in self.__cols__:
            if isinstance(col, (str, bytes, bytearray)):
                self.__cols.append(self.to_string(col))
                self.__cols_type.append(str)
            else:
                self.__cols.append(self.to_string(col[0]))
                if not col[1] in self.__support_type:
                    raise TypeError("Unsupport Type")
                self.__cols_type.append(col[1])
        self.__coll = len(self.__cols)

    def add(self, index, *args):
        super().add(index, *args)
        return {index, args}

    def add_all(self, dicts):
        for i in dicts:
            super().add(i, *dicts[i])
        return dicts

    def _org(self, row):
        de = self._deb
        ge = ((de(i) if i else b'') for i in row)
        ts = self.to_string
        return {k:(t(ts(v)) if v else t()) for v,t,k in zip(ge, self.__cols_type, self.__cols)}

    def _anain(self, vals):
        index = vals[0]
        args = vals[1:]
        tb = self.to_bytes
        en = self._enb
        a = deque(en(tb(v)) for v in args)
        e = self.__coll - len(a)
        if e < 0: raise OverflowError("Data overflow")
        a.extend((b'',) * e)
        return (index, a)

    def _adi(self):
        l = list(self._adds.popleft())
        i, v = self._anain(l)
        self.de.append(i, v)

    def search(self, exp, col=None):
        try:
            _col = self.__cols.index(col) if col else None
        except:
            _col = None
        return self.deepsearch(exp, _col)

    def modify(self, index, **kwargs):
        org = self._org(self.de[index])
        cols = self.__cols
        tb = self.to_bytes
        for k in kwargs:
            if not k in cols:
                raise KeyError('No such column')
            org[k] = tb(kwargs)
        self.de[i] = deque(self._deb(org[k]) for k in cols)

    def __getitem__(self, index):
        return self._org(self.de[index])
