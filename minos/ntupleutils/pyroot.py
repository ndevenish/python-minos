# coding: utf-8

import ROOT
from ROOT import TString

import logging
logger = logging.getLogger(__name__)
import rootpy
from minos.rootmagic import suppress

import pdb
pdb.set_trace()

QUICKLOAD_SUCCESS = None
with suppress():
  # Attempt to load on it's own - if it does work, then we are either fully
  # dependency-realised, or using the reduced ntupleutils
  QUICKLOAD_SUCCESS = ROOT.gSystem.Load("libNtupleUtils.so") >= 0

if QUICKLOAD_SUCCESS:
  logger.debug("Successfully loaded Ntupleutils directly")

# Load the normal dependencies only if this failed
if not QUICKLOAD_SUCCESS:
  ROOT.gSystem.Load("libCore.so")
  ROOT.gSystem.Load("libRIO.so")
  ROOT.gSystem.Load("libEG.so")
  ROOT.gSystem.Load("libPhysics.so")
  ROOT.gSystem.Load("libNet.so")
  ROOT.gSystem.Load("libGeom.so")
  ROOT.gSystem.Load("libTree.so")
  ROOT.gSystem.Load("libGui.so")
  ROOT.gSystem.Load("libMinuit2.so")

  ROOT.gSystem.Load("libMessageService.so")
  ROOT.gSystem.Load("libConventions.so")
  ROOT.gSystem.Load("libValidity.so")

  ROOT.gSystem.Load("libUtility.so")
  ROOT.gSystem.Load("libRegistry.so")
  ROOT.gSystem.Load("libConfigurable.so")
  ROOT.gSystem.Load("libRecord.so")
  ROOT.gSystem.Load("libDatabaseInterface.so")

  ROOT.gSystem.Load("libDynamicFactory.so")
  ROOT.gSystem.Load("libAlgorithm.so")

  ROOT.gSystem.Load("libMinosObjectMap.so")

  ROOT.gSystem.Load("libRint.so")
  ROOT.gSystem.Load("libJobControl.so")
  ROOT.gSystem.Load("libOnlineUtil.so")
  ROOT.gSystem.Load("libRawData.so")
  ROOT.gSystem.Load("libCandidate.so")
  ROOT.gSystem.Load("libCandData.so")

  ROOT.gSystem.Load("libPlex.so")
  ROOT.gSystem.Load("libFabrication.so")

  ROOT.gSystem.Load("libREROOT_Classes.so")
  ROOT.gSystem.Load("libDigitization.so")
  ROOT.gSystem.Load("libLattice.so")
  ROOT.gSystem.Load("libNavigation.so")
  ROOT.gSystem.Load("libMINF_Classes.so")
  ROOT.gSystem.Load("libCandNtupleSR.so")
  ROOT.gSystem.Load("libBeamDataNtuple.so")
  ROOT.gSystem.Load("libMCNtuple.so")
  ROOT.gSystem.Load("libTruthHelperNtuple.so")
  ROOT.gSystem.Load("libStandardNtuple.so")

  ROOT.gSystem.Load("libUgliGeometry.so")
  ROOT.gSystem.Load("libGeoGeometry.so")

  ROOT.gSystem.Load("libCalibrator.so")
  ROOT.gSystem.Load("libPulserCalibration.so")
  ROOT.gSystem.Load("libCandDigit.so")

  ROOT.gSystem.Load("libRerootExodus.so")

  ROOT.gSystem.Load("libNtupleUtils.so")


# Even if it succeeded, we may need to load more libraries, but
# if we did succeed, load them quietly as they might not all be available
_post_library_libs = ("libOscProb.so", "libRecoBase.so", "libDataUtil.so",
                      "libXMLParser.so", "libMCReweight.so", "libNeugenInterface.so",
                      "libDcsUser.so")
if QUICKLOAD_SUCCESS:
  with suppress():
    for lib in _post_library_libs:
      ROOT.gSystem.Load(lib)
else:
  for lib in _post_library_libs:
      ROOT.gSystem.Load(lib)

import pdb
pdb.set_trace()

