#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os
import sys

import setuptools
from setuptools import setup, Extension
from setuptools.command.test import test as TestCommand

from distutils.sysconfig import get_config_var, get_python_inc

import versioneer


class PyTest(TestCommand):
    description = "Run test suite with pytest"

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        sys.exit(pytest.main(self.test_args))


version = versioneer.get_version()

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

setup_requirements = [
    "cython>=0.25.2",
    {% if cookiecutter.require_numpy == 'y' -%}
    "numpy>=1.11.3",
    {%- endif %}
]

install_requirements = [
    {% if cookiecutter.require_numpy == 'y' -%}
    "numpy>=1.11.3",
    {%- endif %}
    # TODO: put package install requirements here
]

test_requirements = [
    "pytest",
]

cmdclasses = dict()
cmdclasses.update(versioneer.get_cmdclass())
cmdclasses["test"] = PyTest

{%- set license_classifiers = {
    "MIT license": "License :: OSI Approved :: MIT License",
    "BSD license": "License :: OSI Approved :: BSD License",
    "ISC license": "License :: OSI Approved :: ISC License (ISCL)",
    "Apache Software License 2.0": "License :: OSI Approved :: Apache Software License",
    "GNU General Public License v3": "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
} %}

if not (({"develop", "test"} & set(sys.argv)) or
    any([v.startswith("build") for v in sys.argv]) or
    any([v.startswith("bdist") for v in sys.argv]) or
    any([v.startswith("install") for v in sys.argv])):
    setup_requirements = []
else:
    with open("src/version.pxi", "w") as f:
        f.writelines([
            "__version__ = " + "\"" + str(version) + "\""
        ])


try:
    i = sys.argv.index("test")
    sys.argv = sys.argv[:i] + ["build_ext", "--inplace"] + sys.argv[i:]
except ValueError:
    pass


include_dirs = [
    os.path.dirname(get_python_inc()),
    get_python_inc()
]
library_dirs = list(filter(
    lambda v: v is not None,
    [get_config_var("LIBDIR")]
))

headers = []
sources = glob.glob("src/*.pxd") + glob.glob("src/*.pyx")
libraries = []
define_macros = []
extra_compile_args = []
cython_directives = {}
cython_line_directives = {}


if "test" in sys.argv:
    cython_directives["binding"] = True
    cython_directives["embedsignature"] = True
    cython_directives["profile"] = True
    cython_directives["linetrace"] = True
    define_macros += [
        ("CYTHON_PROFILE", 1),
        ("CYTHON_TRACE", 1),
        ("CYTHON_TRACE_NOGIL", 1),
    ]


ext_modules = [
    Extension(
        "{{cookiecutter.project_import}}",
        sources=sources,
        include_dirs=include_dirs,
        library_dirs=library_dirs,
        libraries=libraries,
        define_macros=define_macros,
        extra_compile_args=extra_compile_args,
        language="c"
    )
]
for em in ext_modules:
    em.cython_directives = dict(cython_directives)
    em.cython_line_directives = dict(cython_line_directives)


setup(
    name="{{ cookiecutter.project_name }}",
    version=version,
    description="{{ cookiecutter.project_short_description }}",
    long_description=readme + "\n\n" + history,
    author="{{ cookiecutter.full_name.replace('\"', '\\\"') }}",
    author_email="{{ cookiecutter.email }}",
    url="https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_name }}",
    cmdclass=cmdclasses,
    packages=setuptools.find_packages(exclude=["tests*"]),
    include_package_data=True,
    setup_requires=setup_requirements,
    install_requires=install_requirements,
    headers=headers,
    ext_modules=ext_modules,
{%- if cookiecutter.open_source_license in license_classifiers %}
    license="{{ cookiecutter.open_source_license }}",
{%- endif %}
    zip_safe=False,
    keywords="{{ cookiecutter.project_name }}",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
{%- if cookiecutter.open_source_license in license_classifiers %}
        "{{ license_classifiers[cookiecutter.open_source_license] }}",
{%- endif %}
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    tests_require=test_requirements
)
