# coding: utf-8

from collections import namedtuple

ChargeSignTuple = namedtuple("ChargeSignTuple", ["nq", "pq"])
OscillationParameters = namedtuple("OscillationParameters", ["dm2", "sn2"])
NeutrinoSign = namedtuple("NeutrinoSign", ["nu", "bar"])
Detectorset = namedtuple("Detectorset", ["near", "far", "tau"])
Detectors = namedtuple("Detectors", ["near", "far"])
HornCurrent = namedtuple("HornCurrent", ["fhc","rhc"])

SystematicInformation = namedtuple("SystematicInformation", ["enum", "name", "function", "mode"])

