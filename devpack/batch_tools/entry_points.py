#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 9/6/22
           """

__all__ = []

from pathlib import Path
from typing import Mapping


def validate_entry_points(
    path: Path, entry_points: Mapping, *, verbose: bool = True
) -> bool:
    """

    :param verbose:
    :type verbose:
    :param path:
    :type path:
    :return:
    :rtype:
    """
    if path.is_dir():
        for k, v in entry_points.items():
            import_path, func_name = v.split(":")
            target = (path / import_path.replace(".", "/")).with_suffix(".py")
            with open(target) as f:
                for ln, line in enumerate(f.readlines()):
                    if (
                        f"def {func_name}" in line
                    ):  # TODO: Replace with loaded module check, this solution allow for match with substring and does not allow variying spaces between def and func_name
                        if verbose:
                            print(f"Found {func_name} declaration at line {ln}: {line}")
                        return True
    return False


if __name__ == "__main__":
    print(
        validate_entry_points(
            Path.cwd(),
            {"validate_entry_points_key": "entry_points:validate_entry_points"},
        )
    )
