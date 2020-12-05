import zlib
import base64

DEF __all__ = ("csv_b85en", "csv_b85de", 
        "csv_a85en", "csv_a85de", "csv_b85cen", "csv_b85cde", 
        "csv_b64en", "csv_b64de", "csv_b64cen", "csv_b64cde",
        )

DEF _csv_encode_trans = bytes.maketrans(b',', b'\x00')
DEF _csv_decode_trans = bytes.maketrans(b'\x00', b',')


def csv_b64en(s):
    return base64.b64encode(s).translate(_csv_encode_trans)

def csv_b64de(s):
    return base64.b64decode(s.translate(_csv_decode_trans))

def csv_b64cen(s):
    return csv_b64en(zlib.compress(s))

def csv_b64cde(s):
    return zlib.decompress(csv_b64de(s))

def csv_b85cen(s):
    return csv_b85en(zlib.compress(s))

def csv_b85cde(s):
    return zlib.decompress(csv_b85de(s))

def csv_b85en(s):
    return base64.b85encode(s).translate(_csv_encode_trans)

def csv_b85de(s):
    return base64.b85decode(s.translate(_csv_decode_trans))

def csv_a85en(s):
    return base64.a85encode(s).translate(_csv_encode_trans)

def csv_a85de(s):
    return base64.a85decode(s.translate(_csv_decode_trans))
