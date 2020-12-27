from collections import deque

class Deque(deque):
    def pop(self):
        p, l = super(Deque, self).pop(), len(self)
        return l, p

    def __getitem__(self, index):
        return index, super(Deque, self).__getitem__(index)

    def _slice(self, sli):
        a, e, o = sli.start, sli.stop, sli.step
        a, e, o = (a if a else 0), (e if e else len(self)), (o if o else 1)
        gi = self.item
        return Deque(gi(i) for i in range(a, e, o))

    def popi(self, index):
        c = self[index]
        s = self._slice(slice(0, index)) + self._slice(slice(index + 1, len(self)))
        self.clear()
        self.extend(s)
        return c

    def popo(self):
        return super(Deque, self).pop()

    def item(self, index):
        return super(Deque, self).__getitem__(index)

    def iter(self):
        for i, v in enumerate(self):
            yield (i, v)

class MDeque(deque):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rows = deque()

    def __setitem__(self, index, val):
        i = self.rows.index(index)
        super(MDeque, self).__setitem__(i, val)

    def __getitem__(self, index):
        return super(MDeque, self).__getitem__(self.rows.index(index))

    def append(self, index, val):
        self.rows.append(index)
        return super().append(val)

    def pop(self):
        r = self.rows.pop()
        p = super().pop()
        return r, p

    def popo(self):
        return self.pop()[1]

    def item(self, index):
        return super().__getitem__(index)

    def iter(self):
        for i, v in zip(self.rows, self):
            yield (i, v)
