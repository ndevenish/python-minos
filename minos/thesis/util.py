# coding: utf-8

import math
import numpy
import scipy.stats

def poisson_intervals(mu):
  """Calculate the central poisson intervals for a set of mus"""
  mu = numpy.asarray(mu)
  limits = []
  for val in mu:
    if val == 0:
      limits.append((0,0))
      continue
    if val > 25:
      limits.append((val-math.sqrt(val), val+math.sqrt(val)))
      continue
    pois = scipy.stats.poisson(val)
    # Determine the most likely value
    interval = int(math.floor(val))
    interval = {interval} if pois.pmf(interval) > pois.pmf(interval+1) else {interval+1}
    while sum(pois.pmf(x) for x in interval) < 0.68:
      # Choose the next interval to include
      lower = pois.pmf(min(interval) - 1)
      upper = pois.pmf(max(interval) + 1)
      if lower >= upper:
        interval.add(min(interval)-1)
      if upper >= lower:
        interval.add(max(interval)+1)
    limits.append((min(interval), max(interval)))
  return limits