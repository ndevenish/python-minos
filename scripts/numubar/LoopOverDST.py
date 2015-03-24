#!/usr/bin/env python
# coding: utf-8

"""Builds a DST summary .root file

Usage:
  LoopOverDST.py [-v] <input_file> <anaVersion> [-b SCHEME]
                 [--ncana=NCANA]
                 [--nuosc=PARS | --nuosc=PARS --barosc=PARS]
                 <output_file>

Options:
  -b SCHEME, --binning=SCHEME   The binning scheme to use [default: 4]
  -v, --verbose                 Debug output
  --ncana=NCANA                 The NC anaVersion [default: CCA_NC]
  --nuosc=PARS                  Pair of oscillation parameters "dm2,sn2"
  --barosc=PARS                 Pair of antineutrino oscillation parameters,
                                "dm2bar,sn2bar". If this is not specified,
                                then CPT-conservation is assumed and the
                                nuosc value is used for both.
"""

from decimal import Decimal
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

  # Construct an XML file for the dst processing
  xml = NuXMLConfig()
  xml.LoadKeyValue("binningScheme", args["--binning"])
  xml.LoadKeyValue("anaVersion", args["<anaVersion>"])
  xml.LoadKeyValue("anaVersionNC", args["--ncana"])

  # Handle oscillation
  if args["--nuosc"]:
    dm2, sn2 = [str(Decimal(x)) for x in args["--nuosc"].split(",")]
    if args["--barosc"]:
      dm2bar, sn2bar = [str(Decimal(x)) for x in args["--barosc"].split(",")]
    else:
      dm2bar, sn2bar = dm2, sn2
    xml.LoadKeyValue("dm2nu", dm2)
    xml.LoadKeyValue("sn2nu", sn2)
    xml.LoadKeyValue("dm2bar", dm2bar)
    xml.LoadKeyValue("sn2bar", sn2bar)

    logger.info("Oscillating with dm2={} sn2={}".format(dm2, sn2))
    logger.info("             BAR dm2={} sn2={}".format(dm2bar, sn2bar))

  logger.info("Using anaVersion " + args["<anaVersion>"])
  logger.info("Using NC anaVersion " + args["--ncana"])
  logger.info("Using binning scheme {}".format(args["--binning"]))

  # MMRereco REQUIRES a setting here, via NuSystematic::ReadXML
  xml.LoadKeyValue("name", "Nominal")
  xml.LoadKeyValue("title", "Nominal")
  xml.LoadKeyValue("shift", "1.0")

  logger.info("Reading {}".format(args["<input_file>"]))
  NuBase.InputFileName(args["<input_file>"])
  NuBase.LoadTrees(False)
  # Create the analysis object
  ana = NuDSTAna()
  ana.OpenOutFile(args["<output_file>"])
  logger.debug("Doing MMRereco")
  ana.MMRereco("null", xml)
  ana.WriteOutHistos()
  ana.CloseOutFile()
  logger.info("End of MakeSummary")
