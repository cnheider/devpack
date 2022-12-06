#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 8/30/22
           """

__all__ = ["recursive_remove_inits"]

from pathlib import Path
from typing import Callable, Iterable, Optional

from warg.os_utilities.filtering import negate, is_python_module


def recursive_remove_inits(
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

    init_file = path / init_name
    if init_file.exists():
        init_file.unlink()

    for child in path.iterdir():
        if child.is_dir():
            if exclusion_filter is None or not any(
                flt(child) for flt in exclusion_filter
            ):
                recursive_remove_inits(
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
            pass


if __name__ == "__main__":
    recursive_remove_inits("../exclude/samples")
