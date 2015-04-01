# coding: utf-8
"""Contains data relating to thesis analysis"""

from .extrapolators import *

import logging
logger = logging.getLogger(__name__)
import os
import matplotlib.pyplot as plt

FORMATS = ["png", "pdf", "eps"]



import styles
from .styles import Sizes


# Save a figure to a standard thesis image directory
def savefig(figure, location):
  basePath = "thesis"
  if "THESIS_IMAGES" in os.environ:
    basePath = os.environ["THESIS_IMAGES"]
  path, name = os.path.split(location)
  path = os.path.join(basePath, path, "images")
  if not os.path.isdir(path):
    os.makedirs(path)
  path = os.path.join(path, name)
  saved = []
  for ext in FORMATS:
    fullName = "{}.{}".format(path, ext)
    saved.append(fullName)
    figure.savefig(fullName)
    logger.info("Saved {}".format(fullName))
  plt.close(figure)
  return saved