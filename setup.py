from distutils.core import setup
import setuptools

setup(name="minos",
      version='0.1',
      author="Nicholas Devenish",
      author_email="ndevenish@gmail.com",
      packages=['minos'],
      scripts=['bin/cmrt'],
      package_data={'minos': ['cmake/data/*.cmake', 'cmake/data/*.txt']},
      requires=["docopt", "rootpy", "numpy", "matplotlib", "enum34", "scipy"],
     )
