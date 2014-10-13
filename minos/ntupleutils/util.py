# coding: utf-8

from .structs import ChargeSignTuple
from .pyroot import NuMatrixSpectrum, NuMMRunFC, NuMMHelperCPT
from minos.data import shared_library

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
def prepare_fake_run(data_tags, pot):
  tags = list(data_tags) + ["mc"]
  # Assemble the files
  combined_helper_file = shared_library.get_file(tags + ["combined"])
  xsec_file = shared_library.get_file(["xsec"])
  helper = NuMMHelperCPT(combined_helper_file, xsec_file)
  
  nd_file = shared_library.get_file(tags + ["nd", "summary"])
  fd_file = shared_library.get_file(tags + ["fd", "summary"])
  nd_data = load_matrix_pair(nd_file, "RecoEnergy{}_ND")
  fd_data = load_matrix_pair(fd_file, "RecoEnergy{}_FD")
  fd_data.nq.ScaleToPot(pot)
  fd_data.pq.ScaleToPot(pot)
  run = NuMMRunFC(helper, nd_data.nq, nd_data.pq, fd_data.nq, fd_data.pq)
  run.QuietModeOn()
  return run

