from astroid import extract_node

from pylint_requests.utils import has_timeout


def test_positive_simple():
    node = extract_node('func(timeout=1)')
    assert has_timeout(node)


def test_positive_unpacked():
    node = extract_node(
        '''
        kwargs = {'timeout': 1}
        func(**kwargs)
        '''
    )
    assert has_timeout(node)


def test_negative_simple():
    node = extract_node('func()')
    assert not has_timeout(node)


def test_negative_unpacked():
    node = extract_node(
        '''
        kwargs = {'xxx': 'yyy'}
        func(**kwargs)
        '''
    )
    assert not has_timeout(node)


def test_avoid_false_positives():
    node = extract_node(
        '''
        def func(**kwargs):
            other_func(**kwargs)  #@
        '''
    )
    assert has_timeout(node)
