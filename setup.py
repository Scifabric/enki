# -*- encoding: utf8 -*-
from setuptools import setup, find_packages

setup(
    name='enki',
    version='0.0.2',
    packages=find_packages(),
    install_requires=['pybossa-client', 'pandas'],
    # metadata for upload to PyPI
    author='Daniel Lombraña González',
    author_email='teleyinex@gmail.com',
    description='A Python library to analyze PyBossa application results',
    long_description='''PyBossa is a crowdsourcing framework. This tiny library that allows you to analyze the results of a PyBossa aplication.''',
    license='AGPLv3',
    url='https://github.com/pybossa/enki',
    download_url='https://github.com/PyBossa/enki/zipball/master',
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points=''''''
)
