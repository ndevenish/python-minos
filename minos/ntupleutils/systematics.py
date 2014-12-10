# coding: utf-8

from itertools import chain
from .structs import SystematicInformation
from .pyroot import NuSystematic, SystematicMap

# Map of systematic information and required variables to systematic function name.
# Generated by nusyst_members.py --python
_systematic_data = {'kRockZA': SystematicInformation(enum='kRockZA', name='RockZA', function='RockZAShift', mode='kSigma'), 'kNuMuBarXSecDISMultip2': SystematicInformation(enum='kNuMuBarXSecDISMultip2', name='NuMuBarXSecDISMultip2', function='NeugenXSecShift', mode='kAsIs'), 'kEnergyResolutionShowerNear': SystematicInformation(enum='kEnergyResolutionShowerNear', name='EnergyResolutionShowerNear', function='EnergyResolutionShower', mode='kMinusPlus'), 'kNuMuBarXSecSum': SystematicInformation(enum='kNuMuBarXSecSum', name='NuMuBarXSecSum', function='NuMuBarSumXSecShift', mode='kSigma'), 'kRockSelection': SystematicInformation(enum='kRockSelection', name='RockSelection', function='RockSelectionShift', mode='kSigma'), 'kNormalisationBoth': SystematicInformation(enum='kNormalisationBoth', name='NormalisationBoth', function='NormalisationShift', mode='kMinusPlus'), 'kCombinedXSecOverall': SystematicInformation(enum='kCombinedXSecOverall', name='CombinedXSecOverall', function='OverallXSecShift', mode='kMinusPlus'), 'kNDCoilHole': SystematicInformation(enum='kNDCoilHole', name='NDCoilHole', function='NDCoilHole', mode='kMinusPlus'), 'kNuMuBarXSecCCMA': SystematicInformation(enum='kNuMuBarXSecCCMA', name='NuMuBarXSecCCMA', function='NeugenXSecShift', mode='kMinusPlus'), 'kCombinedXSecDISMultip3': SystematicInformation(enum='kCombinedXSecDISMultip3', name='CombinedXSecDISMultip3', function='NeugenXSecShift', mode='kAsIs'), 'kBFieldBoth': SystematicInformation(enum='kBFieldBoth', name='BFieldBoth', function='BFieldShift', mode='kMinusPlus'), 'kCombinedXSecDISMultip2': SystematicInformation(enum='kCombinedXSecDISMultip2', name='CombinedXSecDISMultip2', function='NeugenXSecShift', mode='kAsIs'), 'kEnergyResolutionShowerBoth': SystematicInformation(enum='kEnergyResolutionShowerBoth', name='EnergyResolutionShowerBoth', function='EnergyResolutionShower', mode='kMinusPlus'), 'kTrackEnergyScale': SystematicInformation(enum='kTrackEnergyScale', name='TrackEnergyScale', function='TrackEnergyScale', mode='kMinusPlus'), 'kRelativeHadronicCalibrationSterile': SystematicInformation(enum='kRelativeHadronicCalibrationSterile', name='RelativeHadronicCalibrationSterile', function='RelativeHadronicCalibrationSterile', mode='kMinusPlus'), 'kCombinedXSecCCMA': SystematicInformation(enum='kCombinedXSecCCMA', name='CombinedXSecCCMA', function='NeugenXSecShift', mode='kMinusPlus'), 'kShowerEnergyScale': SystematicInformation(enum='kShowerEnergyScale', name='ShowerEnergyScaleBoth', function='ShowerEnergyScale', mode='kMinusPlus'), 'kEnergyResolutionTrackCurveNear': SystematicInformation(enum='kEnergyResolutionTrackCurveNear', name='EnergyResolutionTrackCurveNear', function='EnergyResolutionTrackCurve', mode='kMinusPlus'), 'kFDCleaningSterile': SystematicInformation(enum='kFDCleaningSterile', name='FDCleaningSterile', function='FDCleaningShiftSterile', mode='kSigma'), 'kHornCurrent': SystematicInformation(enum='kHornCurrent', name='HornCurrent', function='HornCurrentShift', mode='kSigma'), 'kEnergyResolutionEventBoth': SystematicInformation(enum='kEnergyResolutionEventBoth', name='EnergyResolutionEventBoth', function='EnergyResolutionEvent', mode='kMinusPlus'), 'kShowerEnergyScaleNear': SystematicInformation(enum='kShowerEnergyScaleNear', name='ShowerEnergyScaleNear', function='ShowerEnergyScale', mode='kMinusPlus'), 'kWSNuBarBackground': SystematicInformation(enum='kWSNuBarBackground', name='WSNuBarBackground', function='WSNuBarBackgroundShift', mode='kMinusPlus'), 'kEnergyResolutionEventNear': SystematicInformation(enum='kEnergyResolutionEventNear', name='EnergyResolutionEventNear', function='EnergyResolutionEvent', mode='kMinusPlus'), 'kTargetHole': SystematicInformation(enum='kTargetHole', name='TargetHole', function='TargetHoleShift', mode='kAsIs'), 'kShowerEnergyOffset': SystematicInformation(enum='kShowerEnergyOffset', name='ShowerEnergyOffset', function='ShowerEnergyOffset', mode='kAsIs'), 'kShowerEnergyFunction': SystematicInformation(enum='kShowerEnergyFunction', name='ShowerEnergyScaleFunctionBoth', function='ShowerEnergyFunction', mode='kSigma'), 'kJitterVDPID': SystematicInformation(enum='kJitterVDPID', name='JitterVDPID', function='JitterVDPIDShift', mode='kSigma'), 'kRockXSec': SystematicInformation(enum='kRockXSec', name='RockXSec', function='RockXSecShift', mode='kSigma'), 'kNormalisationNear': SystematicInformation(enum='kNormalisationNear', name='NormalisationNear', function='NormalisationShift', mode='kMinusPlus'), 'kTauQELRes': SystematicInformation(enum='kTauQELRes', name='TauQELRes', function='TauQELResShift', mode='kMinusPlus'), 'kEnergyResolutionTrackRangeBoth': SystematicInformation(enum='kEnergyResolutionTrackRangeBoth', name='EnergyResolutionTrackRangeBoth', function='EnergyResolutionTrackRange', mode='kMinusPlus'), 'kBeam': SystematicInformation(enum='kBeam', name='Flux', function='BeamShift', mode='kSigma'), 'kNormalisationFar': SystematicInformation(enum='kNormalisationFar', name='NormalisationFar', function='NormalisationShift', mode='kMinusPlus'), 'kNuMuBarXSecOverall': SystematicInformation(enum='kNuMuBarXSecOverall', name='NuMuBarXSecOverall', function='OverallXSecShift', mode='kMinusPlus'), 'kFDCleaning': SystematicInformation(enum='kFDCleaning', name='FDCleaning', function='FDCleaningShift', mode='kSigma'), 'kAbsoluteHadronicCalibrationSterile': SystematicInformation(enum='kAbsoluteHadronicCalibrationSterile', name='AbsoluteHadronicCalibrationSterile', function='AbsoluteHadronicCalibrationSterile', mode='kSigma'), 'kShowerEnergyScaleFar': SystematicInformation(enum='kShowerEnergyScaleFar', name='ShowerEnergyScaleFar', function='ShowerEnergyScale', mode='kMinusPlus'), 'kBFieldFar': SystematicInformation(enum='kBFieldFar', name='BFieldFar', function='BFieldShift', mode='kMinusPlus'), 'kShowerEnergyScaleRelative': SystematicInformation(enum='kShowerEnergyScaleRelative', name='ShowerEnergyScaleRelative', function='ShowerEnergyScale', mode='kMinusPlus'), 'kCombinedXSecMaQE': SystematicInformation(enum='kCombinedXSecMaQE', name='CombinedXSecMaQE', function='NeugenXSecShift', mode='kMinusPlus'), 'kNDCleaningSterile': SystematicInformation(enum='kNDCleaningSterile', name='NDCleaningSterile', function='NDCleaningShiftSterile', mode='kSigma'), 'kEnergyResolutionTrackCurveBoth': SystematicInformation(enum='kEnergyResolutionTrackCurveBoth', name='EnergyResolutionTrackCurveBoth', function='EnergyResolutionTrackCurve', mode='kMinusPlus'), 'kEnergyResolutionTrackRangeNear': SystematicInformation(enum='kEnergyResolutionTrackRangeNear', name='EnergyResolutionTrackRangeNear', function='EnergyResolutionTrackRange', mode='kMinusPlus'), 'kNuMuBarXSecQEL': SystematicInformation(enum='kNuMuBarXSecQEL', name='NuMuBarXSecQEL', function='NuMuBarQELXSecShift', mode='kMinusPlus'), 'kTrackEnergyOverall': SystematicInformation(enum='kTrackEnergyOverall', name='TrackEnergyOverall', function='TrackEnergyOverall', mode='kSigma'), 'kTrackEnergyRange': SystematicInformation(enum='kTrackEnergyRange', name='TrackEnergyRange', function='TrackEnergyScale', mode='kMinusPlus'), 'kTrackEnergyOffset': SystematicInformation(enum='kTrackEnergyOffset', name='TrackEnergyOffset', function='TrackEnergyOffset', mode='kAsIs'), 'kAcceptance': SystematicInformation(enum='kAcceptance', name='Acceptance', function='AcceptanceShift', mode='kSigma'), 'kTrackEnergyCurvatureBoth': SystematicInformation(enum='kTrackEnergyCurvatureBoth', name='TrackEnergyCurvatureBoth', function='TrackEnergyScale', mode='kMinusPlus'), 'kCCWSBackground': SystematicInformation(enum='kCCWSBackground', name='CCWSBackground', function='CCWSBackground', mode='kMinusPlus'), 'kCombinedXSecMaRes': SystematicInformation(enum='kCombinedXSecMaRes', name='CombinedXSecMaRes', function='NeugenXSecShift', mode='kMinusPlus'), 'kFDCleaningCosmicsSterile': SystematicInformation(enum='kFDCleaningCosmicsSterile', name='FDCleaningCosmicsSterile', function='FDCleaningCosmicsShiftSterile', mode='kSigma'), 'kScraping': SystematicInformation(enum='kScraping', name='DecayPipe', function='ScrapingShift', mode='kMinusPlus'), 'kNuMuBarXSecRes': SystematicInformation(enum='kNuMuBarXSecRes', name='NuMuBarXSecRes', function='NuMuBarResXSecShift', mode='kMinusPlus'), 'kBFieldNear': SystematicInformation(enum='kBFieldNear', name='BFieldNear', function='BFieldShift', mode='kMinusPlus'), 'kNCNuBarBackground': SystematicInformation(enum='kNCNuBarBackground', name='NCNuBarBackground', function='NCNuBarBackgroundShift', mode='kMinusPlus'), 'kCCBackgroundSterile': SystematicInformation(enum='kCCBackgroundSterile', name='CCBackgroundSterile', function='CCBackgroundShiftSterile', mode='kMinusPlus'), 'kNCBackground': SystematicInformation(enum='kNCBackground', name='NCBackground', function='NCBackgroundShift', mode='kMinusPlus'), 'kNormalisationSterile': SystematicInformation(enum='kNormalisationSterile', name='NormalisationSterile', function='NormalisationShiftSterile', mode='kMinusPlus'), 'kTrackEnergyCurvatureFar': SystematicInformation(enum='kTrackEnergyCurvatureFar', name='TrackEnergyCurvatureFar', function='TrackEnergyScale', mode='kMinusPlus'), 'kNDCleaning': SystematicInformation(enum='kNDCleaning', name='NDCleaning', function='NDCleaningShift', mode='kSigma'), 'kNormalisationNC': SystematicInformation(enum='kNormalisationNC', name='NormalisationNC', function='NormalisationShift', mode='kMinusPlus'), 'kAllBackgroundsScaleBoth': SystematicInformation(enum='kAllBackgroundsScaleBoth', name='AllBackgroundsScaleBoth', function='AllBackgroundsScaleBothShift', mode='kMinusPlus'), 'kCCBackground': SystematicInformation(enum='kCCBackground', name='CCBackground', function='CCBackgroundShift', mode='kMinusPlus'), 'kTrackEnergyNeutrinoQE': SystematicInformation(enum='kTrackEnergyNeutrinoQE', name='TrackEnergyNeutrinoQE', function='TrackEnergyNeutrinoQE', mode='kAsIs'), 'kFDCleaningCosmics': SystematicInformation(enum='kFDCleaningCosmics', name='FDCleaningCosmics', function='FDCleaningCosmicsShift', mode='kSigma')}
_systematic_variables = {'NuMuBarSumXSecShift': set(['inu', 'rw', 'iaction', 'neuEnMC']), 'FDCleaningCosmicsShift': set(['detector', 'rw', 'energyNC']), 'NCNuBarBackgroundShift': set(['rw', 'iaction']), 'NDCleaningShift': set(['detector', 'rw', 'energyNC']), 'NormalisationShiftSterile': set(['detector', 'rw', 'simFlag']), 'EnergyResolutionShower': set(['energy', 'shwEn', 'shwEnMC', 'trkEn', 'nshw', 'detector']), 'AllBackgroundsScaleBothShift': set(['inu', 'charge', 'rw', 'iaction']), 'TrackEnergyOverall': set(['trkEnRange', 'energy', 'shwEn', 'trkEnCurv', 'trkEn', 'usedCurv', 'usedRange']), 'NuMuBarQELXSecShift': set(['inu', 'rw', 'iaction', 'iresonance']), 'FDCleaningShiftSterile': set(['shwEnLinNCCor', 'detector', 'rw', 'simFlag']), 'NCBackgroundShift': set(['rw', 'iaction']), 'TauQELResShift': set(['inu', 'rw', 'iaction', 'iresonance']), 'JitterVDPIDShift': set(['jitter', 'dpID']), 'BFieldShift': set(['inu', 'charge', 'rw', 'iaction', 'detector']), 'EnergyResolutionTrackCurve': set(['trkEn', 'energy', 'trkEnMC', 'shwEn', 'ntrk', 'trkEnCurv', 'detector', 'usedCurv']), 'TrackEnergyOffset': set(['shwEn', 'trkEn', 'energy']), 'AcceptanceShift': set(['detector', 'rw', 'energy']), 'AbsoluteHadronicCalibrationSterile': set(['shwEnLinNCCor', 'shwEnCC', 'shwEnMC', 'simFlag']), 'NeugenXSecShift': set(['releaseType', 'rw', 'iaction', 'iresonance']), 'TrackEnergyScale': set(['shwEn', 'trkEn', 'detector', 'energy', 'usedRange']), 'RelativeHadronicCalibrationSterile': set(['shwEnLinNCCor', 'shwEnCC', 'detector', 'simFlag']), 'BeamShift': set(['fluxErr', 'rw']), 'SetShiftedNeugenParameters': set(['inu']), 'TargetHoleShift': set(['rw', 'ppvz']), 'CCBackgroundShift': set(['rw', 'iaction']), 'CreateMCEventInfo': set(['initialStateMC', 'tgtPxMC', 'neuEnMC', 'tgtPyMC', 'inu', 'hadronicFinalStateMC', 'tgtPzMC', 'q2MC', 'neuPxMC', 'yMC', 'tgtEnMC', 'iaction', 'neuPzMC', 'nucleusMC', 'iresonance', 'xMC', 'neuPyMC', 'w2MC']), 'NDCoilHole': set(['shwEn', 'trkEn', 'detector', 'energy']), 'OverallXSecShift': set(['inu', 'rw', 'iaction']), 'Shift': set([]), 'HornCurrentShift': set(['detector', 'rw', 'energy']), 'ShowerEnergyOffset': set(['shwEn', 'trkEn', 'energy']), 'FDCleaningShift': set(['detector', 'rw', 'energyNC']), 'RockZAShift': set(['detector', 'rw', 'run']), 'NDCleaningShiftSterile': set(['shwEnLinNCCor', 'detector', 'rw', 'simFlag']), 'NuMuBarResXSecShift': set(['inu', 'rw', 'iaction', 'iresonance']), 'NormalisationShift': set(['detector', 'rw', 'run']), 'TrackEnergyNeutrinoQE': set(['iresonance', 'energy', 'shwEn', 'charge', 'simFlag', 'inu', 'trkEn']), 'WSNuBarBackgroundShift': set(['inu', 'charge', 'rw', 'iaction']), 'EnergyResolutionEvent': set(['energy', 'detector', 'neuEnMC']), 'EnergyResolutionTrackRange': set(['trkEnRange', 'energy', 'trkEnMC', 'shwEn', 'ntrk', 'trkEn', 'detector', 'usedRange']), 'TFProbShift': set(['prob']), 'ShowerEnergyScale': set(['shwEn', 'trkEn', 'detector', 'energy']), 'RockXSecShift': set(['iresonance', 'detector', 'rw', 'run', 'zMC']), 'CCBackgroundShiftSterile': set(['iaction', 'rw', 'simFlag', 'inu']), 'ScrapingShift': set(['rw', 'ppvz', 'ptype']), 'CCWSBackground': set(['qp', 'rw', 'inu']), 'RockSelectionShift': set(['regionTrkVtx', 'run', 'index', 'stripHoveNumTrkVtx', 'edgeRegionTrkVtx', 'stripHoveNumTrkVtxNoShift']), 'ShowerEnergyFunction': set(['shwEn', 'trkEn', 'energy']), 'FDCleaningCosmicsShiftSterile': set(['shwEnLinNCCor', 'detector', 'rw', 'simFlag'])}
# #######################################

