# coding: utf-8
from .pyroot import NuMMParameters

class Parameters(object):
  """Contains all parameters required for prediction generation."""
  VALID_PARAM = ["dm2", "sn2", "dm2bar", "sn2bar"]
  def __init__(self, cpt=True, **kwargs):
    """Initialise, optionally with predetermined parameters.

    Keyword Arguments:
      cpt   Assume CPT conservation on creation, and copy nu => bar parameters
    """
    parameters = {x: y for x, y in kwargs.items() if x in self.VALID_PARAM}
    # Unpack any passed in packed
    if "nu" in kwargs:
      parameters["dm2"], parameters["sn2"] = kwargs["nu"]
    if "bar" in kwargs:
      parameters["dm2bar"], parameters["sn2bar"] = kwargs["bar"]

    if cpt and not "dm2bar" in parameters and not "sn2bar" in parameters:
      parameters["dm2bar"] = parameters["dm2"]
      parameters["sn2bar"] = parameters["sn2"]

    self.parameters = parameters
  
  def __getitem__(self, value):
    return self.parameters[value]

  def __setitem__(self, key, value):
    if not key in self.VALID_PARAM:
      raise IndexError("Invalid oscillation parameter: {}".format(key))
    self.parameters[key] = value

  def __repr__(self):
    return "Parameters(**{})".format(repr(self.parameters))

  def toMM(self):
    pars = NuMMParameters()
    pars.Dm2(self.parameters.get("dm2", 0.0))
    pars.Sn2(self.parameters.get("sn2", 0.0))
    pars.Dm2Bar(self.parameters.get("dm2bar", 0.0))
    pars.Sn2Bar(self.parameters.get("sn2bar", 0.0))
    pars.FixAllParameters()
    pars.SetQuietMode(True)
    return pars

  def copy_with(self, **kwargs):
    par = Parameters(**self.parameters)
    par.parameters.update({k: v for k,v in kwargs.items() if k in self.VALID_PARAM})
    return par

  def bounds(self, value):
    if value in ["dm2", "dm2bar"]:
      return (0, None)
    elif value in ["sn2", "sn2bar"]:
      return (0, 1)
    raise RuntimeError("Could not identify bounds for variable {}".format(value))