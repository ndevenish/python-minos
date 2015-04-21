# coding: utf-8

import uuid

from .structs import ChargeSignTuple
from .pyroot import NuMatrixSpectrum, NuMMRunFC, NuMMHelperCPT, NuMMParameters, NuUtilities
from array import array

import simplehist
from simplehist import Hist, ashist

from ROOT import TH1D

import numpy

def load_matrix_pair(filename, histname):
  """Loads a pair of matrixspectrums from a data file.
  Args:
    filename  The .root filename to load from
    histname  The name of the histogram, with a '{}' placeholder for the
              location where the charge-sign indicator should be inserted
              e.g. "RecoEnergy{}_FD"
  Returns:
    A ChargeSignTuple of NuMatrixSpectrum's
  """
  nq = NuMatrixSpectrum(filename, histname.format(""))
  pq = NuMatrixSpectrum(filename, histname.format("PQ"))
  return ChargeSignTuple(nq, pq)

def load_spectrum_pair(filename, histname):
  return ChargeSignTuple._make(ashist(x) for x in load_matrix_pair(filename, histname))


# prepare_fake_run(["Daikon07", "Dogwood3", "Bravo0720", "run1"])
# Helper: "combined"
# Near:   "nd"
# Far:    "fd"
# def prepare_fake_run(data_tags, pot):
#   tags = list(data_tags) + ["mc"]
#   # Assemble the files
#   combined_helper_file = shared_library.get_file(tags + ["combined"])
#   xsec_file = shared_library.get_file(["xsec"])
#   helper = NuMMHelperCPT(combined_helper_file, xsec_file)
  
#   nd_file = shared_library.get_file(tags + ["nd", "summary"])
#   fd_file = shared_library.get_file(tags + ["fd", "summary"])
#   nd_data = load_matrix_pair(nd_file, "RecoEnergy{}_ND")
#   fd_data = load_matrix_pair(fd_file, "RecoEnergy{}_FD")
#   fd_data.nq.ScaleToPot(pot)
#   fd_data.pq.ScaleToPot(pot)
#   run = NuMMRunFC(helper, nd_data.nq, nd_data.pq, fd_data.nq, fd_data.pq)
#   run.QuietModeOn()
#   return run

def binningscheme4():
  "Returns a numpy array of the standardised NuMuBar binning, kNuMuBar0325Std2"
  return array('d', NuUtilities.RecoBins(4))

def binning_displayfd():
  return array('d', NuUtilities.RecoBins(10))


def binning_displayfd_RHC():
  return array('d', NuUtilities.RecoBins(8))

def binning_displaynd():
  #Reco Energy: 1 Gev to 30 GeV, 2 GeV from 30 to 50 GeV; One 150 GeV bin to 200 GeV
  return array('d', NuUtilities.RecoBins(7))

def rebin(data, bins, newBins):
  newBins = numpy.asarray(newBins)
  data = numpy.asarray(data)
  # Make sure ALL new bin splits were in the previous bin data e.g. no split bins
  assert all(any(numpy.allclose(x, y) for y in bins) for x in newBins)
  assert len(data) == len(bins)-1
  binIndex = numpy.digitize(bins, newBins)
  newData = numpy.zeros(len(newBins)-1)
  for _bin, _value in zip(binIndex, data):
    newData[_bin-1] += _value
  
  return (newData, newBins)

def rebin_fd(data):
  data, bins = rebin(data, data.bins, binning_displayfd())
  return Hist(bins, data=data)

def rebin_fd_rhc(data):
  data, bins = rebin(data, data.bins, binning_displayfd_RHC())
  return Hist(bins, data=data)
  
def rebin_nd(data):
  data, bins = rebin(data, data.bins, binning_displaynd())
  return Hist(bins, data=data)

try:
  from simplehist.converter import converts_type, ashist
  @converts_type("ROOT.NuMatrixSpectrum")
  def fromNuMatrixSpectrum(hist):
    rh = ashist(hist.Spectrum()).view(Spectrum)
    rh.pot = hist.GetPOT()
    return rh
except ImportError:
  pass

class PotArray(numpy.ndarray):
  def __array_finalize__(self, obj):
    self.pot = getattr(obj, "pot", None)
  def __repr__(self):
    rep = super(PotArray, self).__repr__()
    if self.pot is not None:
      rep = rep[:-1] + ", pot={})".format(self.pot)
    return rep
  @classmethod
  def convert(cls, froma, pot=None):
    newv = froma.view(cls)
    newv.pot = pot
    return newv

class Spectrum(Hist):
  def __new__(cls, bins, data=None, pot=None):
    obj = simplehist.Hist.__new__(cls, bins, data=data)
    obj.pot = pot
    return obj
  def __array_finalize__(self,obj):
    super(Spectrum,self).__array_finalize__(obj)
    self.pot = getattr(obj, "pot", None)
  def __repr__(self):
    rep = super(Spectrum, self).__repr__()
    if self.pot is not None:
      rep = rep[:-1] + ", pot={})".format(self.pot)
    return rep
  def scale_to_pot(self, POT):
    scale = POT / self.pot
    self *= scale
    self.pot = POT
  def to_numatrix(self):
    hname = str(uuid.uuid4())[:6]
    spectrum = TH1D(hname,hname,len(self.bins)-1, self.bins)
    for bin_ in range(len(self.bins)-1):
      spectrum.SetBinContent(bin_+1, self[bin_])
    assert numpy.isclose(numpy.sum(self), spectrum.Integral())
    return NuMatrixSpectrum(spectrum, self.pot)

def mapTuples(func, items, skip_none=False):
  """Run a function on every item in a nest of tuples.
  This will recurse down the chain of tuples as long as every item
  is a list or tuple of the same length, and call the function with 
  every item as an argument.

  Arguments:
    skip_none:  if True, instances of None are not passed through
  """
  allTuples = all(isinstance(x, (tuple, list)) for x in items)
  # If all are lists/tuples and with the same length...
  if allTuples and all(len(x) == len(items[0]) for x in items):
    # Call the self-map over every corresponding entry
    newItems = []
    for i in range(len(items[0])):
      sublist = [x[i] for x in items]
      item = mapTuples(func, sublist, skip_none=skip_none)
      newItems.append(item)
    if hasattr(items[0], "_make"):
      return type(items[0])._make(newItems)
    else:
      return type(items[0])(newItems)
  else:
    # Not a list of tuples, so pass into the function
    if items == [None] and skip_none:
      return None
    else:
      return func(*items)

def iterTuples(item, path=False):
  """Iterates over every item of a multiple-depth tuple"""
  if isinstance(item, tuple):
    for i, subItem in enumerate(item):
      myPath = item._fields[i] if hasattr(item, "_fields") else i
      for x, _path in iterTuples(subItem, path=True):
        if path:
          yield x, tuple([myPath]+list(_path))
        else:
          yield x
  else:
    yield item, tuple()
