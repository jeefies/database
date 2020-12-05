from collections import deque

from .data import base

class Model(base):
    __cols__ = ()
    __support_type = (int, list, tuple, 
            float, complex)

    def __init__(self, workplace, workname):
        super(Model, self).__init__(workplace, workname)
        self.__anacols()

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

    def _org(self, row):
        r = dict()
        de = self._deb
        ge = ((de(i) if i else b'') for i in row)
        ts = self.to_string
        return {k:(t(ts(v)) if v else t()) for v,t,k in zip(ge, self.__cols_type, self.__cols)}

    def _anain(self, args):
        tb = self.to_bytes
        en = self._enb
        a = deque(en(tb(v)) for v in args)
        e = self.__coll - len(a)
        if e < 0: raise OverflowError("Data overflow")
        a.extend((b'',) * e)
        return a

    def search(self, exp, col=None):
        try:
            _col = self.__cols.index(col) if col else None
        except:
            _col = None
        return self.deepsearch(exp, _col)
