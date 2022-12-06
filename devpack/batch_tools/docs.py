#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 9/6/22
           """

__all__ = ["contains_doc"]

from pathlib import Path


def contains_doc(path: Path, *, verbose: bool = True) -> bool:
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
                if "__doc__" in line:
                    if verbose:
                        print(f"Found __doc__ declaration at line {ln}: {line}")
                    return True
    return False


if __name__ == "__main__":
    print(contains_doc(Path(__file__)))
