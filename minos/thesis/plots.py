# coding: utf-8

import logging
logger = logging.getLogger(__name__)

import os, sys
from collections import defaultdict, namedtuple

import matplotlib
import matplotlib.pyplot as plt
from docopt import docopt

matplotlib.rcParams["text.usetex"] = True

_CHAPTERS = {"results", "fc", "select"}

PlotEntry = namedtuple("PlotEntry", ["module", "chapter", "name", "func"])

# _PLOTS = defaultdict(dict)
_PLOTS = []


DEFAULT_FORMATS = ["png", "pdf", "eps"]

_USAGE_STR = """Renders thesis plots.

Usage:
  plots [--pdf] [--png] [--eps] [-l] [-w] [<KEY> [<KEY>]...]

Options:
  --pdf        Renders a pdf file for each plot. Without any of the format
               options, will default to a mix of all types.
  --png        Renders a png file for each plot
  --eps        Renders an eps file for each plot
  -l, --list   List the plots to be rendered, without rendering any. This is
               the default behavior when running the plot tool.
  -w, --write  Actually writes the plots to disk. Default when running modules.
"""

def plot(chapter, name, module=None):
  assert chapter in _CHAPTERS
  def _wrap(func):
    # _PLOTS[chapter][name] = func
    _PLOTS.append(PlotEntry(func.__module__ if module is None else module, chapter, name, func))
    return func
  return _wrap

def register_plot(chapter, name, func):
  assert chapter in _CHAPTERS, "Chapter must be one of {}".format(", ".join(_CHAPTERS))
  _PLOTS.append(PlotEntry(func.__module__, chapter, name, func))

def _process_argument_formats(options):
  """Convert a usage object to a list of file extensions"""
  formats = []
  no_formats_specified = not (options["--pdf"] or options["--eps"] or options["--png"])
  if options["--pdf"] or no_formats_specified:
    formats.append("pdf")
  if options["--png"] or no_formats_specified:
    formats.append("png")
  if options["--eps"] or no_formats_specified:
    formats.append("eps")
  return set(formats)

def _plot_key_match(plot, key):
  """Does a given key match a plot in any way?"""
  if key.lower() in plot.name.lower():
    return True
  if key == plot.chapter or key == "chapter_"+plot.chapter:
    return True
  return False

def _filter_plots(plots, keys):
  for key in keys:
    plots = [x for x in plots if _plot_key_match(x, key)]
  return plots


def run_module_directly():
  options = docopt(_USAGE_STR)
  # Only process __main__ plots in this case
  plots = [x for x in _PLOTS if x.module == "__main__"]
  return _process_main(options, plots)

def plot_main():
    options = docopt(_USAGE_STR)
    # If run as main, invert the list behavior
    options["--list"] = not options["--write"]
    _process_main(options, _PLOTS)

def _process_main(options, plotlist):
  global DEFAULT_FORMATS
  DEFAULT_FORMATS = _process_argument_formats(options)
  plots = _filter_plots(plotlist, options["<KEY>"])

  if options["--list"]:
    for plot in plots:
      print "chapter_{}/{}".format(plot.chapter, plot.name)
    logger.info( "{} plots".format(len(plots)))
  else:
    if not plots:
      logger.warning("No plots to process.")
      return
    logger.info("Processing {} plots".format(len(plots)))
    for plot in plots:
      # Get the directory
      dirname = os.path.dirname(sys.modules[plot.module].__file__)
      current_wd = os.getcwd()
      try:
        if dirname:
          os.chdir(dirname)
        figure = plot.func()
        savefig(figure, plot.chapter, plot.name)
      finally:
        os.chdir(current_wd)

def process_module(name):
  "Run all of the plot generation for a particular module"
  plots = [x for x in _PLOTS if x.module == name]
  for plot in plots:
    figure = plot.func()
    savefig(figure, plot.chapter, plot.name)

def savefig(figure, chapter, name, formats=None):
  basePath = "thesis"
  if "THESIS_IMAGES" in os.environ:
    basePath = os.environ["THESIS_IMAGES"]
  # Make sure the destination exists
  imageDir = os.path.join(basePath, "chapter_" + chapter, "images")
  if not os.path.isdir(imageDir):
    os.makedirs(imageDir)
  path = os.path.join(imageDir, name)
  # Decide which formats we are saving in
  if formats is None:
    formats = DEFAULT_FORMATS
  # Do saving
  savednames = []
  for ext in formats:
    outputname = "{}.{}".format(path, ext)
    savednames.append(outputname)
    figure.savefig(outputname)
    logger.info("Saved {}".format(outputname))
  plt.close(figure)
  return savednames

# Save a figure to a standard thesis image directory
def savefig_direct(figure, location):
  "The old form of saving thesis figures"
  chapter, name = os.path.split(location)
  return savefig(figure, chapter, name)