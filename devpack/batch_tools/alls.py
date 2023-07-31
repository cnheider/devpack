#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

        TODO: IMPLEMENT, NOT DONE AT ALL!

           Created on 9/2/22
           """

__all__ = ["AutoAllsModeEnum", "auto_add_all", "is_init_file"]

from enum import Enum
from pathlib import Path
from typing import Iterable, Callable, Optional

from sorcery import assigned_names

from warg import is_python_package, negate, import_file


class AutoAllsModeEnum(Enum):
    """
    TODO: add more modes
    """

    add_vars, empty = assigned_names()


def auto_add_all(*, verbose: bool = True):
    """If __all__ is missing from file and conditions are met, auto-populate all"""
    pass


def is_library_file(path: Path, *, verbose: bool = True) -> bool:
    """
    Does not have variables and/or call in global scope or hidden behind a __main__

    TODO: BAD CHECK!!
    """
    if path.is_file():
        with open(path) as f:
            for ln, line in enumerate(f.readlines()):
                if "__main__" not in line:
                    if verbose:
                        print(f"Found .... at line {ln}: {line}")
                    return True
    return False


def is_runnable_file(path: Path, *, verbose: bool = True) -> bool:
    """
    Has variables and/or call in global scope or hidden behind a __main__
    """
    if path.is_file():
        with open(path) as f:
            for ln, line in enumerate(f.readlines()):
                if "__main__" in line:
                    if verbose:
                        print(f"Found main at line {ln}: {line}")
                    return True
    return False


def is_main_file(path: Path, *, verbose: bool = True) -> bool:
    """
    if file not supposed to be imported from anywhere, i.e. all code is hidden behind the common if __name__ == '__main__': clause
    """
    if path.is_file():
        with open(path) as f:
            for ln, line in enumerate(f.readlines()):
                if "__main__" in line:
                    if verbose:
                        print(f"Found main at line {ln}: {line}")
                    return True
    return False


def is_init_file(path: Path, *, verbose: bool = True) -> bool:
    """

    :param verbose:
    :type verbose:
    :param path:
    :type path:
    :return:
    :rtype:
    """
    if verbose:
        print(f"Found init file at {path}")
    return path.stem == "__init__"


def has_module_import():
    """
    'import <>'

    :return:
    :rtype:
    """
    ...


def has_from_module_import():
    """
    'from <> import <>'

    useful for finding name bindings of submodules

    :return:
    :rtype:
    """
    ...


def has_all_declaration(path: Path, *, verbose: bool = True) -> bool:
    """

    :param verbose:
    :type verbose:
    :param path:
    :type path:
    :return:
    :rtype:
    """
    if path.is_file():
        with open(path) as f:
            for ln, line in enumerate(f.readlines()):
                if "__all__" in line:
                    if verbose:
                        print(f"Found __all__ declaration at line {ln}: {line}")
                    return True
    return False


def has_non_empty_all(path: Path, *, verbose: bool = True) -> bool:
    """

    :param path:
    :type path:
    :param verbose:
    :type verbose:
    :return:
    :rtype:
    """

    if False:
        assert has_all_declaration(path, verbose=verbose)

    _all = import_file(path, from_list={"__all__"}).__all__

    if _all:
        if verbose:
            print(f"Found non empty __all__ {_all} at {path}")
        return True
    return False


def has_empty_all(path: Path, *, verbose: bool = True) -> bool:
    """
    negates has_non_empty_all

    :param path:
    :type path:
    :param verbose:
    :type verbose:
    :return:
    :rtype:
    """
    return not has_non_empty_all(path, verbose=verbose)


def has_privates(path: Path, *, verbose: bool = True) -> None:
    """
    By default, Python will export all names that do not start with an _ when imported with import *.


    :return:
    :rtype:
    """
    return False


def exports_privates(path: Path, *, verbose: bool = True) -> None:
    """
    By default, Python will export all names that do not start with an _ when imported with import *.

    Test if there any "privates" declared in __all__


    :return:
    :rtype:
    """
    return False


def has_star_import(path: Path, *, verbose: bool = True) -> bool:
    """
    Also called wild/wildcard imports

    :param verbose:
    :type verbose:
    :param path:
    :type path:
    :return:
    :rtype:
    """
    if path.is_file():
        with open(path) as f:
            for ln, line in enumerate(f.readlines()):
                if "import *" in line:
                    if verbose:
                        print(f"Found star import at line {ln}: {line}")
                    return True
    return False


def check_alls(path: Path, *, verbose: bool = True) -> None:
    """

    :param path:
    :type path:
    :param verbose:
    :type verbose:
    """
    if is_init_file(path, verbose=verbose):
        if has_star_import(path, verbose=verbose):
            if has_all_declaration(path, verbose=verbose):
                if verbose:
                    print("WARNING star import with __all__ declaration")
        if has_all_declaration(path, verbose=verbose):
            if has_non_empty_all(path, verbose=verbose):
                if verbose:
                    print("WARNING __init__ with empty __all__ declaration")
    if is_main_file(path, verbose=verbose):
        if has_all_declaration(path, verbose=verbose):
            if has_non_empty_all(path, verbose=verbose):
                if verbose:
                    print("WARNING main file import with non empty __all__ declaration")
    if is_library_file(path, verbose=verbose):
        if has_all_declaration(path, verbose=verbose):
            if not has_non_empty_all(path, verbose=verbose):
                if verbose:
                    print("WARNING library file with empty __all__ declaration")


def has_multiple_alls() -> bool:
    ...


def recursive_check_alls(
    path: Path,
    exclusion_filter: Optional[Iterable[Callable]] = (negate(is_python_package),),
    *,
    alls_mode: AutoAllsModeEnum = AutoAllsModeEnum.empty,
    verbose: bool = True,
) -> None:
    """

    :param path:
    :type path:
    :param exclusion_filter:
    :type exclusion_filter:
    :param alls_mode:
    :type alls_mode:
    :param verbose:
    :type verbose:
    """
    path = Path(path)

    for child in path.iterdir():
        if child.is_dir():
            if exclusion_filter is None or not any(
                flt(child) for flt in exclusion_filter
            ):
                recursive_check_alls(
                    child,
                    exclusion_filter,
                    verbose=verbose,
                )
            else:
                if verbose:
                    print(
                        f"{child} was excluded, filters:\n{[(flt.__name__, flt(child)) for flt in exclusion_filter]}"
                    )
        elif child.is_file():
            check_alls(path, verbose=verbose)
            if alls_mode == AutoAllsModeEnum.empty:
                pass


def does_not_have_all_but_has_import():
    """
    Should not be allowed this allows binding of external dependencies
    :return:
    :rtype:
    """
    ...


def does_not_have_all_but_has_from_import():
    """
    Should not be allowed this allows binding of external dependencies

    :return:
    :rtype:
    """
    ...


def does_not_have_all_and_has_from_import_from_submodule():
    """
    Should be allowed this allows binding of internal dependencies

    :return:
    :rtype:
    """
    ...


if __name__ == "__main__":
    # recursive_check_alls("../exclude")
    has_non_empty_all(Path.cwd() / "__init__.py", verbose=True)
    print("---")
    has_non_empty_all(Path.cwd(), verbose=True)
    print("----")
    has_non_empty_all(Path(__file__), verbose=True)

    # auto_add_all()
