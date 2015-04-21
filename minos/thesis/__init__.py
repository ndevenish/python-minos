# coding: utf-8
"""Contains data relating to thesis analysis"""

from .extrapolators import *

import logging
logger = logging.getLogger(__name__)
import os
import matplotlib.pyplot as plt

from .plots import plot
from .plots import savefig_direct as savefig
import plots

import styles
from .styles import Sizes

class MathText(object):
  dmbar = r"$\left|\Delta\bar m^2\right|$"
  dmbaraxis = r"$\left|\Delta\bar m^2\right| \left(\textrm{eV}^2\right)$"
  snbar = r"$\sin^2 \left(2\bar\theta\right)$"
  snbaraxis = snbar
  energy = r"Energy (GeV)"
