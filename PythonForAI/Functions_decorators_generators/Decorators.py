import time
import time
from functools import wraps

# --- Plain decorator (no config args) ---
# `@timing` desugars to: slow_embedding = timing(slow_embedding)
# `@EXPR` always makes exactly ONE automatic call: EXPR(func_being_decorated).
# EXPR here is just the bare name `timing`, so that IS the automatic call -
# no extra call is needed because timing() takes no config, only func.
def timing(func):
    @wraps(func)
    # Copies func's __name__/__doc__/__qualname__ onto wrapper. Doesn't change
    # runtime behavior (the print below already reads func.__name__ directly,
    # not wrapper's), but without it slow_embedding.__name__ would report
    # "wrapper", breaking help()/inspect.signature()/anything keying off
    # __name__ (e.g. Flask route registration).
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs) # if we remove this func call still it would work.
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.3f}s")
        return result
    return wrapper

def slow_embedding(text):
    time.sleep(0.5)
    return [0.1, 0.2, 0.3]

slow_embedding = timing(slow_embedding)
slow_embedding("hello")  # slow_embedding took 0.501s

@timing  # -> slow_embedding = timing(slow_embedding); wrapper takes over the name
def slow_embedding(text):
    time.sleep(0.5)
    return [0.1, 0.2, 0.3]

slow_embedding("hello")  # slow_embedding took 0.500s


import time
from functools import wraps

# --- Parameterized decorator (needs its own config args) ---
# `@` only ever passes ONE thing automatically: the function being decorated.
# There's no way to also sneak max_retries/delay/backoff into that one
# automatic call, so retry() can't be a func-taking decorator directly -
# its params are config, not func.
#
# So retry() is a decorator FACTORY with 3 nested levels:
#   retry(max_retries, delay, backoff)  -> returns decorator (consumes config)
#   decorator(func)                     -> returns wrapper     (consumes func)
#   wrapper(*args, **kwargs)            -> runs on every actual call, later
#
# @retry(max_retries=3, delay=0.1, backoff=2.0) below desugars to TWO calls:
#   1) retry(max_retries=3, delay=0.1, backoff=2.0)  <- explicit, written by us,
#      needed just to evaluate the expression after @. Returns `decorator`
#      with max_retries/delay/backoff captured in its closure.
#   2) decorator(call_embedding_api)                  <- @'s one automatic call.
#      Returns `wrapper`, which replaces call_embedding_api.
def retry(max_retries=3, delay=1.0, backoff=2.0):
    def decorator(func):
        @wraps(func)  # same purpose as in timing() above: preserves
        # call_embedding_api's __name__/__doc__/signature on the wrapper
        # that replaces it.
        def wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        print(f"Attempt {attempt + 1} failed: {e}. "
                              f"Retrying in {current_delay:.1f}s...")
                        time.sleep(current_delay)
                        current_delay *= backoff

            raise last_exception
        return wrapper
    return decorator

failures_left = 2

@retry(max_retries=3, delay=0.1, backoff=2.0)  # see retry() above for why this needs two calls at decoration time
def call_embedding_api(text):
    global failures_left

    if failures_left > 0:
        failures_left -= 1
        raise ConnectionError("API timeout")

    return [0.1, 0.2, 0.3]

result = call_embedding_api("Hello world")
print(result)