from ROOT import (MajCInfo, MajorityCurvature, NuCounter, NuCuts,
                  NuDemoModule, NuEvent, NuExtraction, NuFluctuator,
                  NuFluggChain, NuFluxChain, NuFluxHelper, NuGeneral, 
                  NuGnumiChain, NuHistos, NuHistInterpolator, NuHistSmoother, 
                  NuInputEvents, NuLibrary, NuXMLConfig, NuMatrixFitter, 
                  NuMatrixInput, NuMatrixMethod, NuMatrixOutput, NuMatrixSpectrum, 
                  NuMIPP, NuMMHelper, NuMMHelperPRL, NuMMHelperPRLPQ, NuMMHelperCPT, 
                  NuMMHelperCPTpair, NuMMHelperNoChargeCut, NuMMParameters, 
                  NuMMRun, NuMMRunCCTutorial, NuMMRunCC2010, NuMMRunCC2010New, 
                  NuMMRunNC2010, NuMMRunNuBar, NuMMRunCPT, NuMMRunCPTSyst, 
                  NuMMRunPRL, NuMMRunFC, NuMMRunFCNSINubar, NuMMRunFCNSINu, 
                  NuMMRunNDOsc, NuMMRunNSI, NuMMRunNSINu, NuMMRunNSINubar, 
                  NuMMRunNSINu, NuMMRunTransition, NuMMRunTransSME, 
                  NuMMRunNoChargeCut, NuMMRunTemplates, NuMMRunLED, NuFCEvent, 
                  NuMCEvent, NuReco, NuShiftableSpectrum, NuShiftableBinnedSpectrum, 
                  NuShiftableUnbinnedSpectrum, NuSystematic, NuSystFitter, 
                  NuTreeWrapper, NuUtilities, NuZBeamReweight, SRMom, HoughTransNCPi0, 
                  NuTH2Interpolator, NuFCGridPoint, NuFCGridPointNSINubar, 
                  NuFCGridPointNSINu, NuFCExperiment, NuFCExperimentFactory, 
                  NuFCExperimentFactoryNSI, NuFCFitter, NuFCFitterNSI, 
                  NuFCFitterNSINubar, NuFCFitterNSINu, NuABFitter, NuEZFitter, 
                  NuEZFitterNSI, NuEZRunsFitter, NuFCConfig, NuStatistics, 
                  NuContour, ConfigFile, NuMatrix, NuMatrix1D, NuMatrix2D, 
                  NuMatrixCPT, NuCutter, NuCut, NuParticle)

import pdb
pdb.set_trace()
# __all__ = [ "MajCInfo", "MajorityCurvature", "NuCounter", "NuCuts",
#             "NuDemoModule", "NuEvent", "NuExtraction", "NuFluctuator",
#             "NuFluggChain", "NuFluxChain", "NuFluxHelper", "NuGeneral",
#             "NuGnumiChain", "NuHistos", "NuHistInterpolator", "NuHistSmoother",
#             "NuInputEvents", "NuLibrary", "NuXMLConfig", "NuMatrixFitter",
#             "NuMatrixInput", "NuMatrixMethod", "NuMatrixOutput", "NuMatrixSpectrum",
#             "NuMIPP", "NuMMHelper", "NuMMHelperPRL", "NuMMHelperPRLPQ", "NuMMHelperCPT",
#             "NuMMHelperCPTpair", "NuMMHelperNoChargeCut", "NuMMParameters",
#             "NuMMRun", "NuMMRunCCTutorial", "NuMMRunCC2010", "NuMMRunCC2010New",
#             "NuMMRunNC2010", "NuMMRunNuBar", "NuMMRunCPT", "NuMMRunCPTSyst",
#             "NuMMRunPRL", "NuMMRunFC", "NuMMRunFCNSINubar", "NuMMRunFCNSINu",
#             "NuMMRunNDOsc", "NuMMRunNSI", "NuMMRunNSINu", "NuMMRunNSINubar",
#             "NuMMRunNSINu", "NuMMRunTransition", "NuMMRunTransSME",
#             "NuMMRunNoChargeCut", "NuMMRunTemplates", "NuMMRunLED", "NuFCEvent",
#             "NuMCEvent", "NuReco", "NuShiftableSpectrum", "NuShiftableBinnedSpectrum",
#             "NuShiftableUnbinnedSpectrum", "NuSystematic", "NuSystFitter",
#             "NuTreeWrapper", "NuUtilities", "NuZBeamReweight", "SRMom", "HoughTransNCPi0",
#             "NuTH2Interpolator", "NuFCGridPoint", "NuFCGridPointNSINubar",
#             "NuFCGridPointNSINu", "NuFCExperiment", "NuFCExperimentFactory",
#             "NuFCExperimentFactoryNSI", "NuFCFitter", "NuFCFitterNSI",
#             "NuFCFitterNSINubar", "NuFCFitterNSINu", "NuABFitter", "NuEZFitter",
#             "NuEZFitterNSI", "NuEZRunsFitter", "NuFCConfig", "NuStatistics",
#             "NuContour", "ConfigFile", "NuMatrix", "NuMatrix1D", "NuMatrix2D",
#             "NuMatrixCPT", "NuCutter", "NuCut", "NuParticle"]

