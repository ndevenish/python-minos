# coding: utf-8

from .structs import ChargeSignTuple
from .pyroot import NuMatrixSpectrum, NuMMRunFC, NuMMHelperCPT, NuMMParameters, NuUtilities
from array import array

from simplehist import Hist

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
  data, bins = rebin(data.data, data.bins, binning_displayfd())
  return Hist(bins, data=data)
  
def rebin_nd(data):
  data, bins = rebin(data.data, data.bins, binning_displaynd())
  return Hist(bins, data=data)

try:
  from simplehist.converter import converts_type, fromTH1
  @converts_type("ROOT.NuMatrixSpectrum")
  def fromNuMatrixSpectrum(hist):
    return fromTH1(hist.Spectrum())
except ImportError:
  pass

class PotArray(numpy.ndarray):
  def __array_finalize__(self, obj):
    self.pot = getattr(obj, "pot", None)

class Spectrum(simplehist.Hist):
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
