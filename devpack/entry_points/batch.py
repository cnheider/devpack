#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 8/18/22
           """

__all__ = []

import argparse
from pathlib import Path

from devpack.batch_tools.inits import recursive_remove_inits
from devpack.batch_tools.readmes import TouchModeEnum, recursive_add_readmes


def recursively_add_readmes_from_here():
    """
    Add readmes to all python modules in the current directory
    """
    parser = argparse.ArgumentParser(description="DevPack add readmes from here")
    parser.add_argument(
        "--path", "-p", type=Path, default=Path.cwd(), help="Path to add readmes to"
    )
    parser.add_argument(
        "--touch-mode",
        "-t",
        type=TouchModeEnum,
        default=TouchModeEnum.breadcrumb,
        help="Touch mode",
    )
    parser.add_argument(
        "--readme-name", "-r", type=str, default="README.md", help="Readme name"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Verbose output of touched files"
    )
    args = parser.parse_args()

    recursive_add_readmes(
        args.path,
        touch_mode=args.touch_mode,
        readme_name=args.readme_name,
        verbose=args.verbose,
    )


def recursively_remove_inits_from_here():
    """
    Add readmes to all python modules in the current directory
    """
    parser = argparse.ArgumentParser(description="DevPack remove inits from here")
    parser.add_argument(
        "--path", "-p", type=Path, default=Path.cwd(), help="Path to remove inits from"
    )

    parser.add_argument(
        "--init-name", "-r", type=str, default="__init__.py", help="init name"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Verbose output of removed files"
    )
    args = parser.parse_args()

    recursive_remove_inits(
        args.path,
        init_name=args.init_name,
        verbose=args.verbose,
    )


def recursively_check_typing():
    """
    Add readmes to all python modules in the current directory
    """
    parser = argparse.ArgumentParser(description="DevPack remove inits from here")
    parser.add_argument(
        "--path", "-p", type=Path, default=Path.cwd(), help="Path to remove inits from"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Verbose output of removed files"
    )
    args = parser.parse_args()

    recursive_remove_inits(
        args.path,
        init_name=args.init_name,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    # recursively_add_readmes_from_here()
    # recursively_remove_inits_from_here()
    recursively_check_typing()
