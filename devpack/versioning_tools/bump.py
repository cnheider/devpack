from pathlib import Path


def bump_version_import(module_name: str, package: str = None) -> str:
    import importlib

    module = importlib.import_module(module_name, package)

    version = module.__version__

    base, _, minor = version.rpartition(".")
    return base + "." + str(int(minor) + 1)


def bump_version_regex(file_path: Path, search_regex_str: str) -> str:
    with open(file_path) as f:
        version = f.readlines()

    base, _, minor = version.rpartition(".")
    return base + "." + str(int(minor) + 1)


def bump_version_regex_inplace(file_path: Path, search_regex_str: str) -> None:
    with open(file_path) as f:
        version = f.readlines()

    base, _, minor = version.rpartition(".")
    new_version = base + "." + str(int(minor) + 1)


def bump_version_input() -> str:
    import sys

    version = sys.argv[1]
    base, _, minor = version.rpartition(".")
    return base + "." + str(int(minor) + 1)


if __name__ == "__main__":
    print(bump_version_import("warg"))
