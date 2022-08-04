import importlib
import inspect
import pkgutil
from typing import Type

from devme import framework, git
from devme.enums import FrameworkType, GitType
from devme.framework import Framework
from devme.git import Git


def _discover_framework():
    ret = {}
    for m in pkgutil.iter_modules(framework.__path__):
        mod = importlib.import_module(f"{framework.__name__}.{m.name}")
        for name, member in inspect.getmembers(mod, inspect.isclass):
            if issubclass(member, Framework) and member is not Framework:
                ret[member.type] = member
    return ret


framework_map = _discover_framework()


def get_framework(type_: FrameworkType) -> Type[Framework]:
    return framework_map[type_]


def _discover_git():
    ret = {}
    for m in pkgutil.iter_modules(git.__path__):
        mod = importlib.import_module(f"{git.__name__}.{m.name}")
        for name, member in inspect.getmembers(mod, inspect.isclass):
            if issubclass(member, Git) and member is not Git:
                ret[member.type] = member
    return ret


git_map = _discover_git()


def get_git(type_: GitType) -> Type[Git]:
    return git_map[type_]


def get_owner_repo_from_url(url: str):
    items = url.split("/")
    repo = items[-1].split(".")[-2]
    owner = items[-2]
    return owner, repo
