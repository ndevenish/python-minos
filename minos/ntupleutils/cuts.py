# coding: utf-8

try:
  from .pyroot import NuCutter

  def get_cutter(name):
    return NuCutter.GetNewCutInstance(name, None)


  def BravoTwo():
    return get_cutter("BravoTwo")


  def Passthrough():
    return get_cutter("Passthrough")

except ImportError:

  def get_cutter(name):
    raise ImportError("Using reduced NtupleUtils library; Cannot import NuCutter")
  def BravoTwo():
    raise ImportError("Using reduced NtupleUtils library; Cannot import NuCutter")
  def Passthrough():
    raise ImportError("Using reduced NtupleUtils library; Cannot import NuCutter")
