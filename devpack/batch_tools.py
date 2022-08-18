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
) -> None:
    """
    Add a readme to the root_path if it does not exist

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
        if touch_mode == TouchModeEnum.breadcrumb:
            assert root_path is not None
            readme_file.write_text(prefix + str(path.relative_to(root_path)))
        elif touch_mode == TouchModeEnum.empty:
            readme_file.write_text("")
        elif touch_mode == TouchModeEnum.parent_name:
            readme_file.write_text(prefix + str(readme_file.parent.name))
        else:
            raise ValueError(f"Unknown touch mode {touch_mode}")


def is_python_module(path: Path) -> bool:
    """
    Check if path is a python module
    """
    return path.is_file() and path.suffix == ".py"


def is_python_package(path: Path) -> bool:
    """
    Check if path is a python package
    """
    return path.is_dir() and (path / "__init__.py").exists()


def negate(f: Callable) -> Callable:
    """
    Negate a function
    """
    return lambda *args, **kwargs: not f(*args, **kwargs)


def recursive_add_readmes(
    path: Path,
    exclusion_filter: Optional[Iterable[Callable]] = (negate(is_python_package),),
    *,
    touch_mode: TouchModeEnum = TouchModeEnum.breadcrumb,
    readme_name: str = "README.md",
    root_path: Optional[Path] = None,
) -> None:
    """
    recursively add readmes to all children spanning from root_path

    """
    path = Path(path)
    if root_path is None:
        root_path = path.parent

    auto_add_readme(
        path, touch_mode=touch_mode, readme_name=readme_name, root_path=root_path
    )

    for child in path.iterdir():
        if exclusion_filter is None or not any(flt(child) for flt in exclusion_filter):
            if child.is_dir():
                recursive_add_readmes(
                    child,
                    exclusion_filter,
                    touch_mode=touch_mode,
                    readme_name=readme_name,
                    root_path=root_path,
                )
            elif child.is_file():
                pass


if __name__ == "__main__":
    recursive_add_readmes("exclude")
