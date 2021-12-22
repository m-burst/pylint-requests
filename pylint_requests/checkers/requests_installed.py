from typing import Optional

from pylint.checkers import BaseChecker
from pylint.checkers.utils import check_messages
from pylint.lint import PyLinter

from ..__pkginfo__ import BASE_ID


class RequestsInstalledChecker(BaseChecker):
    name = 'requests-installed-checker'

    msgs = {
        f'F{BASE_ID}01': (
            'Requests is not available on the PYTHONPATH',
            'requests-not-available',
            'Requests could not be imported by the pylint-requests plugin, so most '
            'Requests-related improvements to pylint will fail.',
        )
    }

    def __init__(self, linter: Optional[PyLinter] = None):
        super().__init__(linter)
        self._ran = False

    @check_messages('requests-not-available')
    def close(self) -> None:
        # hack to avoid displaying the same message for every file
        if self._ran:
            return
        self._ran = True

        try:
            __import__('requests')
        except ImportError:  # pragma: no cover
            self.add_message('requests-not-available')
