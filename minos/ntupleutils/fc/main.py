#!/usr/bin/env python
# coding: utf-8

"""Generates Feldman-Cousins experiments for FHC+RHC combined data, for the
thesis of Nicholas Devenish. Easily extendable to e.g. take in a configuration
file or just more options.

Usage:
  fc.py [-n COUNT | -u] [--no-systematics] [-v] [-o OUTPUT_FILE] 
        [--detail=DETAIL_FILE] [--pdf] [--1dfitsin] <dm2bar> <sn2bar>

Options:
 -n COUNT --number=COUNT   Number of experiments to run [default: 10]
 -u, --unlimited           Continuously run experiments until killed
 --no-systematics          Do not apply any systematic shifts to experiments
 -o OUTPUT_FILE            Set the output deltaChi2 file name specifically
 -v, --verbose             Set verbose output level
 --detail=DETAIL_FILE      If set, will dump a detail array to a separate file
 --pdf                     Will generate a pdf page for every experiment,
                           named the same as the output file +pdf
 --1dfitsin                Does 1D fitting fixing dm2bar - e.g. marginalising
                           for sin22thetabar at each grid point.
"""

import sys, os
from collections import namedtuple
import random
import zlib
import uuid
import base64
import math
import logging
logger = logging.getLogger(__name__)

from docopt import docopt
import numpy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import minos.matplotlib
import minos.ntupleutils as ntu
from datatool import Datatool
dataLib = Datatool()
from simplehist import Hist, ashist

from .systematics import ThesisSystematics, Systematics
from .util import load_and_oscillate_events
from .experiment import Experiment

FCSample = namedtuple("FCSample", ["sample", "pot"])

dump_format = numpy.dtype([('chi2', '<f8'), ('dm2bar', '<f8'), ('sn2bar', '<f8'), ('fhc', '|u1', (400,)), ('rhc', '|u1', (400,))])

def load_sample_events(samples, oscillation=None):
  events = []
  ev_files = dataLib.get_dataset("reduced_fc_events")
  for sample in samples:
    events.append(load_and_oscillate_events(ev_files.tagged(sample.sample), sample.pot, oscillation, nu=False))
  return tuple(events)

def load_helpers(samples):
  helpers = []
  for sample in samples:
    # Load the helpers for each sample
    helperFilename = dataLib.get_dataset("thesis_helpers").tagged(sample.sample).only
    helpers.append(ntu.NuMMHelperCPT(helperFilename, dataLib.get_dataset("xsec").only))
  return tuple(helpers)

def fluctuate(hist):
  "Returns the poisson fluctuated version of a histogram"
  return ntu.Spectrum(ntu.binningscheme4(), data=numpy.random.poisson(hist), pot=hist.pot)

def fhcd(hist, *args, **kwargs):
  "Draw a rebinned FHC histogram"
  h = ntu.rebin_fd(hist)
  h /= (h.bins[1:]-h.bins[:-1])
  return h.draw_hist(*args, **kwargs)

def rhcd(hist, *args, **kwargs):
  "Draw a rebinned RHC histogram"
  h = ntu.rebin_fd_rhc(hist)
  h /= (h.bins[1:]-h.bins[:-1])
  return h.draw_hist(*args, **kwargs)

def draw_data(hist, *args, **kwargs):
  """Draw a data-style histogram"""
  bin_widths = hist.bins[1:]-hist.bins[:-1]
  bin_centers = hist.bins[:-1]+bin_widths*0.5
  return plt.errorbar(bin_centers, hist, xerr=bin_widths*0.5, ls='None', marker='o', capsize=0, **kwargs)

def infinite_generator():
  x = 0
  while True:
    yield x
    x += 1

