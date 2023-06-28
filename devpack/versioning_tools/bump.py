from enum import Enum
from pathlib import Path

from sorcery import assigned_names


class BumpOrderEnum(Enum):
    major, minor, patch = assigned_names()
    micro = patch
    epoch = major


def bump_version_import(
    module_name: str,
    package: str = None,
    order: BumpOrderEnum = BumpOrderEnum.patch,
    reset_lower_order: bool = True,
) -> str:
    import importlib

    module = importlib.import_module(module_name, package)

    version = module.__version__

    return version_bump(version, reset_lower_order=reset_lower_order)


def version_partition(version: str) -> str:
    dot_count = version.count(".")

    if dot_count == 1:
        major, minor = version.split(".")
        return int(major), int(minor)

    elif dot_count >= 2:
        major, minor, patch, *rest = version.split(".")

        return int(major), int(minor), int(patch), *rest

    return (version,)


def version_bump(
    version: str,
    order: BumpOrderEnum = BumpOrderEnum.patch,
    reset_lower_order: bool = True,
) -> str:
    # TODO: HANDLE weird alpha, beta, rc versioning e.g. 1.2a, 12.3.alpha, 1.2.3.4rc

    partitioned = version_partition(version)

    # TODO: USE reset_lower_order!

    if len(partitioned) == 1:
        return str(int(partitioned[0]) + 1)

    pre = post = ""

    if order == BumpOrderEnum.major:
        ordered, *post = partitioned
        post = ".".join([str(p) for p in post])

    elif order == BumpOrderEnum.minor:
        if len(partitioned) == 2:
            pre, ordered = partitioned
        else:
            pre, ordered, *post = partitioned
            post = ".".join([str(p) for p in post])
        pre = str(pre)

    elif order == BumpOrderEnum.patch:
        if len(partitioned) == 2:
            pre, ordered = partitioned
        else:
            major, minor, ordered, *post = partitioned
            pre = ".".join((str(major), str(minor)))
            post = ".".join([str(p) for p in post])
        pre = str(pre)

    if pre != "":
        pre = str(pre) + "."

    if post != "":
        if reset_lower_order:
            post = ".".join(["0" for p in post.split(".")])

        post = "." + str(post)

    return pre + str(int(ordered) + 1) + post


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

    def ujhasduhau():
        for e in BumpOrderEnum:
            print("__")
            print(version_bump("1", order=e))
            print(version_bump("1.2", order=e))
            print(version_bump("1.2.3", order=e))
            print(version_bump("1.2.3.4", order=e))
            print("_")
            print(version_bump("1.2.3.4", order=e, reset_lower_order=False))

    ujhasduhau()
