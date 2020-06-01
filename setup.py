import sys

from setuptools import setup, find_packages

MIN_PYTHON_VERSION = (3, 7)

if sys.version_info[:2] != MIN_PYTHON_VERSION:
    raise RuntimeError("Требуется версия Python = {}.{}".format(MIN_PYTHON_VERSION[0], MIN_PYTHON_VERSION[1]))

import oidv6

REQUIRED_PACKAGES = [
    'requests >= 2.23.0',
    'numpy >= 1.18.4',
    'pandas >= 1.0.4',
    'progressbar2 >= 3.51.3',
    'opencv-contrib-python >= 4.2.0.34',
    'awscli >= 1.18.69'
]

CLASSIFIERS = """\
Development Status :: 5 - Production/Stable
Natural Language :: Russian
Natural Language :: English
Intended Audience :: Developers
Intended Audience :: Education
Intended Audience :: Science/Research
License :: OSI Approved :: MIT License
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3 :: Only
Programming Language :: Python :: Implementation :: CPython
Topic :: Scientific/Engineering
Topic :: Scientific/Engineering :: Mathematics
Topic :: Software Development
Topic :: Software Development :: Libraries
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: MacOS :: MacOS X
Operating System :: Microsoft :: Windows
Operating System :: POSIX :: Linux
"""

with open('README.md', 'r') as fh:
    long_description = fh.read()

    setup(
        name = oidv6.__name__,
        packages = find_packages(),
        license = oidv6.__license__,
        version = oidv6.__version__,
        author = oidv6.__author__,
        author_email = oidv6.__email__,
        maintainer = oidv6.__maintainer__,
        maintainer_email = oidv6.__maintainer_email__,
        url = oidv6.__uri__,
        description = oidv6.__summary__,
        long_description = long_description,
        long_description_content_type = 'text/markdown',
        install_requires=REQUIRED_PACKAGES,
        keywords = ['oidv6', 'Open Images Dataset'],
        include_package_data = True,
        classifiers = [_f for _f in CLASSIFIERS.split('\n') if _f],
        python_requires = '>=3.7',
        entry_points = {
            'console_scripts': [
                'oidv6 = oidv6.samples.run:main',
            ],
        },
    )
