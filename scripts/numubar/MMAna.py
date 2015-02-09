#!/usr/bin/env python
# coding: utf-8

"""Builds a Normalised Ana file

Usage:
  MMAna.py <input_file> <output_file>
"""

import logging
logger = logging.getLogger(__name__)

from docopt import docopt

#from minos.ntupleutils import NuXMLConfig
from minos.numubar import NuBase, NuDSTAna

if __name__ == "__main__":
  args = docopt(__doc__)
  logging.basicConfig(level=logging.DEBUG)
  
  # Set up the framework
  logger.info("Reading {}".format(args["<input_file>"]))
  NuBase.InputFileName(args["<input_file>"])
  NuBase.LoadTrees(False)

  # Create the analysis object
  ana = NuDSTAna()
  ana.OpenOutFile(args["<output_file>"])
  logger.debug("Doing MMAna")
  ana.MMAna("null")
  ana.WriteOutHistos()
  ana.CloseOutFile()
  logger.info ("End of MMAna script")
