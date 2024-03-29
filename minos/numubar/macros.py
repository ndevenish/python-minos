# coding: utf-8

import sys, os
from docopt import docopt
from .pyroot import NuBase, NuDSTAna
from minos.ntupleutils import NuXMLConfig

from minos.runquality import RunQualityFinder

def script_wrapper(func, argv=None):
  if not argv:
    argv = sys.argv[1:]
  args = docopt(func.__doc__, argv=argv)
  # Reduce this arguments dictionary
  shortargs = {x[1:-1]: y for x, y in args.iteritems() if x.startswith("<") and x.endswith(">")}
  func(**shortargs)

def MakeSummary(input_file, output_file, xml_file):
  """Usage: MakeSummary <input_file> <output_file> <xml_file>"""
  assert os.path.isfile(input_file)
  assert os.path.isfile(xml_file)
  
  NuBase.InputFileName(input_file)
  NuBase.LoadTrees(False)
  # Create the analysis object
  ana = NuDSTAna()
  ana.OpenOutFile(output_file)
  ana.MMRereco("null", xml_file)
  ana.WriteOutHistos()
  ana.CloseOutFile()
  print ("End of MakeSummary")

def MicroDST(input_file, analysis_version):
  """Usage: MicroDST <analysis_version> <input_file>"""
  NuBase.InputFileName(input_file)
  NuBase.LoadTrees(False)
  RunQualityFinder.OverrideDB()
  ana = NuDSTAna()
  ana.MakeMicroDST(analysis_version)
  ana.WriteOutHistos()