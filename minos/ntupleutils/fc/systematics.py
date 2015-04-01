# coding: utf-8

import random

import numpy

import minos.ntupleutils as ntu

class SystematicShifts(dict):
  def __init__(self, data=None):
    assert all(x in Systematics.SUPPORTED for x in data.keys())
    super(SystematicShifts,self).__init__(data)

  def for_nusystematics(self):
    "Converts the dictionary into values suitable for NuSystematics shifting"
    sigs = dict(self)
    sigs["DecayPipe"] = 2*(systematics["DecayPipe"]-1)
    for name in set(systematics.keys()) - {"DecayPipe", "ShowerEnergyScaleFunctionBoth", "Flux"}:
      sigs[name] = (sigs[name]-1)/(SHIFT_VALUES[name]-1)
    return sigs

class ThesisSystematics(object):
  # The actual shift values to use
  SHIFT_VALUES = {
    "TrackEnergyRange": 1.02,
    "TrackEnergyCurvatureBoth": 1.03,
    "ShowerEnergyScaleNear": 1.02,
    "ShowerEnergyScaleFar": 1.01,
    "AllBackgroundsScaleBoth": 1.5,
    "NormalisationFar": 1.0154,
    "CombinedXSecOverall": 1.035,
    "DecayPipe": (0.0, 1.5),
    "ShowerEnergyScaleFunctionBoth": (-1.0,1.0),
    "Flux": (-1.0,1.0),
  }
  # The ranges of each shift value, for random generation
  SHIFT_RANGES = {s: x if isinstance(x, tuple) else ((-1*(x-1)+1, x)) for s, x in SHIFT_VALUES.items()}

  # A set of shifts with NO shifts
  NO_SHIFTS = {
    "TrackEnergyRange": 1,
    "TrackEnergyCurvatureBoth": 1,
    "ShowerEnergyScaleNear": 1,
    "ShowerEnergyScaleFar": 1,
    "AllBackgroundsScaleBoth": 1,
    "NormalisationFar": 1,
    "CombinedXSecOverall": 1,
    "DecayPipe": 1, 
    "ShowerEnergyScaleFunctionBoth": 0,
    "Flux": 0,
  }

  @classmethod
  def random_shifts(cls):
    return SystematicShifts({s: random.uniform(*x) for s, x in cls.SHIFT_RANGES.items()})


class Systematics(object):
  """Accepts a set of events, and applies shifts to them on demand"""

  SUPPORTED = {"TrackEnergyRange", "TrackEnergyCurvatureBoth", "ShowerEnergyScaleFunctionBoth",
               "ShowerEnergyScaleFar", "ShowerEnergyScaleNear", "NormalisationFar", "DecayPipe",
               "AllBackgroundsScaleBoth", "Flux", "CombinedXSecOverall"}
  def __init__(self, events):
    #self.events = events
    # self.max_shifts = maximum_shifts
    # Work out the detector of this sample (disallow mixed)
    self.pot = events.pot
    self.detector = ntu.Detector(events[0]["detector"])
    assert numpy.all(events["detector"] == self.detector)

    # Precalculate the various masks
    self.usedRange = events["usedRange"] == 1
    self.inDecayPipe = numpy.logical_and(events["ppvz"]>4500, numpy.abs(events["ptype"]) != 13)
    self.isBackground = numpy.logical_and(numpy.logical_or(events["iaction"] == 0, events["inu"] == 14), events["charge"]==1)
    self.isCC = events["iaction"] == 1

    # All selections are done precalculated, so only use the very minimal of
    # run-time storage
    self.fluxErr = events["fluxErr"]
    self.reduced_events = events[["trkEn", "shwEn", "rw"]]
    self.binning = ntu.binningscheme4()

  def shift(self, shifts):
    events = self.reduced_events.copy()
    self.shift_track_energy(events, shifts["TrackEnergyRange"], shifts["TrackEnergyCurvatureBoth"])
    self.shift_shower_energy(events, shifts["ShowerEnergyScaleFunctionBoth"], shifts["ShowerEnergyScaleFar"], shifts["ShowerEnergyScaleNear"])
    self.shift_normalisation(events, shifts["NormalisationFar"])
    self.shift_decaypipe(events, shifts["DecayPipe"])
    self.shift_background(events, shifts["AllBackgroundsScaleBoth"])
    self.shift_beam(events, shifts["Flux"])
    self.shift_crosssection(events, shifts["CombinedXSecOverall"])
    return events

  def unshifted_histogram(self):
    events = self.reduced_events.copy()
    hist, _ = numpy.histogram(events["trkEn"]+events["shwEn"], self.binning, weights=events["rw"])
    # hist = hist.view(ntu.Spectrum)
    hist = ntu.Spectrum(self.binning, data=hist, pot=self.pot)
    return hist

  def shifted_histogram(self, shifts):
    """Generate a set of shifts and returns a histogram"""
    events = self.shift(shifts)
    hist, _ = numpy.histogram(events["trkEn"]+events["shwEn"], self.binning, weights=events["rw"])
    # hist = hist.view(ntu.Spectrum)
    hist = ntu.Spectrum(self.binning, data=hist, pot=self.pot)
    return hist

  def _shower_energy_function(self, events, shiftVal):
    offset = 6.6
    scale = 3.5
    eLife = 1.44
    shwEn = events["shwEn"]
    shift = 1 + shiftVal*0.01*(offset+scale*numpy.exp(-1*(shwEn/eLife))) 
    shwEn *= shift

  def shift_track_energy(self, events, shift_range, shift_curvature):
    numpy.place(events["trkEn"], self.usedRange,  events[self.usedRange]["trkEn"]*shift_range)
    numpy.place(events["trkEn"], ~self.usedRange, events[~self.usedRange]["trkEn"]*shift_curvature)

  def shift_shower_energy(self, events, shiftBoth, shiftFar, shiftNear):
    self._shower_energy_function(events, shiftBoth)
    if self.detector == ntu.Detector.far:
      events["shwEn"] *= shiftFar
    else:
      events["shwEn"] *= shiftNear

  def shift_normalisation(self, events, shift):
    if self.detector == ntu.Detector.far:
      events["rw"] *= shift

  def shift_decaypipe(self, events, shift):
    numpy.place(events["rw"], self.inDecayPipe, events[self.inDecayPipe]["rw"] * shift)

  def shift_background(self, events, shift):
    numpy.place(events["rw"], self.isBackground, events[self.isBackground]["rw"] * shift)

  def shift_crosssection(self, events, shift):
    numpy.place(events["rw"], self.isCC, events[self.isCC]["rw"]*shift)

  def shift_beam(self, events, shift):
    events["rw"] *= 1 + (shift * (self.fluxErr-1))
