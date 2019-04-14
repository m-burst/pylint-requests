from astroid import extract_node, parse
from pylint.testutils import CheckerTestCase, Message

from pylint_requests import RequestsInstalledChecker, TimeoutChecker


class TestTimeoutChecker(CheckerTestCase):
    CHECKER_CLASS = TimeoutChecker

    def test_has_timeout(self):
        module = parse(
            '''
            import requests

            requests.get('url', timeout=1)
            '''
        )
        with self.assertNoMessages():
            self.walk(module)

    def test_not_requests(self):
        module = parse(
            '''
            requests = {}
            requests.get('url')
            '''
        )
        with self.assertNoMessages():
            self.walk(module)

    def test_no_timeout(self):
        node = extract_node(
            '''
            import requests

            requests.get('url')
            '''
        )

        with self.assertAddsMessages(Message('request-without-timeout', node=node)):
            self.walk(node.root())


class TestRequestsInstalledChecker(CheckerTestCase):
    CHECKER_CLASS = RequestsInstalledChecker

    def test_installed(self):
        with self.assertNoMessages():
            self.checker.close()
