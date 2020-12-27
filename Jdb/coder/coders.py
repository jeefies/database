import lzma

class LZMACoder:
    @classmethod
    def decode(cls, fp):
        ldc = lzma.decompress

        l = b''
        e = 0

        while True:
            l += fp.readline()
            if not l:
                e += 1
                if e > 2:
                    break
            else:
                if l.endswith(b'YZ\n') or l.endswidth(b'YZ'):
                    yield ldc(l.strip())
                    l = b''
                    e = 0

    @classmethod
    def encode(cls, de):
        lc = lzma.compress
        return b'\n'.join(map(lc, tuple(b','.join((e if e else b'') for e in each) for each in de)))

class NONECoder:
    @staticmethod
    def decode(fp):
        while True:
            r = fp.readline()
            if r:
                yield r
            else:
                break

    @staticmethod
    def encode(de):
        return b'\n'.join(b','.join((e if e else b'') for e in each) for each in de)
