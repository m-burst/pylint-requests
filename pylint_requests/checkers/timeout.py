from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.checkers.utils import check_messages
from pylint.interfaces import IAstroidChecker

from ..__pkginfo__ import BASE_ID
from ..utils import has_timeout, is_requests_func


class TimeoutChecker(BaseChecker):
    __implements__ = IAstroidChecker

    name = 'requests-timeout-checker'

    msgs = {
        f'E{BASE_ID}01': (
            'HTTP request without timeout',
            'request-without-timeout',
            'An HTTP request is being made without a timeout specified. '
            'You should specify the timeout as a keyword argument.',
        )
    }

    @check_messages('request-without-timeout')
    def visit_call(self, node: nodes.Call) -> None:
        if not is_requests_func(node.func):
            return

        if not has_timeout(node):
            self.add_message('request-without-timeout', node=node)
