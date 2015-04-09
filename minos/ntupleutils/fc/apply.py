#coding: utf-8

import tables
import numpy
import matplotlib.pyplot as plt
import matplotlib.colors
from scipy.interpolate import RectBivariateSpline

class FCApplicator(object):
  def __init__(self, filename):
    self.grids = {}
    with tables.open_file(filename) as tf:
      self.grids["0.68"] = tf.root.fcgrid_68.read()
      self.grids["0.90"] = tf.root.fcgrid_90.read()
      self.grids["0.9973"] = tf.root.fcgrid_3s.read()
      self.dm2s = tf.root.fcgrid_68.attrs.dm2s
      self.sn2s = tf.root.fcgrid_68.attrs.sn2s
    self.limits = [(self.sn2s[0], self.sn2s[-1]+(self.sn2s[-1]-self.sn2s[-2])),
                   (self.dm2s[0], self.dm2s[-1]+(self.dm2s[-1]-self.dm2s[-2]))]
    self.offset = {"0.68": 2.3, "0.90": 4.61, "0.9973":11.83}

  def pcolormesh(self, grid, **kwargs):
    grid = self.grids[grid]
    # Extend the sn2, dm2 arrays to allow for a final 'bin'
    xs = numpy.hstack((self.sn2s, [self.limits[0][1]]))
    ys = numpy.hstack((self.dm2s, [self.limits[1][1]]))
    return plt.pcolormesh(xs, ys, grid.T, **kwargs)

  def interpolate_grid(self, grid, newX, newY):
    """Interpolate an FC grid to match the x, y coordinates of another"""
    gridvalue = RectBivariateSpline(self.sn2s, self.dm2s, self.grids[grid])
    grid = numpy.zeros((len(newX), len(newY)))
    for i, x in enumerate(newX):
      for j, y in enumerate(newY):
        grid[i,j] = gridvalue(x, y)
    return grid

  def contour(self, gridCode, likesurf, likeX, likeY, **kwargs):
    """Apply the FC grid data to a likelihood surface and draw the contour"""
    assert likesurf.ndim == 2
    # Build a grid with the same data points as the likelihood surface
    grid = self.interpolate_grid(gridCode, likeX, likeY)
    # Draw a contour plot at z == 0
    return plt.contour(likeX, likeY, (likesurf-grid).T, [0], **kwargs)
    