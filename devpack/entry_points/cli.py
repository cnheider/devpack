#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christian Heider Nielsen"
__doc__ = r"""
           Entry points for package development.
"""

import argparse

from devpack.development import pip_install_development_package
from devpack.development import pip_uninstall_package


def install_develop():
    """For programmatically installing a package as a development install"""
    parser = argparse.ArgumentParser(description="DevPack Develop Installation")
    parser.add_argument(
        "PACKAGE_NAME", metavar="Name", type=str, help="Package name to install"
    )
    """
parser.add_argument(
"--SITE",
"-s",
type=bool,
default=False,
metavar="SITE",
help="Open user or site dirs (default: User)",
)
"""
    args = parser.parse_args()

    pip_install_development_package(args.PACKAGE_NAME)


def uninstall():
    """For programmatically uninstalling a package"""
    parser = argparse.ArgumentParser(description="DevPack Uninstall")
    parser.add_argument(
        "PACKAGE_NAME", metavar="Name", type=str, help="Package name to uninstall"
    )
    args = parser.parse_args()

    pip_uninstall_package(args.PACKAGE_NAME)


if __name__ == "__main__":
    install_develop()
