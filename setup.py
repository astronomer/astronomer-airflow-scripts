# Copyright 2019 Astronomer Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import re

from setuptools import find_namespace_packages, setup


def fpath(*parts):
    return os.path.join(os.path.dirname(__file__), *parts)


def read(*parts):
    return open(fpath(*parts)).read()


def desc():
    return read('README.md')


# https://packaging.python.org/guides/single-sourcing-package-version/
def find_version(*paths):
    version_file = read(*paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='astronomer-airflow-scripts',
    version=find_version('version.py'),
    url='https://github.com/astronomer/airflow-migration-spinner',
    license='Apache2',
    author='astronomerio',
    author_email='humans@astronomer.io',
    description='',
    long_description=desc(),
    long_description_content_type="text/markdown",
    packages=find_namespace_packages(exclude='tests'),
    package_data={'': ['LICENSE']},
    entry_points={
        'console_scripts': [
            'airflow-migration-spinner=migration_spinner.command_line:main',
            'airflow-cleanup-pods=cleanup_pods.command_line:main',
        ]
    },
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
        'apache-airflow>=1.10.0',
    ],
    setup_requires=[
        'pytest-runner~=4.0',
    ],
    tests_require=[
        "pytest",
        "pytest-mock",
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
    ],
)
