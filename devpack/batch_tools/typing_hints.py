#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 9/6/22
           """

__all__ = ["is_missing_typing_hints"]

import subprocess
from pathlib import Path
from typing import Optional, Iterable, Callable, Sequence


def is_missing_typing_hints(
    path: Path,
    *,
    verbose: bool = True,
    flags: Optional[Sequence] = (
        "--disallow-untyped-calls ",
        "--disallow-untyped-defs ",
        "--disallow-incomplete-defs ",
        "--strict-optional",
        "--strict",
    ),
) -> bool:
    """

    :param verbose:
    :type verbose:
    :param path:
    :type path:
    :return:
    :rtype:
    """
    a = subprocess.getoutput(f'mypy {" ".join(flags)} {str(path)}')
    if verbose:
        print(a)
    if "Success:" not in a:
        return True
    return False


def is_missing_typing_hints_traverse(
    path: Path,
    exclusion_filter: Optional[Iterable[Callable]] = None,
    *,
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
                is_missing_typing_hints_traverse(
                    child, exclusion_filter=exclusion_filter, verbose=verbose
                )
            else:
                if verbose:
                    print(
                        f"{child} was excluded, filters:\n{[(flt.__name__, flt(child)) for flt in exclusion_filter]}"
                    )
        elif child.is_file():
            if is_missing_typing_hints(
                child,
                verbose=verbose,
            ):
                break


if __name__ == "__main__":
    print(is_missing_typing_hints(Path(__file__).parent))
