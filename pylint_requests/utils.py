from typing import List

from astroid import AstroidIndexError, AstroidTypeError, InferenceError, bases, nodes
from astroid.exceptions import AttributeInferenceError

try:
    from astroid.nodes import NodeNG
except ImportError:  # astroid < 2.7.0  # pragma: no cover
    from astroid.node_classes import NodeNG

FUNCTION_NODES = (nodes.FunctionDef, bases.UnboundMethod, bases.BoundMethod)

REQUESTS_API_MODULES = {'requests', 'requests.api'}
HTTP_METHOD_FUNCTIONS = {'request', 'head', 'get', 'post', 'put', 'patch', 'delete'}

SESSION_MODULE = 'requests.sessions'
SESSION_CLASS_NAME = 'Session'
SESSION_ONLY_METHODS = {'send'}
SESSION_METHODS = HTTP_METHOD_FUNCTIONS | SESSION_ONLY_METHODS

TIMEOUT_ARG = 'timeout'


def is_requests_api_module(node: NodeNG) -> bool:
    """True if node represents the requests or requests.api module."""

    if isinstance(node, (nodes.Name, nodes.Expr)):
        _, assigns = node.lookup(node.name)
        for assign in assigns:
            if (
                isinstance(assign, (nodes.Import, nodes.ImportFrom))
                and assign.real_name(node.name) in REQUESTS_API_MODULES
            ):
                return True

    return False


def is_session_class(node: NodeNG) -> bool:
    """True if node represents the requests.Session class."""

    try:
        for inferred in node.infer():
            if (
                isinstance(inferred, nodes.ClassDef)
                and inferred.name == SESSION_CLASS_NAME
                and isinstance(inferred.parent, nodes.Module)
                and inferred.parent.name == SESSION_MODULE
            ):
                return True
    except InferenceError:
        pass

    return False


def _lookup(node: NodeNG) -> List[NodeNG]:
    """Given a name or attribute node, returns the assignments to that name/attr."""

    if isinstance(node, nodes.Name):
        return node.lookup(node.name)[1]

    if isinstance(node, nodes.Attribute):
        try:
            obj = next(node.expr.infer())
        except InferenceError:
            return []

        if isinstance(obj, bases.Instance):
            try:
                return obj.getattr(node.attrname)
            except AttributeInferenceError:
                return []

    return []


def _is_session_argument(arguments: nodes.Arguments, name: str) -> bool:
    """Returns True if the argument with the given name is annotated as Session."""

    args = arguments.args + arguments.kwonlyargs
    annotations = arguments.annotations + arguments.kwonlyargs_annotations
    for arg, annotation in zip(args, annotations):
        if annotation is not None and arg.name == name and is_session_class(annotation):
            return True
    return False


def is_requests_session(node: NodeNG) -> bool:
    """Returns True if node represents a requests.Session object."""

    assigns = _lookup(node)
    for assign in assigns:
        if hasattr(assign, 'assign_type'):
            assign = assign.assign_type()

        if isinstance(assign, nodes.Assign):
            if isinstance(assign.value, nodes.Call) and is_session_class(
                assign.value.func
            ):
                return True
            if isinstance(assign.value, nodes.Name) and is_requests_session(
                assign.value
            ):
                return True

        if isinstance(assign, nodes.AnnAssign) and is_session_class(assign.annotation):
            return True

        if isinstance(assign, nodes.Arguments):
            if _is_session_argument(assign, node.name):
                return True

    return False


def is_requests_func(node: NodeNG) -> bool:
    """
    Checks if the node represents a requests HTTP call function.

    Examples are: requests.get/post/..., requests.Session.get/post/...
    """

    # simple case
    if isinstance(node, nodes.Attribute) and node.attrname in SESSION_METHODS:
        if (
            is_requests_api_module(node.expr)
            and node.attrname not in SESSION_ONLY_METHODS
        ) or is_requests_session(node.expr):
            return True

    if isinstance(node, nodes.Name):
        _, assigns = node.lookup(node.name)
        for assign in assigns:
            if (
                isinstance(assign, nodes.ImportFrom)
                and assign.modname in REQUESTS_API_MODULES
                and assign.real_name(node.name) in HTTP_METHOD_FUNCTIONS
            ):
                return True

            if hasattr(assign, 'assign_type'):
                assign = assign.assign_type()

            if isinstance(assign, nodes.Assign) and is_requests_func(assign.value):
                return True

    return False


def _check_key_in_dict(dict_node: nodes.Dict, key: str) -> bool:
    """Returns True if the dict node contains the given key."""

    try:
        dict_node.getitem(nodes.Const(value=key))
        return True
    except AstroidIndexError:
        return False
    except AstroidTypeError:  # pragma: no cover
        return True  # to avoid false positives


def _check_key_in_kwargs(unpacked: NodeNG, key: str) -> bool:
    """Given a **kwargs node in a function call, tries to check presence of a key."""

    try:
        for inferred in unpacked.infer():
            if (
                isinstance(inferred, nodes.Dict)
                and inferred.items
                and not _check_key_in_dict(inferred, key)
            ):
                # only if we know that it is a dict and astroid inferred some values
                return False
    except InferenceError:
        pass

    return True


def has_timeout(node: nodes.Call) -> bool:
    """Returns True if the call contains a timeout argument."""

    if not node.keywords:
        return False

    for keyword in node.keywords:
        if keyword.arg == TIMEOUT_ARG:
            return True
        if keyword.arg is None and _check_key_in_kwargs(keyword.value, TIMEOUT_ARG):
            return True

    return False
