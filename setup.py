from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='jgauth',
      version=version,
      description="Auth library for Pylons and such.",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='auth user pylons',
      author='Jonathan Gardner',
      author_email='jgardner@jonathangardner.net',
      url='http://tech.jonathangardner.net/wiki/Jgauth',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
          'sqlalchemy',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
