#!/usr/bin/env python3
"""Redis exercise module"""

import redis
import uuid
from functools import wraps
from typing import Union, Callable


def call_history(method: Callable) -> Callable:
    """Stores the history of inputs and outputs for a particular function."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Stores the history of inputs and outputs for a particular function.
        """
        input_key = f'{method.__qualname__}:inputs'
        output_key = f'{method.__qualname__}:outputs'
        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, output)
        return output
    return wrapper


def count_calls(method: Callable) -> Callable:
    """Function that counts how many times a function has been called."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Function that increments the count for a particular key every time.
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


class Cache(object):
    """Provides some methods to interact with Redis instance."""
    def __init__(self) -> None:
        """Initialize Redis instance."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Function that takes a data argument and returns a string."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes,
                                                          int, float]:
        """Takes a key string argument and an optional Callable argument."""
        value = self._redis.get(key)
        return value if fn is None else fn(value)

    def get_str(self, key: str) -> str:
        """Function that takes a key string argument and returns a string."""
        return self.get(
            key,
            lambda s: s.decode('utf-8')
        )

    def get_int(self, key: str) -> int:
        """Function that takes a key string argument and returns an integer."""
        return self.get(key, lambda n: int(n))


def replay(fn: Callable) -> None:
    """
    Displays the history of calls of a particular function.
    """
    name = fn.__qualname__
    cache = redis.Redis()
    calls = cache.get(name).decode("utf-8")
    print("{} was called {} times:".format(name, calls))
    inputs = cache.lrange(name + ":inputs", 0, -1)
    outputs = cache.lrange(name + ":outputs", 0, -1)
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(name, i.decode('utf-8'),
                                     o.decode('utf-8')))