_all_ntuples = [ "MajCInfo", "MajorityCurvature", "NuCounter", "NuCuts",
            "NuDemoModule", "NuEvent", "NuExtraction", "NuFluctuator",
            "NuFluggChain", "NuFluxChain", "NuFluxHelper", "NuGeneral",
            "NuGnumiChain", "NuHistos", "NuHistInterpolator", "NuHistSmoother",
            "NuInputEvents", "NuLibrary", "NuXMLConfig", "NuMatrixFitter",
            "NuMatrixInput", "NuMatrixMethod", "NuMatrixOutput", "NuMatrixSpectrum",
            "NuMIPP", "NuMMHelper", "NuMMHelperPRL", "NuMMHelperPRLPQ", "NuMMHelperCPT",
            "NuMMHelperCPTpair", "NuMMHelperNoChargeCut", "NuMMParameters",
            "NuMMRun", "NuMMRunCCTutorial", "NuMMRunCC2010", "NuMMRunCC2010New",
            "NuMMRunNC2010", "NuMMRunNuBar", "NuMMRunCPT", "NuMMRunCPTSyst",
            "NuMMRunPRL", "NuMMRunFC", "NuMMRunFCNSINubar", "NuMMRunFCNSINu",
            "NuMMRunNDOsc", "NuMMRunNSI", "NuMMRunNSINu", "NuMMRunNSINubar",
            "NuMMRunNSINu", "NuMMRunTransition", "NuMMRunTransSME",
            "NuMMRunNoChargeCut", "NuMMRunTemplates", "NuMMRunLED", "NuFCEvent",
            "NuMCEvent", "NuReco", "NuShiftableSpectrum", "NuShiftableBinnedSpectrum",
            "NuShiftableUnbinnedSpectrum", "NuSystematic", "NuSystFitter",
            "NuTreeWrapper", "NuUtilities", "NuZBeamReweight", "SRMom", "HoughTransNCPi0",
            "NuTH2Interpolator", "NuFCGridPoint", "NuFCGridPointNSINubar",
            "NuFCGridPointNSINu", "NuFCExperiment", "NuFCExperimentFactory",
            "NuFCExperimentFactoryNSI", "NuFCFitter", "NuFCFitterNSI",
            "NuFCFitterNSINubar", "NuFCFitterNSINu", "NuABFitter", "NuEZFitter",
            "NuEZFitterNSI", "NuEZRunsFitter", "NuFCConfig", "NuStatistics",
            "NuContour", "ConfigFile", "NuMatrix", "NuMatrix1D", "NuMatrix2D",
            "NuMatrixCPT", "NuCutter", "NuCut", "NuParticle"]

__all__ = []

for name in _all_ntuples:
  print name
  try:
    cattr = getattr(ROOT, name)
    __all__.append(name)
    globals()[name] = cattr
  except AttributeError:
    pass
del _all_ntuples