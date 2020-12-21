# Copyright 2020 Stein & Gabelgaard ApS
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name="click-odoo-sg",
    description="click-odoo scripts collection",
    long_description="\n",
    use_scm_version=True,
    packages=find_packages(),
    include_package_data=True,
    setup_requires=["setuptools-scm"],
    install_requires=[
        "click-odoo>=1.3.0",
        "importlib_resources ; python_version<'3.9'",
    ],
    license="LGPLv3+",
    author="Stein & Gabelgaard ApS",
    author_email="info@steingabelgaard.dk",
    url="http://www.steingabelgaard.dk",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: "
        "GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: Odoo",
    ],
    entry_points="""
        [console_scripts]
        click-odoo-pulltrans=click_odoo_sg.pulltrans:main
        """,
)