# coding: utf-8

"""Handles Minossoft releases with CMake.

Usage:
  cmrt [options] bootstrap <folder>
  cmrt [options] release <release_name>
  cmrt [options] build [<folder>]
  cmrt [options] testrel <folder> [<package> [<package>...] ]
  cmrt [options] addpkg [--virtual | --here] <package> [<version>]
  cmrt [options] create-cmake <folder>
  cmrt [options] resolveproxy [--proxy=<proxydir>] <package> [<package>...]

Options:
  -l, --log             Compile into log files
  -v, --verbose         Be verbose with output.
  -r, --release=<TAG>   The release version tag to use. [default: development]
  --virtual             Add the package to build and records, but do not
                        attempt to check out or otherwise mess with the actual
                        package directory. Used if loading the actual package
                        source from an alternate location.
  --here                Do the action here e.g. don't look for the release and
                        don't tie into the CMake infrastructure

Commands:
  cmrt bootstrap <folder>
    Prepares a folder for a CMAKE-enabled base release of minossoft, including
    activation script and FindMinos.cmake sources.

  cmrt release <release_name>
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

  cmrt addpkg [--virtual] [--here] <package> [<version>]
    Adds a package to a test release, by checking it out from CVS (if --virtual
    is not specified) and adding the package to the relevant CMake
    infrastructure files.

  cmrt create-cmake <folder>
    Read a plain package folder and create the minos-cmake CMakeLists.txt
    files for the package.

  cmrt resolveproxy [--proxy=<proxydir>] <package> [<package>...] 
    Resoves all data .proxy files by softlinking them to a global proxy data
    store, set by the --proxy option, or the SITE_PROXY_CACHE environmental
    variable.
"""

from __future__ import division, print_function
import os
import glob

import logging
logger = logging.getLogger(__name__)

from docopt import docopt

from .cvs import retrieve_package_source, get_release_sources
from .cmakegen import write_package_cmakelist
from .makeparser import parse_makefile

class ArgumentError(Exception):
  pass

def main(args):
  args = docopt(__doc__)
  if args["--verbose"]:
    logging.basicConfig(level=logging.DEBUG)
  else:
    logging.basicConfig(level=logging.INFO)

  try:
    if args["addpkg"]:
      return addpkg(args)
    if args["create-cmake"]:
      return create_cmake(args)
    if args["resolveproxy"]:
      return resolveproxy(args)
    if args["release"]:
      return release(args)
  except ArgumentError as e:
    logger.error(e)
    return 1

def addpkg(arguments):
  assert arguments["--here"]
  assert arguments["<version>"]
  #assert arguments["<version>"].upper() == "HEAD"
  retrieve_package_source(arguments["<package>"][0], arguments["<version>"])

def create_cmake(arguments):
  folder = arguments["<folder>"]
  name = os.path.basename(folder[:-1] if folder.endswith("/") else folder)
  make = parse_makefile(os.path.join(folder, "GNUmakefile"), name)
  write_package_cmakelist(folder, make, {})
#def write_package_cmakelist(folder, makefile, liblookup):

def resolveproxy(arguments):
  #resolveproxy [--proxy=<proxydir>] [<package> [<package>...] ]
  # Work out the proxy directory
  proxydir = arguments["--proxy"] or os.environ.get("SITE_PROXY_CACHE",None)
  if not proxydir:
    raise ArgumentError("Could not resolve proxy directory. Pass in --proxy or set SITE_PROXY_CACHE")
  logger.info("Resolving proxy files via {}".format(proxydir))

  if not all(os.path.isdir(x) for x in arguments["<package>"]):
    raise ArgumentError("Could not resolve all listed packaged; " + str(x for x in arguments["<package>"] if not os.path.isdir(x)))

  for package in arguments["<package>"]:
    for filename in glob.glob(os.path.join(package, "data", "*.proxy")):
      dest = open(filename).read().strip()
      assert dest.startswith("minossoft/")
      dest = os.path.join(proxydir, dest[len("minossoft/"):])
      assert os.path.isfile(dest)
      source = filename[:-6]
      logger.info("Linking {} to {}".format(source, dest))
      os.symlink(dest, source)

def release(arguments):
  releasename = arguments["<release_name>"]
  get_release_sources(releasename)
