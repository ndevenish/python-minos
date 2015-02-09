#!/usr/bin/env python
# coding: utf-8

"""
Usage:
    CombineHelpers.py --near=NEARFILE --far=FARFILE --tau=TAUFILE
                      --nuflux=NUFLUXFILE --barflux=NUBARFLUXFILE
                      --allflux=ALLFLUXFILE
                      <output_file>
"""

import os
import subprocess
import logging
logger = logging.getLogger(__name__)

from docopt import docopt

base_script = "/minos/app/nickd/test/NuMuBar/macros/NickThesis/CombineMMHelpers.C"
# void CombineMMHelpers(string nearfile="",
#           string farfile="",
#           string newfile="",
#           string numufluxfile="",
#           string numubarfluxfile="",
#           string allccfluxfile="",
#           string taufile="")

if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)

  args = docopt(__doc__)
  print (args)
  # Validate all the files exist
  # for files in ("--near","--far","--tau","--nuflux","--barflux","--allflux"):
  #   assert os.path.isfile(args[files])

  argOrder = ["--near","--far","<output_file>","--nuflux","--barflux","--allflux","--tau"]
  root_args = ",".join('"{}"'.format(args[x]) for x in argOrder)
  root_command = "{}({})".format(base_script, root_args)
  logger.info("Running root with " + root_command)
  results = subprocess.call(["root","-b","-q",root_command])
  if results:
    logger.error("ROOT signalled failure with {}".format(results))
