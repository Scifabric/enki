# -*- encoding: utf8 -*-
from setuptools import setup, find_packages

setup(
    name='enki',
    version='1.1.1',
    packages=find_packages(),
    install_requires=['pybossa-client>=1.1.1, <1.1.2', 'pandas'],
    # metadata for upload to PyPI
    author='SciFabric LTD',
    author_email='info@scifabric.com',
    description='A Python library to analyze PYBOSSA application results',
    long_description='''PyBossa is a crowdsourcing framework. This tiny library that allows you to analyze the results of a PYBOSSA aplication.''',
    license='AGPLv3',
    url='https://github.com/Scifabric/enki',
    download_url='https://github.com/Scifabric/enki/zipball/master',
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering'
    ],
    entry_points=''''''
)
