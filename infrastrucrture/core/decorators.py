import time
from time import time
from time import sleep
from functools import wraps
from infrastrucrture.core.exceptions import NegativeIntegerException
from infrastrucrture.engine.driver_engine import log


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
        log(text=f'function run took {end:.3f} sec')
        print(f'function run took {end:.3f} sec')

    return wrapper


def negative(exception_type: Exception(any)):

    """
    This decorator function takes in a function as an argument
    and returns a new function that wraps the original function.
    When the new function is called, it calls the original
    function with the same arguments and catches any AssertionError that might be raised.
    If an AssertionError is caught, it prints out the error message and then re-raises the exception.

    """

    def decorator(func) -> callable:
        def wrapper(*args: any, **kwargs: any) -> None:
            try:
                log(text=f"{func.__name__} raised {exception_type.__name__}")
                func(*args, **kwargs)
            except exception_type:
                log(text=f"{func.__name__} did not raise {exception_type.__name__}")
                return
            raise AssertionError(f"{func.__name__} did not raise {exception_type.__name__}")

        return wrapper

    return decorator


def retry(retries: int = 3, delay: float = 1) -> callable:

    if retries < 1 or delay <= 0:
        raise NegativeIntegerException(f'Are you high, mate? Positive numbers only, your number is: {retries}')

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
