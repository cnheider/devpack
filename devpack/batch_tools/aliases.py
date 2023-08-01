#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

        TODO: IMPLEMENT

           Created on 9/2/22
           """

__all__ = ["recursive_detect_import_aliasing"]

from pathlib import Path
from typing import Iterable, Callable, Optional, Sequence, Mapping, List

from warg.os_utilities.filtering import negate, is_python_package


def has_import_aliases(path: Path, *, verbose: bool = False) -> bool:
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
            for ln, l in enumerate(f.readlines()):
                if "import" in l and "as" in l:
                    if verbose:
                        print(f"Found alias at line {ln}: {l}")
                    return True
    return False


def recursive_detect_import_aliasing(
    path: Path,
    file_extensions: Sequence[str] = (".py", ".txt", ".yaml"),
    *,
    exclusion_filter: Optional[Iterable[Callable]] = (negate(is_python_package),),
    verbose: bool = True,
) -> None:
    """we do not like them!"""
    path = Path(path)
    file_extensions = [f".{f.lstrip('.')}" for f in file_extensions]

    for child in path.iterdir():
        if child.is_dir():
            if exclusion_filter is None or not any(
                flt(child) for flt in exclusion_filter
            ):
                recursive_detect_import_aliasing(
                    child,
                    file_extensions=file_extensions,
                    exclusion_filter=exclusion_filter,
                    verbose=verbose,
                )
            else:
                if verbose:
                    print(
                        f"{child} was excluded, filters:\n{[(flt.__name__, flt(child)) for flt in exclusion_filter]}"
                    )
        elif child.is_file():
            if child.suffix in file_extensions:
                if has_import_aliases(child, verbose=verbose):
                    print(child)


COMMON_ALIAS_REPLACEMENTS = {
    "plt.": "pyplot.",
    "import matplotlib.pyplot as plt": "from matplotlib import pyplot",
    "np.": "numpy.",
    "import numpy as np": "import numpy",
}


def auto_replace_aliases(
    path: Path,
    replacement_mapping: Mapping = COMMON_ALIAS_REPLACEMENTS,
    *,
    verbose: bool = False,
) -> List[str]:
    """
    replaces plt. with pyplot. and changes import to from matplotlib import pyplot. for numpy numpy. becomes numpy. and so on
    """
    path = Path(path)

    working_copy = []

    if path.is_file():
        with open(path) as f:
            for ln, line in enumerate(f.readlines()):
                line_copy = line
                for k, v in COMMON_ALIAS_REPLACEMENTS.items():
                    if k in line:
                        if verbose:
                            print(f"Found {k} at line {ln}: {line}")
                        line_copy = line_copy.replace(k, v)
                if verbose:
                    print(f"{line} -> {line_copy}")
                working_copy.append(line_copy)
    return working_copy


if __name__ == "__main__":
    recursive_detect_import_aliasing(Path(__file__).parent.parent / "exclude")

    import numpy as np  # for demonstration
    import matplotlib.pyplot as plt

    print(plt.__doc__[0])
    print(np.__version__)

    print(auto_replace_aliases(Path(__file__)))
