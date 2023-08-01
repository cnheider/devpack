#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

        TODO: IMPLEMENT

           Created on 9/5/22
           """

__all__ = ["recursive_check_for_privates"]

from pathlib import Path
from typing import Optional, Callable, Iterable

from draugr.os_utilities.linux_utilities.user_utilities import get_username

from warg.os_utilities.filtering import is_python_module, negate


def contains_specific_home_reference(path: Path, *, verbose: bool = True) -> bool:
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
                if "/home" in line:
                    if verbose:
                        print(f"Found home specific reference at line {ln}: {line}")
                    return True
    return False


def contains_password_like(path: Path, *, verbose: bool = True) -> bool:
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
                if "pass" in line or "secret" in line:
                    if verbose:
                        print(f"Found password like reference at at line {ln}: {line}")
                    return True
    return False


def contains_username_like(path: Path, *, verbose: bool = True) -> bool:
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
                if "user" in line:
                    if verbose:
                        print(f"Found username like reference at line {ln}: {line}")
                    return True
    return False


def contains_author_name(path: Path, *, verbose: bool = True) -> bool:
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
                if get_username() in line:
                    if verbose:
                        print(f"Found author name at line {ln}: {line}")
                    return True
    return False


def recursive_check_for_privates(
    path: Path,
    exclusion_filter: Optional[Iterable[Callable]] = (negate(is_python_module),),
    *,
    init_name: str = "__init__.py",
    verbose: bool = True,
):
    """

    :param path:
    :type path:
    :param exclusion_filter:
    :type exclusion_filter:
    :param init_name:
    :type init_name:
    :param verbose:
    :type verbose:
    """
    path = Path(path)

    for child in path.iterdir():
        if child.is_dir():
            if exclusion_filter is None or not any(
                flt(child) for flt in exclusion_filter
            ):
                recursive_check_for_privates(
                    child,
                    exclusion_filter,
                    init_name=init_name,
                    verbose=verbose,
                )
            else:
                if verbose:
                    print(
                        f"{child} was excluded, filters:\n{[(flt.__name__, flt(child)) for flt in exclusion_filter]}"
                    )
        elif child.is_file():
            if (
                contains_author_name(child, verbose=verbose)
                or contains_username_like(child, verbose=verbose)
                or contains_password_like(child, verbose=verbose)
                or contains_specific_home_reference(child, verbose=verbose)
            ):
                print(child)


if __name__ == "__main__":
    recursive_check_for_privates("../exclude/samples")
