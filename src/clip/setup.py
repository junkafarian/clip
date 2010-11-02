from setuptools import setup, find_packages
import sys, os

version = '0.1'

requires = [
    'Fabric',
    ]

setup(name='clip',
      version=version,
      description="Deployment environment for buildout-based projects using git.",
      author='junkafarian',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
