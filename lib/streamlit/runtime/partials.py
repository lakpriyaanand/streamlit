import hashlib
from functools import wraps
from typing import (
    Any,
    Callable,
    Iterator,
    MutableMapping,
    Optional,
    TypeVar,
    Union,
    overload,
)

import cloudpickle

from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.runtime.state.session_state_proxy import get_session_state

F = TypeVar("F", bound=Callable[..., Any])


@overload
def partial(
    func: F,
) -> F:
    ...


@overload
def partial(
    func: None = None,
) -> Callable[[F], F]:
    ...


def partial(func: Optional[F] = None) -> Union[Callable[[F], F], F]:
    if func is None:
        # Support passing the params via function decorator
        def wrapper(f: F) -> F:
            return partial(
                func=f,
            )

        return wrapper
    else:
        # To make mypy type narrow Optional[F] -> F
        non_optional_func = func

    h = hashlib.new("md5")
    # TODO: find something better to hash
    h.update(f"{callable.__module__}.{callable.__qualname__}".encode("utf-8"))
    partial_id = h.hexdigest()
    partial_storage = PartialsStorage()

    @wraps(non_optional_func)
    def wrap(*args, **kwargs):
        ctx = get_script_run_ctx()
        if ctx is None:
            return
        dg_stack = ctx.dg_stack

        def wrapped_group():
            print("Start function")
            # import streamlit as st
            from streamlit.runtime.scriptrunner import get_script_run_ctx

            ctx = get_script_run_ctx(suppress_warning=True)
            assert ctx is not None

            ctx.dg_stack = dg_stack
            # Set dg stack to outside state
            print(type(ctx.dg_stack))
            print(ctx.dg_stack)
            ctx.current_partial_id = partial_id

            result = callable(*args, **kwargs)

            # TODO: always reset to None -> otherwise problems with exceptions
            ctx.current_partial_id = None
            return result

        partial_storage[partial_id] = cloudpickle.dumps(wrapped_group)
        return wrapped_group()

    return wrap


class PartialsStorage(MutableMapping[str, bytes]):
    """A storage for partials that is backed by the session state."""

    def _get_partials_state(self) -> MutableMapping[str, bytes]:
        # TODO(lukasmasuch): This is just a super hacky solution for storing partials
        # We should create a dedicated partials storage outside of the session state.
        session_state = get_session_state()
        if "_st_partials" not in session_state:
            session_state["_st_partials"] = {}
        return session_state["_st_partials"]  # type: ignore

    def __iter__(self) -> Iterator[Any]:
        """Iterator over all partials."""
        return iter(self._get_partials_state())

    def __len__(self) -> int:
        """Number of partials in the partial storage."""
        return len(self._get_partials_state())

    def __str__(self) -> str:
        """String representation of the partial state."""
        return str(self._get_partials_state())

    def __getitem__(self, key: str) -> bytes:
        """Return a specific partial."""
        return self._get_partials_state()[key]

    def __setitem__(self, key: str, value: bytes) -> None:
        """Store the bytes for a given partial."""
        self._get_partials_state()[key] = value

    def __delitem__(self, key: str) -> None:
        """Delete the bytes of a given partial."""
        del self._get_partials_state()[key]

    def clear(self) -> None:
        return self._get_partials_state().clear()