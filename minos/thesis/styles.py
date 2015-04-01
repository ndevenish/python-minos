#coding: utf-8

# class Sizes(object):
#   A4 = (8.3-0.4, 11.7-0.4) # With 5mm margin on all sides
#   Standard = (5.9, 5.5)
#   Wide = (4.9, 3.3)
#   Half = 

import matplotlib as mpl
#from minos.thesis import Sizes

class Sizes(object):
  A4 = (8.3-0.4, 11.7-0.4) # With 5mm margin on all sides
  Standard = (5.9, 4.4)
  Wide = (5.9, 3.3)
  Half = (5.9*0.49, 5.9*0.49*(3./4.))
  FullPage = (5.9, 5.9*1.4) # A4 ratio, but thesis fit


Standard = {
  "figure.figsize": Sizes.Standard,
  "font.size": 12,
  "legend.numpoints": 1,
  "legend.fontsize": "medium"
}

Wide = {
  "figure.figsize": Sizes.Wide,
  "font.size": 12,  
}

# Used for half-width 4:3 plots e.g. side-by-side
Half = {
 "figure.figsize": Sizes.Half,
 "font.size": 9,
 "legend.fontsize": "small",
}

FullPage = {
  "figure.figsize": Sizes.FullPage,
}

def figure_style(style):
  """Uses the matplotlib style context manager for a specific function"""
  def _wrap(fn):
    def _innerwrap(*args, **kwargs):
      with mpl.style.context(style):
        return fn(*args, **kwargs)
    return _innerwrap
  return _wrap
