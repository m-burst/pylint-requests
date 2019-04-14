import pytest
from astroid import extract_node

from pylint_requests.utils import is_requests_func


@pytest.mark.parametrize(
    'func_name', ['request', 'head', 'get', 'post', 'put', 'patch', 'delete']
)
def test_module_func_simple(func_name):
    node = extract_node(
        f'''
        import requests

        requests.{func_name}
        '''
    )
    assert is_requests_func(node)


def test_module_func_imported():
    node = extract_node(
        '''
        from requests import get as custom_name

        custom_name
        '''
    )
    assert is_requests_func(node)


def test_module_func_assigned():
    node = extract_node(
        '''
        import requests

        custom_name = requests.get
        custom_name
        '''
    )
    assert is_requests_func(node)


def test_not_requests():
    node = extract_node(
        '''
        requests = {}
        requests.get
        '''
    )
    assert not is_requests_func(node)


@pytest.mark.parametrize(
    'method_name', ['request', 'head', 'get', 'post', 'put', 'patch', 'delete', 'send']
)
def test_session_method_simple(method_name):
    node = extract_node(
        f'''
        import requests

        session = requests.Session()
        session.{method_name}
        '''
    )
    assert is_requests_func(node)


def test_session_method_by_annotation():
    node = extract_node(
        '''
        from requests import Session

        session: Session = get_session_from_somewhere()
        session.get
        '''
    )
    assert is_requests_func(node)


def test_session_method_in_function():
    node = extract_node(
        '''
        import requests

        def request_api(sess: requests.Session):
            sess.get  #@
        '''
    )
    assert is_requests_func(node)


def test_session_method_in_class():
    node = extract_node(
        '''
        import requests

        class MyAPIClient:
            def __init__(self):
                self.http = requests.Session()

            def test_method(self):
                self.http.get  #@
        '''
    )
    assert is_requests_func(node)


def test_session_method_from_constructor_parameter():
    node = extract_node(
        '''
        import requests

        class MyAPIClient:
            def __init__(self, http: requests.Session):
                self.http = http

            def test_method(self):
                self.http.get  #@
        '''
    )
    assert is_requests_func(node)


def test_some_other_session_class():
    node = extract_node(
        '''
        class Session:
            def get(self, *args, **kwargs):
                pass

        class MyAPIClient:
            def __init__(self, session: Session):
                self.session = session

            def test_method(self):
                self.session.get  #@
        '''
    )
    assert not is_requests_func(node)
