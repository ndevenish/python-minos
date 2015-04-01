# coding: utf-8

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
    



  def likelihood(self, parameters):
    if not isinstance(parameters, ntu.NuMMParameters):
      parameters = parameters.toMM()
    return self.fitter.Likelihood(parameters)