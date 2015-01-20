# coding: utf-8

# coding: utf-8

import logging
import os, sys
import subprocess
from .util import check_output_noerr, PackageVersion

logger = logging.getLogger(__name__)

SRT_REPO = ":pserver:anonymous@srtcvs.fnal.gov:/srtcvs"
CVS_REPO = ":pserver:anonymous:anoncvs@minoscvs.fnal.gov:/cvs/minoscvs/rep1"
CVS_EXPORT_COMMAND = "export -kk -r {version} {packagename}"

class CVS(object):
  def __init__(self, repo=None):
    self.repo = repo or CVS_REPO

  def _build_args(self, *args):
    if len(args) == 1 and isinstance(args[0], list):
      args = args[0]
    else:
      args = list(args)
    return ["cvs", "-d", self.repo] + args

  def checkout_file(self, file):
    "Retrieve a file from the repository without comitting to disk"
    cvs_args = self._build_args("checkout", "-p", file)
    return check_output_noerr(cvs_args)

  def export(self, path, version=None):
    "Exports a CVS path to disk"
    export_args = CVS_EXPORT_COMMAND.format(packagename=path, version=version or "HEAD")
    cvs_args = self._build_args(export_args.split())
    logger.debug("  Exporting from CVS with: " + " ".join(cvs_args))
    subprocess.call(cvs_args)

  def rls(self, path):
    args = self._build_args("rls", path)
    return check_output_noerr(args)

def get_package_list(release):
  # cvs -d checkout -p setup/packages-R3.05 2> /dev/null
  repo = CVS()
  package_file = repo.checkout_file("setup/packages-{}".format(release)).decode()
  #cvs_args = build_cvs_args(["checkout", "-p", ])
  lines = [x.strip() for x in package_file.splitlines() if not x.strip().startswith("#")]
  sources = [PackageVersion(*x.split(":")) for x in lines if ":" in x]
  unspec = [x for x in lines if not ":" in x]
  sources.extend([PackageVersion(x, u"HEAD") for x in unspec])
  return sources

def get_repo(package):
  "Resolves the required repository address from the package name"
  if package == "SoftRelTools":
    return SRT_REPO
  return CVS_REPO

def retrieve_package_source(package, version):
  # Special: SoftRelTools is different
  repo = get_repo(package)
  cvs = CVS(repo=repo)
  cvs.export(package, version=version)

def get_release_sources(release, force=False, packages=None):
  if os.path.exists(release) and not force:
    logger.error ("Cannot export release while destination " + release + " already exists")
    sys.exit(1)
  elif not os.path.exists(release):
    os.mkdir(release)
  if not os.path.isdir(release):
    logger.error  ("ERROR: Release path exists, but is not a directory")
    sys.exit(2)
  os.chdir(release)

  logger.info ("Retrieving package list for release " + release)
  package_list = get_package_list(release)
  logger.info ("Found {} packages".format(len(package_list)))

  if packages:
    package_list = [x for x in package_list if x.name in packages]

  for package in package_list:
    logger.info ("Retrieving {}...".format(package.name))
    retrieve_package_source(package.name, package.version)  

def get_release_list():
  rlist = CVS().rls("setup/packages-*").decode()
  lines = rlist.splitlines() 
  output = [x[len("packages-"):] for x in lines if x.startswith("packages")]
  return output
