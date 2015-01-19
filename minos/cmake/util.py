# coding: utf-8

import os
import subprocess

from collections import namedtuple
from contextlib import contextmanager

def check_output_noerr(*args, **kwargs):
  "A convenient version of subprocess.check_output that discards STDERR"
  with open(os.devnull, "w") as fnull:
    if not "stdout" in kwargs:
      return subprocess.check_output(stderr=fnull, *args, **kwargs)
    else:
      return subprocess.check_output(*args, **kwargs)

@contextmanager
def chdir(path):
  "A context-aware directory changer"
  pwd = os.getcwd()
  os.chdir(path)
  yield
  os.chdir(pwd)

PackageVersion = namedtuple("PackageVersion", ["name", "version"])
