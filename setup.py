from distutils.core import setup
import setuptools

setup(name="minos",
      version='0.1',
      author="Nicholas Devenish",
      author_email="ndevenish@gmail.com",
      packages=['minos'],
#      scripts=['bin/minos-cmake'],
#      package_data={'minos_cmake': ['data/*.txt', 'data/*.cmake']},
      requires=["docopt"],
     )
