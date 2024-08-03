import pkgutil
import inspect
import importlib

# Walk through the packages in the current directory (__path__)
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    module = importlib.import_module(f"{__name__}.{module_name}")
    
    # Import all functions from the module
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj) and obj.__module__ == module.__name__:
            globals()[name] = obj

# Create __all__ to contain only the function names
__all__ = [name for name, obj in globals().items() if inspect.isfunction(obj) and obj.__module__.startswith(__name__)]

# Clean up the imported modules
del pkgutil, inspect, importlib
