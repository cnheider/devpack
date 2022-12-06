#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 9/6/22
           """

__all__ = ["contains_shebang"]

from pathlib import Path


def contains_shebang(path: Path, *, verbose: bool = True) -> bool:
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
                if "#!" in line:
                    if verbose:
                        print(f"Found #! declaration at line {ln}: {line}")
                    return True
    return False


if __name__ == "__main__":
    print(contains_shebang(Path(__file__)))
