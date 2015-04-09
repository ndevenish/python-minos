# coding: utf-8

import logging
logger = logging.getLogger(__name__)
import numpy
import minos.ntupleutils as ntu
from .systematics import ThesisSystematics

def _create_run(helper, data):
  ex = ntu.NuMMRunFC(helper, data.near.nq, data.near.pq, data.far.nq, data.far.pq)
  ex.PredictNus(False)
  ex.QuietModeOn()
  return ex

class Experiment(object):
  def __init__(self, data, helpers):
    self.data = data
    # Construct the extrapolators for each sample
    data_matrix = ntu.mapTuples(lambda x: x.to_numatrix(), [data])
    self.extrapolators = [_create_run(h, dat) for dat, h in zip(data_matrix, helpers)]

    self.fitter = ntu.NuSystFitter()
    self.fitter.BatchModeOn()
    for _ex in self.extrapolators:
      self.fitter.push_back(_ex)
    
  def fit(self, params=None):
    start_params = params or ntu.Parameters(dm2=2.5e-3, sn2=1.0, cpt=True)
    mmPars = start_params.toMM()
    mmPars.ReleaseDm2Bar()
    mmPars.ReleaseSn2Bar()
    mmPars.ConstrainPhysical()

    result = self.fitter.FCMinimise(mmPars)
    
    best = ntu.Parameters(dm2=result.Dm2(), dm2bar=result.Dm2Bar(), sn2=result.Sn2(), sn2bar=result.Sn2Bar())
    return best

  def fit_sin_only(self, params):
    fitter = ntu.Fitter(self.extrapolators)
    fitResult = fitter.minimize(params.copy_with(sn2bar=0.8), ["sn2bar"])
    return params.copy_with(sn2bar=fitResult.x[0])

  def fit_dm_only(self, params):
    fitter = ntu.Fitter(self.extrapolators)

    def _do_logsearch():
      # Perform a FCMinimise-style log search
      probe_dm2s = numpy.hstack([numpy.linspace(0.5e-3, 30e-3, 20), 10**numpy.linspace(-1.5, 0, 16)])
      likes = [fitter.likelihood(params.copy_with(dm2bar=x)) for x in probe_dm2s]
      return probe_dm2s[numpy.argmin(likes)]

    dmbar_seed = _do_logsearch()
    logger.info("Seeding log search found {:.2e}".format(dmbar_seed))
    fitResult = fitter.minimize(params.copy_with(dm2bar=dmbar_seed), ["dm2bar"])
    return params.copy_with(dm2bar=fitResult.x[0])

  # result = experiment.fit_dm_only(oscillation_pars)


  def likelihood(self, parameters):
    if not isinstance(parameters, ntu.NuMMParameters):
      parameters = parameters.toMM()
    return self.fitter.Likelihood(parameters)