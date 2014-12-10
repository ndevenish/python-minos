# coding: utf-8
from .pyroot import NuCutter, NuCut

def get_cutter(name):
  return NuCutter.GetNewCutInstance(name, None)

def BravoTwo():
  return get_cutter("BravoTwo")