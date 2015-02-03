#!/usr/bin/env python
# coding: utf-8

"""
Usage:
    MakeMMFluxHelpers.py [-v] (all | nu | nubar) <run_number> [-o <output_filename>] [-a <anaversion>] <flux_files>

Options:
  -o <output_filename>    The output filename to use
  -a <anaversion>         The Analysis version to use. Defaults to BravoTwo/RHC0325STD
  -v                      Verbose (debugging) output
"""

import logging
logger = logging.getLogger(__name__)

from docopt import docopt
import minos.ntupleutils

from ROOT import BeamType, vector

from datatool import Datatool

if __name__ == "__main__":
  args = docopt(__doc__)
  logging.basicConfig(level='DEBUG' if args["-v"] else "INFO")
  logging.getLogger("datatool").setLevel("INFO")

  # Sort out analysis version
  if args["-a"]:
    anaVersion = args["-a"]
  else:
    anaVersion = "BravoTwo" if args["<run_number>"] in ("1","2","3") else "RHC0325STD"
  logging.debug("Using analysis version " + anaVersion)

  # Construct an XML file for the flux helper
  xml = minos.ntupleutils.NuXMLConfig()
  xml.LoadKeyValue("binningScheme", "4")
  xml.LoadKeyValue("anaVersion", anaVersion)
  #xml.LoadKeyValue("runPeriod", args["<run_number>"])
  xml.LoadKeyValue("useBeamWeight", "1")
  
  fluxHelper = minos.ntupleutils.NuFluxHelper(xml)

  particles = vector(int)()
  if args['all']:
    particles.push_back(minos.ntupleutils.NuParticle.kNuMu)
    particles.push_back(minos.ntupleutils.NuParticle.kNuMuBar)
  elif args['nu']:
    particles.push_back(minos.ntupleutils.NuParticle.kNuMu)
  elif args['nubar']:
    particles.push_back(minos.ntupleutils.NuParticle.kNuMuBar)
  fluxHelper.ParticlesToExtrapolate(particles)

  # Check the particles and spit out debug info
  particleFlags = [fluxHelper.IsParticleToExtrapolate(x) for x in [minos.ntupleutils.NuParticle.kNuMu, minos.ntupleutils.NuParticle.kNuMu]]
  logger.debug("Extrapolating: numu:{}, nubar:{}".format(*particleFlags))

  # Set the beam type
  fluxHelper.BeamType(BeamType.kL010z185i)

  # Set the output filename
  if args["-o"]:
    logger.debug("Setting output file {}".format(args["-o"]))
    fluxHelper.OutputFilename(args["-o"])
  else:
    sample = "All" if args['all'] else ("NuMu" if args["nu"] else "NuMuBar")
    name = "FluxHelpers{}Run{}.root".format(sample, args["<run_number>"])
    logger.debug("Setting output file {}".format(name))
    fluxHelper.OutputFilename(name)

  # Configure the cross-section filename
  xsecfilename = Datatool().get_dataset("xsec").only
  fluxHelper.CrossSectionFile(xsecfilename)
  
  fluxHelper.MakeHelperHistos(args["<flux_files>"])