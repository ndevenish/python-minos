# coding: utf-8

# from collections import namedtuple
from enum import IntEnum, Enum

from minos.operatuple import operatable_namedtuple as namedtuple

ChargeSignTuple = namedtuple("ChargeSignTuple", ["nq", "pq"])
ChargeSign = namedtuple("ChargeSign", ["nq", "pq"])
OscillationParameters = namedtuple("OscillationParameters", ["dm2", "sn2"])
NeutrinoSign = namedtuple("NeutrinoSign", ["nu", "bar"])
Detectorset = namedtuple("Detectorset", ["near", "far", "tau"])
Detectors = namedtuple("Detectors", ["near", "far"])
HornCurrent = namedtuple("HornCurrent", ["fhc","rhc"])

SystematicInformation = namedtuple("SystematicInformation", ["enum", "name", "function", "mode"])

class Detector(IntEnum):
  near = 1
  far = 2

class Current(Enum):
  FHC = "fhc"
  RHC = "rhc"

class Charge(Enum):
  NQ = -1
  PQ =  1