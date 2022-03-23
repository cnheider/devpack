#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 02/03/2020
           """

import subprocess
import sys
from typing import Optional

__all__ = ["pip_install_development_package"]


def pip_install_development_package(
    package: str,
    from_index: str = "https://test.pypi.org/simple/",
    extra_index: Optional[str] = "https://pypi.org/simple/",
    upgrade: bool = True,
) -> None:
    """ """
    arguments = [
        "install",
        "--index-url",
        from_index,
    ]

    if extra_index:
        arguments += "--extra-index-url", extra_index

    if upgrade:
        arguments += ("-U",)

    arguments += (package,)

    # Is being deprecated!
    # from pip import main
    # main(arguments)

    subprocess.check_call([sys.executable, "-m", "pip", *arguments])


if __name__ == "__main__":
    pass
    # pip_install_development_package("devpack")
    # pip_install_development_package("draugr")
    # pip_install_development_package("munin")
