#!/usr/bin/env python
# coding: utf-8

"""Convert a NuFCEvent TTree to python tables

Usage: convert.py [--extension=<ext>] <input> [<input>...]

Options:
  -e <ext>, --extension <ext>   The extension to append [default: hdf5]
"""

from __future__ import absolute_import, print_function

import sys
import os
import time
from docopt import docopt
import logging
logger = logging.getLogger(__name__)

from ROOT import TFile
import numpy
import tables

ACCEPTED_TYPES = {'UInt_t', 'Float_t', 'Int_t', 'Char_t'}
ROOT_TYPE_MAP = {"UInt_t": "uint32", "Float_t": "float32",
                 "Int_t": "int32", "Char_t": "int8"}
TREE_ACCESS_METHOD = {"UInt_t": lambda x: x.GetValueLong64,
                      "Float_t": lambda x: x.GetValue,
                      "Int_t": lambda x: x.GetValueLong64,
                      "Char_t": lambda x: x.GetValueLong64,
    }

if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  arguments = docopt(__doc__)

  for inFile in arguments["<input>"]:
    outputName = os.path.splitext(inFile)[0] + "." \
        + arguments["--extension"].lstrip(".")
    logger.info("Processing {}".format(inFile))
    f = TFile(inFile)
    if not f.IsOpen():
      logger.error("Could not open file " + inFile)
      sys.exit(1)
    # Find the lone TTree
    tree_key = {x.GetName() for x in f.GetListOfKeys()
                if x.GetClassName() == "TTree"}
    if not tree_key:
      logger.error("Could not find TTree in file " + inFile)
      sys.exit(1)
    if len(tree_key) > 1:
      logger.error("More than one TTree found in file " + inFile)
      sys.exit(1)
    tree_name = tree_key.pop()
    tree = f.Get(tree_name)
    logger.info("Converting tree named " + tree_name)

    leaves = [x for x in tree.GetListOfLeaves()
              if x.GetTypeName() in ACCEPTED_TYPES
              and not x.GetName() in {"fBits", "fUniqueID"}]
    # Build the numpy field list
    dtype = [(x.GetName(), ROOT_TYPE_MAP[x.GetTypeName()]) for x in leaves]

    data = numpy.zeros(tree.GetEntries(), dtype=dtype)

    accessors = [TREE_ACCESS_METHOD[x.GetTypeName()](x) for x in leaves]

    # Get the POT entry
    pot = f.hTotalPot.Integral()

    # Loop over every entry in the tree
    next_time = time.time() + 3
    for entry in tree:
      item = numpy.array(tuple(x() for x in accessors), dtype=dtype)
      data[tree.GetReadEntry()] = item
      if time.time() > next_time:
        logger.info(
            "Processing {}/{}".format(tree.GetReadEntry(), tree.GetEntries())
            )
        next_time = time.time() + 3
    logger.info(
        "Conversion of {} items in {} POT done.".format(tree.GetEntries(), pot)
        )
    logger.info("Writing to output file " + outputName)

    outfile = tables.open_file(outputName, mode='w', title=f.GetTitle())
    table = outfile.create_table(
        outfile.root, tree.GetName(), data, tree.GetTitle()
        )
    table.attrs.POT = pot
    outfile.flush()
    print ()
