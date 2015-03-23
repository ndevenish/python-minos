# coding: utf-8

import logging
logger = logging.getLogger(__name__)

import tables
import numpy

import minos.ntupleutils as ntu
from minos.ntupleutils import ChargeSignTuple, PotArray

from ROOT import NuOscProbCalc

def oscillate_table(table, pars):
  """Applies oscillation parameters to a table of events"""

  # numpy.in1d(events.far.pq["inu"], [-14, -16, 14, 16])
  # events.far.pq["iaction"] == 1

  for row in table:
    # Only CC interactions oscillate
    if row["iaction"] == 0:
      continue
    # Don't oscillate non mu/tau (e.g. electron interactions)
    if not row["inu"] in (-14, -16, 14, 16):
      continue
    # Remove events that turned from nue->nutau
    if abs(row["inunoosc"]) == 12 and abs(row["inu"]) == 16:
      row["rw"] = 0.0
      continue

    #nu.rw *= this->OscillationWeight(nu.neuEnMC,nu.inu,xmlConfig);
    dm2, sn2 = (pars["dm2"], pars["sn2"]) if row["inu"] > 0 else (pars["dm2bar"], pars["sn2bar"])
    prob = NuOscProbCalc.OscillationWeight(row["neuEnMC"], dm2, sn2)
    inu = abs(row["inu"])
    if inu == 14:
      row["rw"] *= prob
    elif inu == 16:
      row["rw"] *= (1-prob)

def load_and_oscillate_events(data, POT, oscillation_pars=None, nu=True, nubar=True):
  """Load and oscillate reduced event files.
  data: A dataset object
  """
  data_filenames = ntu.Detectorset(near=data.near.hdf5.only, far=data.far.hdf5.only, tau=data.tau.hdf5.only)
  logger.info("Reading data files:\n{}".format("\n".join("  "+x for x in data_filenames)))
  event_files = ntu.mapTuples(lambda x: tables.open_file(x), [data_filenames])

  # Leave the near POT, and set the far POT
  POT = ntu.Detectorset(event_files.near.root.FCTree2.attrs.POT, POT, POT)

  # Scale the far and Tau files to match the desired POT, and thus each other
  tau_scale = POT.far / event_files.tau.root.FCTree2.attrs.POT
  far_scale = POT.far / event_files.far.root.FCTree2.attrs.POT
  
  # Load the actual events structure tables, then separate into charge samples
  events = ntu.mapTuples(lambda x: x.root.FCTree2.read().view(ntu.PotArray), [event_files])
  # Close the event files now we have read everything
  for eventFile in event_files:
    eventFile.close()

  # Detectorset._make([x.root.FCTree2.read().view(PotArray) for x in event_files])

  # Scale and set the POT
  events.near.pot = POT.near
  events.far.pot = POT.far
  events.tau.pot = POT.tau
  events.tau["rw"] *= tau_scale
  events.far["rw"] *= far_scale
  events = ntu.Detectorset._make(ChargeSignTuple(pq=x[x["charge"]==1],nq=x[x["charge"]==-1]) for x in events)
  
  logger.info("Read and scaled event files")

  nuPart = None
  barPart = None
  # Apply the oscillation probability to every event
  if oscillation_pars:
    logger.info("Calculating oscillation weights for events")
    if nu:
      oscillate_table(events.far.nq, oscillation_pars)
      oscillate_table(events.tau.nq, oscillation_pars)
      nuPart = numpy.hstack([events.far.nq,events.tau.nq]).view(PotArray)
    if nubar:
      oscillate_table(events.far.pq, oscillation_pars)
      oscillate_table(events.tau.pq, oscillation_pars)
      barPart = numpy.hstack([events.far.pq,events.tau.pq]).view(PotArray)
  else:
    # No tau events as not oscillating
    if nu:
      nuPart = numpy.hstack([events.far.nq]).view(PotArray)
    if nubar:
      barPart = numpy.hstack([events.far.pq]).view(PotArray)
  farEvents = ChargeSignTuple(nq=nuPart,pq=barPart)

  if nu:
    farEvents.nq.pot = POT.far
  if nubar:
    farEvents.pq.pot = POT.far
  # Return with far and tau joined together
  return ntu.Detectors(near=events.near,
                   far=farEvents)
