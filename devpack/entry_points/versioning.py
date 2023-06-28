import argparse
from pathlib import Path


def bump():
    """
    bumps python module python version in the current directory
    """
    parser = argparse.ArgumentParser(description="DevPack bump version of this module")
    parser.add_argument(
        "--path", "-p", type=Path, default=Path.cwd(), help="Path to python module"
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose output of bump")
    args = parser.parse_args()

    # TODO: #version_bump(        args.path,        touch_mode=args.touch_mode,        readme_name=args.readme_name,        verbose=args.verbose,    )
