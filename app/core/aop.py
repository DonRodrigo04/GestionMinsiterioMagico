# app/core/aop.py
import inspect
from functools import wraps
from typing import Any, Callable

Func = Callable[..., Any]

async def _maybe_await(func: Func, *args, **kwargs) -> Any:
    """Ejecuta func sea sync o async."""
    if inspect.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    return func(*args, **kwargs)


def before(before_func: Func):
    """Aspecto simple: ejecuta before_func antes de la función objetivo."""
    def decorator(target: Func) -> Func:
        if inspect.iscoroutinefunction(target):
            @wraps(target)
            async def async_wrapper(*args, **kwargs):
                await _maybe_await(before_func, *args, **kwargs)
                return await target(*args, **kwargs)
            return async_wrapper  # type: ignore
        else:
            @wraps(target)
            def sync_wrapper(*args, **kwargs):
                before_func(*args, **kwargs)
                return target(*args, **kwargs)
            return sync_wrapper  # type: ignore
    return decorator


def after(after_func: Func):
    """Aspecto simple: ejecuta after_func después de la función objetivo."""
    def decorator(target: Func) -> Func:
        if inspect.iscoroutinefunction(target):
            @wraps(target)
            async def async_wrapper(*args, **kwargs):
                result = await target(*args, **kwargs)
                await _maybe_await(after_func, *args, **kwargs, result=result)
                return result
            return async_wrapper  # type: ignore
        else:
            @wraps(target)
            def sync_wrapper(*args, **kwargs):
                result = target(*args, **kwargs)
                after_func(*args, **kwargs, result=result)
                return result
            return sync_wrapper  # type: ignore
    return decorator


def around(before_func: Func | None = None, after_func: Func | None = None):
    """Aspecto around: puede ejecutar lógica antes y después."""
    def decorator(target: Func) -> Func:
        if inspect.iscoroutinefunction(target):
            @wraps(target)
            async def async_wrapper(*args, **kwargs):
                if before_func:
                    await _maybe_await(before_func, *args, **kwargs)
                try:
                    result = await target(*args, **kwargs)
                    return result
                finally:
                    if after_func:
                        await _maybe_await(after_func, *args, **kwargs, result=result)
            return async_wrapper  # type: ignore
        else:
            @wraps(target)
            def sync_wrapper(*args, **kwargs):
                if before_func:
                    before_func(*args, **kwargs)
                try:
                    result = target(*args, **kwargs)
                    return result
                finally:
                    if after_func:
                        after_func(*args, **kwargs, result=result)
            return sync_wrapper  # type: ignore
    return decorator
