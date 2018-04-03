import pytest
import intervals as I


def test_infinity():
    assert I.inf == I.inf
    assert I.inf >= I.inf
    assert I.inf <= I.inf
    assert not (I.inf > I.inf)
    assert not (I.inf < I.inf)
    assert not (I.inf != I.inf)

    assert -I.inf == -I.inf
    assert -I.inf >= -I.inf
    assert -I.inf <= -I.inf
    assert not (-I.inf > -I.inf)
    assert not (-I.inf < -I.inf)
    assert not (-I.inf != -I.inf)

    assert I.inf > -I.inf
    assert -I.inf < I.inf
    assert -I.inf != I.inf
    assert not (-I.inf == I.inf)


def test_creation():
    assert I.closed(0, 1) == I.AtomicInterval(I.CLOSED, 0, 1, I.CLOSED)
    assert I.open(0, 1) == I.AtomicInterval(I.OPEN, 0, 1, I.OPEN)
    assert I.openclosed(0, 1) == I.AtomicInterval(I.OPEN, 0, 1, I.CLOSED)
    assert I.closedopen(0, 1) == I.AtomicInterval(I.CLOSED, 0, 1, I.OPEN)


def test_to_interval_to_atomic():
    intervals = [I.closed(0, 1), I.open(0, 1), I.openclosed(0, 1), I.closedopen(0, 1)]
    for interval in intervals:
        assert interval == I.Interval(interval.to_atomic())
        assert interval == interval.to_atomic()

    assert I.closed(0, 1) | I.closed(2, 3) != I.closed(0, 3)
    assert (I.closed(0, 1) | I.closed(2, 3)).to_atomic() == I.closed(0, 3)


def test_emptyness():
    assert I.openclosed(1, 1).is_empty()
    assert I.closedopen(1, 1).is_empty()
    assert I.open(1, 1).is_empty()
    assert not I.closed(1, 1).is_empty()


def test_containment():
    # Values
    assert 1 in I.closed(0, 2)
    assert 1 in I.closed(1, 2)
    assert 1 in I.closed(0, 1)

    assert 1 in I.open(0, 2)
    assert 1 not in I.open(0, 1)
    assert 1 not in I.open(1, 2)

    assert 1 in I.closed(-I.inf, I.inf)
    assert 1 in I.closed(-I.inf, 1)
    assert 1 in I.closed(1, I.inf)
    assert 1 not in I.closed(-I.inf, 0)
    assert 1 not in I.closed(2, I.inf)

    # Intervals
    assert I.closed(1, 2) in I.closed(0, 3)
    assert I.closed(1, 2) in I.closed(1, 2)
    assert I.open(1, 2) in I.closed(1, 2)
    assert I.closed(1, 2) not in I.open(1, 2)
    assert I.closed(0, 1) not in I.closed(1, 2)
    assert I.closed(0, 2) not in I.closed(1, 3)
    assert I.closed(-I.inf, I.inf) in I.closed(-I.inf, I.inf)
    assert I.closed(0, 1) in I.closed(-I.inf, I.inf)
    assert I.closed(-I.inf, I.inf) not in I.closed(0, 1)


def test_intersection():
    assert I.closed(0, 1) & I.closed(0, 1) == I.closed(0, 1)
    assert I.closed(0, 1) & I.open(0, 1) == I.open(0, 1)
    assert I.openclosed(0, 1) & I.closedopen(0, 1) == I.open(0, 1)
    assert (I.closed(0, 1) & I.closed(2, 3)).is_empty()


def test_union():
    assert I.closed(1, 2) | I.closed(1, 2) == I.closed(1, 2)
    assert I.closed(1, 4) | I.closed(2, 3) == I.closed(1, 4)
    
    assert I.closed(1, 2) | I.open(2, 3) == I.closedopen(1, 3)
    assert I.closed(1, 3) | I.closed(2, 4) == I.closed(1, 4)
    
    assert I.closedopen(1, 2) | I.closed(2, 3) == I.closed(1, 3)
    assert I.open(1, 2) | I.closed(2, 4) == I.openclosed(1, 4)

    assert I.closed(1, 2) | I.closed(3, 4) != I.closed(1, 4)
    assert (I.closed(1, 2) | I.closed(3, 4) | I.closed(2, 3)).is_atomic()
    assert I.closed(1, 2) | I.closed(3, 4) | I.closed(2, 3) == I.closed(1, 4)

    assert (I.closed(0, 1) | I.closed(2, 3) | I.closed(1, 2)).is_atomic()
    assert I.closed(0, 1) | I.closed(2, 3) | I.closed(1, 2) == I.closed(0, 3)


def test_complement():
    assert ~I.closed(1, 2) == I.open(-I.inf, 1) | I.open(2, I.inf)
    assert ~I.open(1, 2) == I.openclosed(-I.inf, 1) | I.closedopen(2, I.inf)

    intervals = [I.closed(0, 1), I.open(0, 1), I.openclosed(0, 1), I.closedopen(0, 1)]
    for interval in intervals:
        assert ~(~interval) == interval


def test_example():
    example = """
    >>> I.closed(0, 3)
    [0,3]
    >>> I.openclosed('a', 'z')
    ('a','z']
    >>> I.openclosed(-I.inf, 0)
    (-inf,0]
    >>> 2 in I.closed(0, 3)
    True
    >>> I.closed(0, 2) & I.open(1, 4)
    (1,2]
    >>> I.closed(0, 1) & I.closed(2, 3)
    ()
    >>> I.closed(0, 2) | I.open(1, 4)
    [0,4)
    >>> I.closed(0, 1) | I.closed(2, 3) | I.closed(1, 2)
    [0,3]
    >>> I.closed(0, 1) | I.closed(2, 3)
    [0,1] | [2,3]
    >>> ~I.closed(0, 1)
    (-inf,0) | (1,+inf)
    >>> ~(I.closed(0, 1) | I.open(2, 3))
    (-inf,0) | (1,2] | [3,+inf)
    """
    lines = iter(example.strip().splitlines())
    for line in lines:
        assert repr(eval(line.strip().replace('>>> ', ''))) == next(lines).strip()