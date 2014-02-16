import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-gather',
    version='0.1',
    packages=['gather'],
    include_package_data=True,
    license='Affero GPL',  
    description='community run and community managed events',
    long_description=README,
	url='https://github.com/opendoor/django-gather',
    author='Jessy Kate Schingler',
    author_email='jessy@opendoor.io',
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
