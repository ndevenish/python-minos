# coding: utf-8

"""
Usage:
  cmrt [options] bootstrap <folder>
  cmrt [options] release --release=<TAG> <folder>
  cmrt [options] build [<folder>]
  cmrt [options] testrel <folder> [<package> [<package>...] ]
  cmrt [options] addpkg [--virtual] <package>

Options:
  -l, --log             Compile into log files
  -v, --verbose         Be verbose with output.
  -r, --release=<TAG>   The release version tag to use. [default: development]
  --virtual             Add the package to build and records, but do not
                        attempt to check out or otherwise mess with the actual
                        package directory. Used if loading the actual package
                        source from an alternate location.

Commands:
  cmrt bootstrap <folder>
    Prepares a folder for a CMAKE-enabled base release of minossoft, including
    activation script and FindMinos.cmake sources.

  cmrt release --release=<TAG> <folder>
    Fetches all the source for a new base release. release_name should be the
    version desired, usually 'development', given no other preference. If the
    target folder has the bootstrap infrastructure in place, then the CMake
    transformations will be applied - otherwise, this will end up being a
    plain source directory.

  cmrt build [<folder>]
    Build a base release. If folder is not specified, then the current release
    is used, as specified by either the environment variables 
    SRT_PRIVATE_CONTEXT (for test releases) or SRT_PUBLIC_CONTEXT (for base
    releases)

  cmrt testrel <folder> [<package> [<package>...] ]
    Creates a test release, with the CMake infrastructure, activation script,
    and an optional list of packages to preload.

  cmrt addpkg [--virtual] <package> 
    Adds a package to a test release, by checking it out from CVS (if --virtual
    is not specified) and adding the package to the relevant CMake
    infrastructure files.
"""

from __future__ import division, print_function

from docopt import docopt

def main(args):
  args = docopt(__doc__)
  print (args)
  return 1