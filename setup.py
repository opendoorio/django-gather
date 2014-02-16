import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-comlink',
    version='0.1',
    packages=['comlink'],
    include_package_data=True,
    license='Affero GPL',  
    description='community linkages via email and forum-like interfaces',
    long_description=README,
	url='https://github.com/opendoor/comlink',
    author='Jacob Sayles, Trevor F. Smith, Jessy Kate Schingler',
    author_email='jacob@officenomad.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
		'License :: OSI Approved :: Affero GPL', 
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