def main(args):
  args = docopt(__doc__,argv=args)
  # Activate logging if we need it
  if args["--verbose"]:
    logging.basicConfig(level=logging.DEBUG)
  else:
    logging.basicConfig(level=logging.INFO)

  # Extract running information
  experiment_count = int(args["--number"])
  if args["--unlimited"]:
    experiment_count = "unlimited"

  dm2bar = float(args["<dm2bar>"])
  sn2bar = float(args["<sn2bar>"])

  # if args["--pdf"] and args["--unlimited"]:
  #   raise RuntimeError("Cannot run both --pdf and --unlimited; file will never close.")

  # Determine the output filename
  if args["-o"] is None:
    output_file = "chi2_{:.2f}_{:.3f}.{}.dat".format(dm2bar*1000,sn2bar, str(uuid.uuid4())[:6])
  else:
    output_file = args["-o"]
  detail_file = args["--detail"]
  pdf_file = None
  if args["--pdf"]:
    pdf_file = os.path.splitext(output_file)[0] + ".pdf"
  
  # Summarize the options
  logger.info("Running {} experiments with dm2bar={:.2f}e-3, sn2bar={:.3f}".format(experiment_count, dm2bar*1000, sn2bar))
  logger.info("Writing experiment deltaChi2 results to {}".format(output_file))

  # Set up the samples that we are going to use
  samples = [FCSample("run3",7.093e20), FCSample("run4",3.4e20)]
  oscillation_pars = ntu.Parameters(dm2=2.43e-3, sn2=1.0, dm2bar=dm2bar, sn2bar=sn2bar)

  # Load all event sets
  events = load_sample_events(samples, oscillation_pars)
  
  # Create systematic shifters for every event sample
  shifters = ntu.mapTuples(lambda x: Systematics(x), [events], skip_none=True)
  helpers = load_helpers(samples)

  # Make an empty far detector NQ spectrum to use as a placeholder
  far_nq = ntu.Spectrum(ntu.binningscheme4(),pot=7e20)

  if pdf_file:
    pages = PdfPages(pdf_file)
  
  if args["--unlimited"]:
    experiment_range = infinite_generator()
  else:
    experiment_range = range(experiment_count)

  try:
    for i in experiment_range:
      logger.info("Experiment {}".format(i))
      
      # Generate a random set of shifts, and the full-statistics histograms for them
      shift = ThesisSystematics.random_shifts()
      hists = ntu.mapTuples(lambda x: x.shifted_histogram(shift), [shifters], skip_none=True)
      
      # Flucturae each shifted detector sample to make the experiment
      far_pq = ntu.HornCurrent._make(fluctuate(x.far.pq) for x in hists)
      expt_data = ntu.HornCurrent._make(ntu.Detectors(near=x.near,far=ntu.ChargeSignTuple(far_nq, y)) for x, y in zip(hists, far_pq))
      experiment = Experiment(expt_data, helpers)

      # Run the fit
      if args["--1dfitsin"]:
        result = experiment.fit_sin_only(oscillation_pars)
      else:
        result = experiment.fit(oscillation_pars)
      logger.info("SystFitter  dm2bar={:.2e} sn2bar={:.2f}".format(result["dm2bar"], result["sn2bar"]))

      # Build the dumping data
      deltaChi2 = experiment.likelihood(oscillation_pars) - experiment.likelihood(result)
      if detail_file:
        flat_data = ntu.HornCurrent(*[numpy.hstack([x.near.nq,x.near.pq,x.far.nq,x.far.pq]) for x in expt_data])
        dump_data = (deltaChi2, result["dm2bar"], result["sn2bar"], flat_data.fhc, flat_data.rhc)
        dump_arr = numpy.asarray([dump_data], dtype=dump_format).tostring()
        dump_arr = base64.b64encode(zlib.compress(dump_arr, 9))
        with open("dump.dat", 'ab') as dumpfile:
          dumpfile.write(dump_arr)
          dumpfile.write(b"\n")
      dump_value = numpy.array([deltaChi2], dtype=numpy.float32).tostring()
      with open(output_file, 'ab') as dumpfile:
        dumpfile.write(dump_value)

      # if deltaChi2 < 0:
      #   logger.debug("Got negative DeltaChi2: {}".format(deltaChi2))
      #   import pdb
      #   pdb.set_trace()

      if pdf_file:
        logger.info("Generating PDF page...")
        # Draw a figure for this
        fig = plt.figure(figsize=((8.3-0.4)/3*4, 8.3-0.4))
        ax_like = plt.subplot2grid((2,3),(0,0),colspan=2,rowspan=2)
        ax_fhc = plt.subplot2grid((2,3),(0,2))
        ax_rhc = plt.subplot2grid((2,3),(1,2))

        for sample, axis, extrap, data, fn in zip(["FHC","RHC"], [ax_fhc,ax_rhc], experiment.extrapolators, expt_data, [fhcd, rhcd]):
          plt.sca(axis)
          nooschist = ashist(extrap.MakeFDBarPred(ntu.Parameters().toMM()))
      
          rebinner = ntu.rebin_fd if sample == "FHC" else ntu.rebin_fd_rhc

          data = rebinner(data.far.pq)
          bin_widths = (data.bins[1:]-data.bins[:-1])
          data /= bin_widths

          fn(nooschist, color='r', label="No Osc")
          draw_data(data, color='k', label="Data")
          fn(ashist(extrap.MakeFDBarPred(result.toMM())), color='b', label="Fit")
         
          plt.xlabel("Energy (GeV)")
          plt.ylabel("Events/GeV")
          plt.title("{} Simulated Data".format(sample))
          plt.xscale("compressedenergy")
          plt.legend(fontsize=8)
          # Work out the unoscillated height to use for general height
          # no_rebin = ntu.rebin_fd(nooschist)
          # plt.ylim(0, 1.5*numpy.max(no_rebin/(no_rebin.bins[1:]-no_rebin.bins[:-1])))
          plt.ylim(0,50)


        plt.sca(ax_like)

        xBins = numpy.linspace(0,1.0,50)
        yBins = numpy.linspace(0e-3,10e-3,50)
        if result["dm2bar"] > 10e-3:
          # def roundup(x):
          maxval = int(math.ceil(result["dm2bar"] / 10e-3)) * 10e-3
          yBins = numpy.linspace(0e-3,maxval,int(50*100*maxval))
        data = numpy.zeros((len(xBins), len(yBins)))
        for xbin, sn2 in enumerate(xBins):
          for ybin, dm2 in enumerate(yBins):
            pointParam = result.copy_with(dm2bar=dm2,sn2bar=sn2)
            data[xbin,ybin] = experiment.likelihood(pointParam)
        data -= numpy.min(data)
        
        # cs = plt.contour(xBins,yBins,data.T,[2.3,4.61,11.83])
        plt.pcolormesh(xBins, yBins, data.T, vmax=12, edgecolor="face")
        plt.suptitle(r"Exp {}: $\Delta\bar m^2={:.2f}$ meV, $\sin^22\bar\theta={:.2f},\Delta\chi^2={:.2f}$".format(i, result["dm2bar"]*1000, result["sn2bar"], deltaChi2))
        plt.xlabel(r"$\sin^22\bar\theta$")
        plt.ylabel(r"Energy (GeV)")
        
        plt.plot([result["sn2bar"]], [result["dm2bar"]], marker='o', color='r', ms=15)
        ax_like.yaxis.set_major_formatter(minos.matplotlib.FixedOrderFormatter(-3))
        plt.colorbar()
        plt.ylim(0, yBins[-1])
        plt.tight_layout()

        pages.savefig()
        plt.close()
  finally:
    if pdf_file:
      pages.close()

if __name__ == "__main__":
  main(args=sys.argv[1:])