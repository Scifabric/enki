# -*- encoding: utf8 -*-
from setuptools import setup, find_packages

setup(
    name='enki',
    version='1.1.2',
    packages=find_packages(),
    install_requires=['pybossa-client>=2.0.1, <2.0.2', 'pandas'],
    # metadata for upload to PyPI
    author='Scifabric LTD',
    author_email='info@scifabric.com',
    description='''A Python library to analyze PYBOSSA project's results''',
    long_description='''PYBOSSA is a crowdsourcing, microtasking or citizen
    science framework. This tiny library allows you to analyze the results of a PYBOSSA project with PANDAS.''',
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
