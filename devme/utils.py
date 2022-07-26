import importlib
import inspect
import pkgutil

from devme import framework
from devme.enums import FrameworkType
from devme.framework import Framework


def _discover_framework():
    ret = {}
    for m in pkgutil.iter_modules(framework.__path__):
        mod = importlib.import_module(f"{framework.__name__}.{m.name}")
        for name, member in inspect.getmembers(mod, inspect.isclass):
            if issubclass(member, Framework) and member is not Framework:
                ret[member.type] = member
    return ret


framework_map = _discover_framework()


def get_framework(type_: FrameworkType):
    return framework_map[type_]
