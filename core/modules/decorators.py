import time
from time import time, sleep
from typing import Callable, Any
from functools import wraps
from core.modules.exceptions import NegativeException
from core.modules.logger import Logger


log = Logger()


def memoize(function: callable) -> wraps:

    cache = {}

    @wraps(function)
    def wrapper(*args: any, **kwargs: any) -> dict[str]:
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = function(*args, **kwargs)
        return cache[key]
    return wrapper


def measure_execution_time(func: callable) -> callable:

    """
    measuring run time of a function
    """

    def wrapper() -> None:
        start = time()
        func()
        end = time() - start
        log.level.info(text=f'function run took {end:.3f} sec')
        print(f'function run took {end:.3f} sec')

    return wrapper


def negative(exception_type: Exception(any)) -> Callable:
    """
    This decorator function takes in an exception type as an argument
    and returns a decorator that wraps the original function.
    When the new function is called, it calls the original
    function with the same arguments and catches any specified exception that might be raised.
    If the specified exception is caught, it logs the error message.
    If the specified exception is not raised, it raises an AssertionError.

    :param exception_type: The type of exception to catch.
    :return: A decorator function.
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> None:
            try:
                func(*args, **kwargs)
            except exception_type as e:
                log.level.info(f"{func.__name__} raised {exception_type.__name__}, {e}")
                return
            log.level.info(f"{func.__name__} did not raise {exception_type.__name__}")
            raise AssertionError(f"{func.__name__} did not raise {exception_type.__name__}")

        return wrapper

    return decorator


@negative(Exception)
def test() -> None:
    raise ValueError("This is a test")


def retry(retries: int = 3, delay: float = 1) -> callable:

    if retries < 1 or delay <= 0:
        raise NegativeException(f'Are you high, mate? Positive numbers only, your number is: {retries}')

    def decorator(func: callable) -> callable:

        @wraps(func)
        def wrapper(*args, **kwargs) -> any:

            for i in range(1, retries + 1):  # 1 to retries + 1 since upper bound is exclusive
                try:
                    print(f'Running ({i}): {func.__name__}')
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == retries:
                        print(f'Error: {repr(e)}.')
                        print(f'"{func.__name__}()" failed after {retries} retries.')
                        break
                    else:
                        print(f'Error: {repr(e)} -> Retrying...')
                        sleep(delay)  # Add a delay before running the next iteration

        return wrapper

    return decorator
