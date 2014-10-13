# coding: utf-8

import ROOT

ROOT.gSystem.Load("libNtupleUtilsFC.so")

from ROOT import (NuFCDelegate, NuFCMultiDelegate, NuFCDelegateArchiver,
                  NuFCDelegateWriterLegacy, NuFCDelegateOutput, 
                  NuFCEvent2, NuFCEventManager, NuFCRunInfo, NuFCRunner)