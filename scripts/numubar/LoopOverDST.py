#!/usr/bin/env python
# coding: utf-8

"""Builds a DST summary .root file

Usage:
  LoopOverDST.py [-v] <input_file> <anaVersion> [-b SCHEME] <output_file> 

Options:
  -b SCHEME, --binning=SCHEME   The binning scheme to use [default: 4]
  -v, --verbose                 Debug output
"""

import logging
logger = logging.getLogger(__name__)

from docopt import docopt

from minos.ntupleutils import NuXMLConfig
from minos.numubar import NuBase, NuDSTAna

if __name__ == "__main__":
  args = docopt(__doc__)
  if args["--verbose"]:
    logging.basicConfig(level=logging.DEBUG)
  else:
    logging.basicConfig(level=logging.INFO)


  #print (args)
  #assert os.path.isfile(input_file)
  #assert os.path.isfile(xml_file)
  

  # Construct an XML file for the dst processing
  xml = NuXMLConfig()
  xml.LoadKeyValue("binningScheme", args["--binning"])
  xml.LoadKeyValue("anaVersion", args["<anaVersion>"])
  logger.debug("Setting up config; binning={}, ana={}".format(args["--binning"], args["<anaVersion>"]))

  logger.debug("Reading {}".format(args["<input_file>"]))
  NuBase.InputFileName(args["<input_file>"])
  NuBase.LoadTrees(False)
  # Create the analysis object
  ana = NuDSTAna()
  ana.OpenOutFile(args["<output_file>"])
  logger.debug("Doing MMRereco")
  ana.MMRereco("null", xml)
  ana.WriteOutHistos()
  ana.CloseOutFile()
  logger.info ("End of MakeSummary")
