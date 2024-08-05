import time
from .logger import Logger
from chemistryIO.config_handler import config_handler
from functools import wraps

def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not config_handler.print_function_time:
            return func(*args, **kwargs)
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        Logger.debug(f"Function '{func.__name__}' took {duration:.4f} seconds to complete.")
        return result
    return wrapper

def species_involved_decorator(func):
    def wrapper(*args, **kwargs):
        if not config_handler.print_species_involved:
            return func(*args, **kwargs)
        self = args[0]
        species = args[1]
        species_names = [sp.name for sp in species]
        Logger.debug(f"Function '{func.__name__}' species involved: {species_names}")
        return func(*args, **kwargs)
    return wrapper


