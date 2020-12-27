from ._mydeque import Deque, MDeque

def test_full():
    de = Deque(range(50))
    assert de.pop() == (49, 49)
    print(de)
    r = de[1]
    assert de.popi(1) == r, (de.popi(1), r)
    assert list(de) == list(range(1)) + list(range(2, 49))
    assert de.popo() == 48

def test_mdeque():
    de = MDeque()
    de.append('index', 'val')
    print(de['index'])
    de['index'] = 'changed'
    assert de['index'] == 'changed'

    print(de.pop())
    de.append('index2', 'val2')
    de.append('index3', 'val3')
    de.append('index4', 'val4')
    p = de.popo()
    assert p == 'val4'
    print(p)
    print(de.item(1))
    assert list(map(lambda x : x[1], de.iter())) == list(de)