def systematic_variable_requirements(systematics):
  """Returns a set of NuEvent variables required by the specified systematics."""
  systematics = set(systematics)

  def _extract_enum_name(name):
    names = [x for x, y in _systematic_data.items() if y.name == name]
    assert len(names) <= 1
    if not names:
      raise KeyError("No systematic lookup entry found for name: " + name)
    return names[0]  
  enum_names = set([_extract_enum_name(x) for x in systematics])
  return set(chain(*[_systematic_variables[_systematic_data[x].function] for x in enum_names]))

class Applicator(object):
  def __init__(self, shifts={}):
    self._systematics = NuSystematic()
    self.set_shifts(shifts)

  def set_shifts(self, shifts):
    # Validate these are all known names
    assert all(x in {y.name for y in _systematic_data.values()} for x in shifts.keys())

    shiftCopy = dict(shifts)
    # This looks strange, but matches bad logic in NuSystematics::SystFromName
    for norm in [x for x in shifts.keys() if x.startswith("Normalisation")]:
      shiftCopy[norm.lower()] = shiftCopy[norm]
      del shiftCopy[norm]

    mapp = SystematicMap()
    for name, val in shiftCopy.items():
      mapp[name] = val
    self._systematics.SetShiftsAsSigmas(mapp)
    self._shifts = shifts

  def set_nubar_cutter(self, cut):
    self._systematics.SetNuBarSelector(cut)

  def shift(self, event):
    """Apply the set of systematic shifts to a NuFCEvent object"""
    self._systematics.Shift(event)
