__version__ = '0.1.1'

from pylint.lint import PyLinter

from .checkers import RequestsInstalledChecker, TimeoutChecker


def register(linter: PyLinter) -> None:  # pragma: no cover
    linter.register_checker(RequestsInstalledChecker(linter))
    linter.register_checker(TimeoutChecker(linter))
