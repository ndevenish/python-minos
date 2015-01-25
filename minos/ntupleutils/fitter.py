# coding: utf-8

from .pyroot import NuMMRun
import numpy as np

# Handle the case where scipy does not work
try:
  from scipy.optimize import minimize
except ImportError as e:
  def minimize(*args, **kwargs):
    raise ImportError("Could not import scipy.optimize; {}".format(e))

class Fitter(object):
  def __init__(self, runs=None):
    if isinstance(runs, NuMMRun):
      self.runs = [runs]
    else:
      self.runs = runs or []

  def append(self, run):
    self.runs.append(run)

  def likelihood(self, parameters):
    if hasattr(parameters, "toMM"):
      parameters = parameters.toMM()
    return sum(x.ComparePredWithData(parameters) for x in self.runs)

  def minimize(self, parameters, variables, options=None, bounds=None):
    """Run a minimization routine over specified variables."""
    # Build the actual variable parameters object for minimization
    min_pars = np.asarray([parameters[x] for x in variables])
    bounds = bounds or [parameters.bounds(x) for x in variables]
    # A temporary function to handle the swizzling
    def _do_min(var_vals):
      pars = parameters.copy_with(**{key: value for key, value in zip(variables, var_vals)})
      return self.likelihood(pars)

    return minimize(_do_min, min_pars, bounds=bounds, options=options)


