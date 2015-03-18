# coding: utf-8
"""Contains data relating to thesis analysis"""

from .extrapolators import *

import logging
logger = logging.getLogger(__name__)
import os
import matplotlib.pyplot as plt

import styles

FORMATS = ["png", "pdf", "eps"]

class Sizes(object):
  A4 = (8.3-0.4, 11.7-0.4) # With 5mm margin on all sides
  Standard = (5.9, 4.4)
  Wide = (4.9, 3.3)
  Half = (5.9*0.49, 5.9*0.49*(3./4.))

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