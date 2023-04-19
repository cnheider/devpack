#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 8/18/22
           """

__all__ = ["auto_add_readme", "recursive_add_readmes", "TouchModeEnum"]

from enum import Enum
from pathlib import Path
from typing import Callable, Iterable, Optional

from sorcery import assigned_names

from warg.os_utilities.filtering import negate, is_python_package


class TouchModeEnum(Enum):
    """
    The touch mode enum

    """

    breadcrumb, empty, parent_name = assigned_names()


def auto_add_readme(
    path: Path,
    *,
    touch_mode: TouchModeEnum = TouchModeEnum.breadcrumb,
    readme_name: str = "README.md",
    root_path: Optional[Path] = Path.cwd(),
    prefix="# ",
    verbose: bool = True,
) -> None:
    """
    Add a readme to the root_path if it does not exist

    :param verbose:
    :type verbose:
    :param path:
    :param touch_mode:
    :param readme_name:
    :param root_path:
    :param prefix:
    :return:

    """
    path = Path(path)
    readme_file = path / readme_name
    if not readme_file.exists():
        readme_file.touch()
        if verbose:
            print(f"Created {readme_file}")
        if touch_mode == TouchModeEnum.breadcrumb:
            assert root_path is not None
            readme_file.write_text(prefix + str(path.relative_to(root_path)))
        elif touch_mode == TouchModeEnum.empty:
            readme_file.write_text("")
        elif touch_mode == TouchModeEnum.parent_name:
            readme_file.write_text(prefix + str(readme_file.parent.name))
        else:
            raise ValueError(f"Unknown touch mode {touch_mode}")
    else:
        if verbose:
            print(f"{readme_name} already exists at {path}")


def recursive_add_readmes(
    path: Path,
    exclusion_filter: Optional[Iterable[Callable]] = (negate(is_python_package),),
    *,
    touch_mode: TouchModeEnum = TouchModeEnum.breadcrumb,
    readme_name: str = "README.md",
    root_path: Optional[Path] = None,
    verbose: bool = True,
) -> None:
    """
    recursively add readmes to all children spanning from root_path

    """
    path = Path(path)
    if root_path is None:
        root_path = path.parent

    auto_add_readme(
        path,
        touch_mode=touch_mode,
        readme_name=readme_name,
        root_path=root_path,
        verbose=verbose,
    )

    for child in path.iterdir():
        if child.is_dir():
            if exclusion_filter is None or not any(
                flt(child) for flt in exclusion_filter
            ):
                recursive_add_readmes(
                    child,
                    exclusion_filter,
                    touch_mode=touch_mode,
                    readme_name=readme_name,
                    root_path=root_path,
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
    recursive_add_readmes("../exclude")
