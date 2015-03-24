# coding: utf-8
from .pyroot import NuCutter


def get_cutter(name):
  return NuCutter.GetNewCutInstance(name, None)


def BravoTwo():
  return get_cutter("BravoTwo")


def Passthrough():
  return get_cutter("Passthrough")
