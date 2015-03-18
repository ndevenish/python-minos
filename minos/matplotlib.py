# coding: utf-8

from __future__ import absolute_import, division

import numpy as np

from matplotlib.scale import ScaleBase, register_scale
from matplotlib.ticker import (NullFormatter, ScalarFormatter,
                               LogFormatterMathtext, FixedLocator)
from matplotlib.ticker import (NullLocator, LogLocator, AutoLocator,
                               SymmetricalLogLocator)
from matplotlib.transforms import Transform



class FixedOrderFormatter(ScalarFormatter):
    """Formats axis ticks using scientific notation with a constant order of 
    magnitude"""
    def __init__(self, order_of_mag=0, useOffset=True, useMathText=True):
        self._order_of_mag = order_of_mag
        ScalarFormatter.__init__(self, useOffset=useOffset, 
                                 useMathText=useMathText)
    def _set_orderOfMagnitude(self, range):
        """Over-riding this to avoid having orderOfMagnitude reset elsewhere"""
        self.orderOfMagnitude = self._order_of_mag

class CompressedEnergyScale(ScaleBase):
  """Compresses the x axis so that 20-50 GeV and 50-200 GeV are smaller"""
  name = "compressedenergy"

  def __init__(self, axis, **kwargs):
    super(CompressedEnergyScale, self).__init__()

  def set_default_locators_and_formatters(self, axis):
    """
    Set the locators and formatters to reasonable defaults for
    linear scaling.
    """
    axis.set_major_locator(FixedLocator([0, 5, 10, 15, 20, 30, 40, 50, 200]))
    axis.set_major_formatter(ScalarFormatter())
    axis.set_minor_locator(FixedLocator([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 80, 110, 140, 170, 200]))
    axis.set_minor_formatter(NullFormatter())

  def get_transform(self):
    return self.CompressedEnergyTransform()

  class CompressedEnergyTransform(Transform):
    input_dims = 1
    output_dims = 1
    is_separable = True
    has_inverse = True

    def transform_non_affine(self, values):
      data = np.array(values)
      # Everything larger than 50 is compressed 15x (so 50-200 -> 50-60)
      data[data > 50] = (data[data>50]-50)/15 + 50
      # and, everything larger than 20 is compressed 2x (so that 20-50 -> 20-35)
      data[data > 20] = (data[data>20]-20)/2 + 20
      return data

    def inverted(self):
      return CompressedEnergyScale.InvertCompressedEnergyTransform()

  class InvertCompressedEnergyTransform(Transform):
    input_dims = 1
    output_dims = 1
    is_separable = True
    has_inverse = True

    def inverted(self):
      return CompressedEnergyScale.CompressedEnergyTransform()

    def transform_non_affine(self, values):
      data = np.array(values)
      data[data>20] = (data[data>20]-20)*2 + 20
      data[data>50] = (data[data>50]-50)*15 + 20
      return data

register_scale(CompressedEnergyScale)