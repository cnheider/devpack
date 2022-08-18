#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List, Union


def python_version_check(major=3, minor=6):
    """
    Check if the python version is equal to or greater than the specified version."""
    import sys

    assert sys.version_info.major == major and sys.version_info.minor >= minor, (
        f"This project is utilises language features only present Python {major}.{minor} and greater. "
        f"You are running {sys.version_info}."
    )


python_version_check()

import pathlib
import re

from setuptools import find_packages, setup

with open(
    pathlib.Path(__file__).parent / "devpack" / "__init__.py", "r"
) as project_init_file:
    content = project_init_file.read()
    # get version string from module
    version = re.search(r"__version__ = ['\"]([^'\"]*)['\"]", content, re.M).group(1)

    project_name = re.search(r"__project__ = ['\"]([^'\"]*)['\"]", content, re.M).group(
        1
    )
    author = re.search(r"__author__ = ['\"]([^'\"]*)['\"]", content, re.M).group(
        1
    )  # get version string from module
__author__ = author


class DevPackPackage:
    """
    A class to represent a devpack package
    """

    @property
    def test_dependencies(self) -> list:
        """
        The test dependencies
        """
        path = pathlib.Path(__file__).parent
        requirements_tests = []
        with open(path / "requirements_tests.txt") as f:
            requirements = f.readlines()

            for requirement in requirements:
                requirements_tests.append(requirement.strip())

        return requirements_tests

    @property
    def setup_dependencies(self) -> list:
        """
        Get the setup dependencies
        """
        path = pathlib.Path(__file__).parent
        requirements_setup = []
        with open(path / "requirements_setup.txt") as f:
            requirements = f.readlines()

            for requirement in requirements:
                requirements_setup.append(requirement.strip())

        return requirements_setup

    @property
    def package_name(self) -> str:
        """
        The name of the package
        """
        return project_name

    @property
    def url(self) -> str:
        """
        A url to the project's homepage
        """
        return "https://github.com/pything/devpack"

    @property
    def download_url(self) -> str:
        """
        A URL to download the package from
        """
        return f"{self.url}/releases"

    @property
    def readme_type(self) -> str:
        """
        The type of readme to use
        """
        return "text/markdown"

    @property
    def packages(self) -> List[Union[bytes, str]]:
        """
        Return a list of packages to include in the distribution
        """
        return find_packages(
            exclude=[
                # 'Path/To/Exclude'
            ]
        )

    @property
    def author_name(self) -> str:
        """
        A
        """
        return author

    @property
    def author_email(self) -> str:
        """
        Author email
        """
        return "christian.heider@alexandra.dk"

    @property
    def maintainer_name(self) -> str:
        """
        A name of the maintainer of the project
        """
        return self.author_name

    @property
    def maintainer_email(self) -> str:
        """
        A property to return the maintainer email
        """
        return self.author_email

    @property
    def package_data(self) -> dict:
        """
        Package data
        """
        emds = [str(p) for p in pathlib.Path(__file__).parent.rglob(".md")]
        return {self.package_name: [*emds]}

    @property
    def entry_points(self) -> dict:
        """
        Entry points for the devpack package

        """
        return {
            "console_scripts": [
                # "name_of_executable = module.with:function_to_execute"
                "devpack_install = devpack.entry_points.cli:install_develop",
                "devpack_uninstall = devpack.entry_points.cli:uninstall",
                "devpack_add_readmes = devpack.entry_points.batch:recursively_add_readmes_from_here",
            ]
        }

    @property
    def extras(self) -> dict:
        """
        Extra requirements
        """
        path = pathlib.Path(__file__).parent
        requirements_xx = []
        with open(path / "requirements_dev.txt") as f:
            requirements = f.readlines()

            for requirement in requirements:
                requirements_xx.append(requirement.strip())

        these_extras = {
            # 'ExtraGroupName':['package-name; platform_system == "System(Linux,Windows)"'
            # "xx": requirements_xx
        }

        all_dependencies = []

        for group_name in these_extras:
            all_dependencies += these_extras[group_name]
        these_extras["all"] = all_dependencies

        return these_extras

    @property
    def requirements(self) -> list:
        """
        Requirements for the package
        """
        requirements_out = []
        with open("requirements.txt") as f:
            requirements = f.readlines()

            for requirement in requirements:
                requirements_out.append(requirement.strip())

        return requirements_out

    @property
    def description(self) -> str:
        """
        A short description of the project
        """
        return "DevPack is a package for managing your dev environment"

    @property
    def readme(self) -> str:
        """
        The readme for the project
        """
        with open("README.md") as f:
            return f.read()

    @property
    def keyword(self) -> str:
        """
        A list of keywords that describe the package
        """
        with open("KEYWORDS.md") as f:
            return f.read()

    @property
    def license(self) -> str:
        """
        The license of the project
        """
        return "Apache License, Version 2.0"

    @property
    def classifiers(self) -> List[str]:
        """
        A list of classifiers
        """
        return [
            "Development Status :: 4 - Beta",
            "Environment :: Console",
            "Intended Audience :: End Users/Desktop",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Natural Language :: English",
            # 'Topic :: Scientific/Engineering :: Artificial Intelligence'
            # 'Topic :: Software Development :: Bug Tracking',
        ]

    @property
    def version(self) -> str:
        """
        The version of the package
        """
        return version


if __name__ == "__main__":
    pkg = DevPackPackage()

    setup(
        name=pkg.package_name,
        version=pkg.version,
        packages=pkg.packages,
        package_data=pkg.package_data,
        author=pkg.author_name,
        author_email=pkg.author_email,
        maintainer=pkg.maintainer_name,
        maintainer_email=pkg.maintainer_email,
        description=pkg.description,
        license=pkg.license,
        keywords=pkg.keyword,
        url=pkg.url,
        download_url=pkg.download_url,
        install_requires=pkg.requirements,
        extras_require=pkg.extras,
        setup_requires=pkg.setup_dependencies,
        entry_points=pkg.entry_points,
        classifiers=pkg.classifiers,
        long_description_content_type=pkg.readme_type,
        long_description=pkg.readme,
        tests_require=pkg.test_dependencies,
        include_package_data=True,
        python_requires=">=3.6",
    )
