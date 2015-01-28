# coding: utf-8

from __future__ import print_function
import os, sys
from itertools import chain

from pkg_resources import resource_string

magic_deps = {'Filtration': set(['REROOT_Classes', 'RecoBase']), 'Candidate': set(['MessageService']), 'PhotonTransportToyMC': set(['CandDigit', 'Digitization']), 'NCUtilsDataQuality': set(['NCUtilsExtrapolation']), 'AtNuAna': set(['AtNuEvent', 'Validity']), 'NtpVtxFinderModule': set(['StandardNtuple', 'JobControl']), 'Lattice': set(['MessageService']), 'MiniBooNEAna': set(['StandardNtuple']), 'Persistencytest': set(['Persistency', 'RawData']), 'PhysicsNtupleFill': set(['Calibrator']), 'MCApplication': set(['GeoGeometry']), 'AstroUtil': set(['MessageService']), 'DatabaseUpdater': set(['DatabaseInterface', 'Registry', 'RawData']), 'MCNNAnalysis': set(['NueAna', 'BeamDataUtil']), 'PhysicsNtupleMinos': set(['StandardNtuple', 'MinosObjectMap']), 'MeuCal': set(['Calibrator', 'StandardNtuple', 'BeamDataNtuple', 'BeamDataUtil', 'AtNuEvent', 'JobControl']), 'Navigation': set(['MessageService']), 'NueAnaParticlePID': set(['NueAna']), 'NtpFitSA': set(['Record']), 'Plex': set(['DatabaseInterface', 'Configurable', 'Registry', 'RawData']), 'PmtDrift': set(['Calibrator']), 'NtupleUtilsSterile': set(['NuMuBar']), 'CandClusterSR': set(['RecoBase']), 'Registry': set(['MessageService']), 'CandNtupleSRModule': set(['StandardNtuple', 'CandFitTrackCam', 'CandMorgue', 'CandShowerSR', 'CandFitTrackSR']), 'CandShowerEM': set(['RecoBase']), 'Dispatcher': set(['Persistency', 'Registry', 'MinosObjectMap']), 'StandardNtuple': set(['MCNtuple', 'TruthHelperNtuple', 'CandNtupleSR']), 'TruthHelperNtuple': set(['Record']), 'BeamDataUtil': set(['DatabaseInterface', 'Utility', 'Registry', 'RawData']), 'MINF_Classes': set(['REROOT_Classes']), 'CandNtupleEMModule': set(['CandFitShowerEM', 'CandNtupleSR']), 'GeoGeometrytest': set(['Plex']), 'NtupleBasetest': set(['NtupleBase', 'CandTrackSR']), 'OscProb': set(['MessageService']), 'GeoSwimmer': set(['MCApplication']), 'CandNtupleSR': set(['Plex']), 'NueAnaReweight': set(['NueAna']), 'NuBarPID': set(['MessageService']), 'CandChop': set(['RecoBase']), 'CandShowerSR': set(['CandSubShowerSR']), 'NCUtilsExtrapolation': set(['NCUtils', 'Registry', 'NCUtilsFitter']), 'NuMuBar': set(['NtupleUtils', 'NtpFitSA', 'BeamDataUtil']), 'GeoGeometry': set(['UgliGeometry']), 'NtupleBase': set(['Record']), 'Sensitivity': set(['NueAna']), 'ParticleTransportSim': set(['MCApplication', 'Digitization', 'JobControl']), 'Conventions': set(['MessageService']), 'CalDetDST': set(['CandFitTrackSR', 'MINF_Classes', 'CandNtupleSR', 'CalDetPID', 'Digitization']), 'CandFitTrackMS': set(['RecoBase', 'MINF_Classes']), 'CandFitTrackSA': set(['Swimmer', 'RecoBase', 'NtpFitSA', 'GeoSwimmer']), 'JobControl': set(['Registry', 'MinosObjectMap']), 'NtupleUtils': set(['StandardNtuple', 'JobControl', 'BeamDataNtuple']), 'CandFitShowerEM': set(['CandShowerEM']), 'NueAnaModule': set(['NueAna', 'BeamDataUtil']), 'NueAnaParticleFinder': set(['MuonRemoval', 'StandardNtuple', 'NueAnaParticleManaged']), 'CandFitTrackCam': set(['Swimmer', 'DataUtil', 'GeoSwimmer']), 'MCMerge': set(['REROOT_Classes', 'Digitization', 'JobControl']), 'NtpVtxFinder': set(['CandNtupleSR']), 'MinosObjectMaptest': set(['Record']), 'EVD': set(['CalDetPID', 'CandFitTrackSR']), 'NtupleUtilsFC': set(['NtupleUtils']), 'Recorddemo': set(['Record']), 'RunSummary': set(['CandData', 'Plex']), 'LeakChecker': set(['MessageService']), 'TruthHelperNtupleModule': set(['StandardNtuple', 'RecoBase', 'Digitization']), 'FilterLI': set(['CandDigit']), 'MinosObjectMap': set(['Record']), 'ShieldPlank': set(['CandDigit']), 'MCNtuple': set(['Record']), 'NtpTiming': set(['StandardNtuple']), 'Rotorooter': set(['Persistency', 'RawData', 'JobControl']), 'GhostFitter': set(['OscProb']), 'DatabaseInterfacetest': set(['DatabaseInterface']), 'BeamDataDbi': set(['BeamDataUtil']), 'DataUtil': set(['REROOT_Classes', 'RecoBase', 'Digitization']), 'Algorithm': set(['DatabaseInterface']), 'NueAnaParticleAna': set(['NueAnaParticleFinder', 'OscProb']), 'RunQuality': set(['DatabaseInterface']), 'NueAnaParticlePIDAnalysis': set(['NueAnaParticlePID']), 'DatabaseMaintenance': set(['DatabaseInterface', 'JobControl']), 'CandDigit': set(['Navigation', 'Algorithm', 'CandData', 'Calibrator']), 'Latticetest': set(['Lattice']), 'CandSubShowerSR': set(['RecoBase']), 'Recordtest': set(['RawData', 'JobControl']), 'Record': set(['Validity']), 'MuonRemovalModule': set(['MuonRemoval']), 'CalDetPID': set(['CandDigit', 'CalDetSI']), 'UgliGeometry': set(['Plex']), 'RecoBase': set(['CandDigit']), 'IoModules': set(['Persistency', 'CandData', 'MINF_Classes']), 'Dispatchertest': set(['JobControl']), 'DeMux': set(['UgliGeometry', 'CandDigit']), 'AtNuUtils': set(['MessageService', 'AtNuEvent']), 'XTalkFilter': set(['StandardNtuple', 'JobControl']), 'NueAnaParticleSystematic': set(['StandardNtuple', 'JobControl']), 'PhotonTransport': set(['Digitization', 'JobControl', 'Calibrator']), 'Swimmer': set(['Plex']), 'Navigationtest': set(['Navigation']), 'CheckGC': set(['PulserCalibration']), 'StandardNtupleModule': set(['StandardNtuple', 'CandData']), 'AnalysisNtuples': set(['MessageService']), 'Configurable': set(['MessageService']), 'NueAna': set(['AnalysisNtuplesModule', 'CalDetDST', 'NueAnaParticleAna', 'NueAnaTools']), 'CandTrackCam': set(['RecoBase']), 'StupidGeometry': set(['Plex']), 'Utility': set(['MessageService']), 'PEGain': set(['PulserCalibration']), 'MuonRemoval': set(['DataUtil']), 'BeamDataMonitoring': set(['BeamDataUtil']), 'JobControltest': set(['Registry']), 'CandMorgue': set(['RunQuality', 'DcsUser', 'CandDigit']), 'RawData': set(['Record']), 'FarDetDataQuality': set(['Navigation', 'Algorithm', 'CandData']), 'DynamicFactory': set(['MessageService']), 'Digitization': set(['Plex']), 'LeakCheckertest': set(['MessageService']), 'TimeOfFlight': set(['CandTrackCam', 'NuMuBar']), 'CandEventSR': set(['CandShowerSR']), 'PulserCalibration': set(['JobControl', 'Calibrator']), 'BeamDataAnaSummary': set(['MessageService']), 'VertexFinder': set(['RecoBase']), 'NueAnaTools': set(['MuonRemoval', 'StandardNtuple']), 'NoiseFilter': set(['JobControl', 'Calibrator']), 'AnalysisNtuplesModule': set(['Mad', 'JobControl', 'BeamDataNtuple']), 'AtNuOutput': set(['CandMorgue', 'DataUtil', 'AtNuEvent']), 'NCUtilsCuts': set(['MessageService']), 'AtNuOscillation': set(['OscProb']), 'BeamDataNtuple': set(['Record']), 'DcsUser': set(['DatabaseInterface', 'RawData', 'JobControl']), 'IoModulestest': set(['MessageService']), 'MCReweight': set(['DatabaseInterface']), 'MCNtupleModule': set(['REROOT_Classes', 'StandardNtuple', 'DetSim', 'PhotonTransport']), 'RerootExodus': set(['UgliGeometry', 'CandDigit', 'Digitization', 'MINF_Classes']), 'LISummary': set(['PulserCalibration']), 'ParticleTransportSimtest': set(['ParticleTransportSim']), 'CalDetSI': set(['REROOT_Classes', 'Navigation', 'Algorithm', 'CandData', 'Plex']), 'Persistency': set(['Record']), 'CandNtupleEM': set(['CandNtupleSR']), 'PhotonTransporttest': set(['Digitization', 'JobControl']), 'MCApplicationtest': set(['MessageService']), 'ScintCal': set(['StandardNtuple', 'JobControl', 'Calibrator']), 'AtNuReco': set(['REROOT_Classes', 'RecoBase']), 'DetSim': set(['Digitization', 'JobControl', 'Calibrator']), 'NueAnaExtrapolation': set(['NueAna']), 'CandNtupleEMtest': set(['CandNtupleEM']), 'SpillLooter': set(['SpillTiming']), 'PhysicsNtupleDraw': set(['Plex']), 'BFieldViz': set(['Plex']), 'NCUtilsExtraction': set(['NCUtilsCuts', 'AnalysisNtuples', 'JobControl']), 'SimCheck': set(['Digitization', 'JobControl']), 'CandData': set(['Candidate', 'RawData', 'JobControl']), 'DatabaseInterface': set(['Record']), 'NueAnaParticleManaged': set(['MessageService']), 'CandFitTrackSR': set(['CandTrackSR', 'Swimmer']), 'Validity': set(['MessageService']), 'Mad': set(['StandardNtuple', 'CandNtupleEM', 'AnalysisNtuples', 'MCReweight']), 'NumericalMethods': set(['MessageService']), 'BeamDataNtupleModule': set(['DatabaseInterface', 'RawData', 'JobControl']), 'Fabrication': set(['Plex']), 'BeamDataAna': set(['BeamDataAnaNt', 'RawData']), 'CandShield': set(['Plex']), 'BField': set(['Plex']), 'NtpFitSAModule': set(['CandFitTrackSA']), 'PhysicsNtupleShort': set(['Calibrator']), 'NCUtils': set(['AnalysisNtuples', 'Validity']), 'CandNtupleSRtest': set(['CandNtupleSR']), 'AtNuPerformance': set(['AtNuUtils', 'CandNtupleSR']), 'CandStripSR': set(['RecoBase']), 'AltDeMux': set(['CandDigit']), 'CandSliceSR': set(['RecoBase']), 'NueAnaParticleDisplay': set(['NueAna']), 'SpillTiming': set(['DatabaseInterface', 'Persistency', 'RawData', 'JobControl', 'Configurable']), 'Calibrator': set(['Plex']), 'Demo': set(['CandDigit', 'MINF_Classes']), 'PhysicsNtuplePlot': set(['Plex']), 'BeamDataAnaBv': set(['BeamDataAnaNt']), 'NueAnaDisplay': set(['NueAna']), 'CandTrackSR': set(['RecoBase']), 'CalDetTracker': set(['CalDetPID', 'DataUtil', 'MuELoss']), 'NCUtilsFitter': set(['MessageService']), 'FilterDigitSR': set(['CandDigit']), 'MessageServicetest': set(['MessageService']), 'Cluster3D': set(['RecoBase']), 'NueAnaMultiBinAna': set(['NueAna'])}

def _get_libname(makefile):
  new_name = makefile.vars["LIB"][0]
  if new_name.startswith("lib"):
    new_name = new_name[3:]
  return new_name

def _flatten_makefiles(makefiles):

  return chain(*(chain([makefile], *[_flatten_makefiles([y]) for x, y in makefile.subdirs]) for makefile in makefiles))

def create_lookup(makefiles):
  # Build a dictionary of library name-target to resolve explicitly named dependencies
  return {_get_libname(x): x.target for x in _flatten_makefiles(makefiles) if x.build_library}

def write_package_cmakelist(folder, makefile, liblookup):
  # Read the makefile options and build up commands for the add package command
  targetname = makefile.target
  cpp_sources = makefile.all_sources #makefile.vars["LIBCXXFILES"] + makefile.vars["LIBCCFILES"] + makefile.vars["LIBCPPFILES"] + makefile.vars["LIBCFILES"]
  data = ''
  build_lib = makefile.vars["LIB"]

  if makefile.uses_mysql:
    data = data + "find_package(MySQL)\nIF (MYSQL_FOUND)\n"

  if makefile.uses_neugen:
    data = data + "find_package(NEUGEN3)\nIF (NEUGEN3_FOUND)\n"
      
  if makefile.uses_fortran:
    cpp_sources = cpp_sources + makefile.vars["LIBFFILES"]
    # Make sure the fortran flags match the compilation of the CXX onesßß
    data = data + """enable_language(Fortran)
IF (${CMAKE_CXX_FLAGS} MATCHES "-m32")
  SET (CMAKE_Fortran_FLAGS ${CMAKE_Fortran_FLAGS} -m32)
ENDIF()
"""


  if makefile.vars["LIB"] and cpp_sources:
    pkg = "MINOS_ADD_LIBRARY( "
    spaces = " " * len(pkg)
    parts = []
    if makefile.vars["ROOTCINT"] == ["YES"]:
      parts.append("ROOTCINT")
    if makefile.uses_sigc:
      parts.append("SIGC")
    if cpp_sources:
      parts.append("SOURCES     " + " ".join(cpp_sources))
    if makefile.vars["CINTLIST"]:
      parts.append("CINTSOURCES " + " ".join(makefile.vars["CINTLIST"]))

    data = data + pkg + targetname
    if parts:
      data = data + "\n" + "\n".join([spaces + x for x in parts])
    data = data + " )\n"
  
    if not makefile.vars["LIB"] == ["lib" + targetname]:
      new_name = _get_libname(makefile)
      data = data + "set_target_properties( {} PROPERTIES OUTPUT_NAME {} )\n".format(targetname, new_name)

  if build_lib and makefile.skip_target:
    data = data + "set_target_properties({} PROPERTIES EXCLUDE_FROM_ALL 1)\n".format(targetname)

  if makefile.uses_gsl:
    #find_package(PkgConfig REQUIRED)
    data = data + "\n".join(["pkg_search_module(GSL REQUIRED gsl)",
                             "link_directories ( ${GSL_LIBRARY_DIRS} )",
                             "include_directories ( ${GSL_INCLUDE_DIRS} )",
                             "target_link_libraries( {} ${{GSL_LIBRARIES}})".format(targetname)]) + "\n"

  if makefile.uses_mysql:
    data = data + "\n" + "include_directories ( ${MYSQL_INCLUDE_DIR} )\n" + "target_link_libraries( {} ${{MYSQL_LIBRARIES}})\n".format(targetname) + "\n"
    data = data + "\nENDIF(MYSQL_FOUND)\n"

  if makefile.uses_neugen:
    data = data + """

include_directories ( ${{NEUGEN3_INCLUDE_DIRS}} )
target_link_libraries ( {} ${{NEUGEN3_LIBRARIES}} )
ENDIF(NEUGEN3_FOUND)
""".format(targetname)

  if makefile.vars["LIBLIBS"]:
    libs = [x[2:] for x in makefile.vars["LIBLIBS"] if x.startswith("-l")]
    package_libs = [x for x in libs if x in liblookup]
    unknown = [x for x in libs if not x in liblookup]
    if package_libs:
      data = data + "target_link_libraries ( {} {} )\n".format(targetname, " ".join([liblookup[x] for x in package_libs]))
    if unknown:
      print ("WARN: Unknown extra link targets {}".format(", ".join(unknown)))

#  if build_lib and _get_libname(makefile) in magic_deps:
#    libname = _get_libname(makefile)
#    deps = [liblookup[x] for x in magic_deps[libname]]
#    data = data + "target_link_libraries ( {} {} )\n".format(targetname, " ".join(deps))



  # Process any extra include folders
  if makefile.vars["CPPFLAGS"]:
    paths = [x[2:] for x in makefile.vars["CPPFLAGS"] if x.startswith("-I") and not x in ['-I..', '-I../..']]
    if paths:
      data = data + "include_directories ( {} )\n".format(" ".join(paths))

  if makefile.subdirs:
    data = data + "\n" + "\n".join("add_subdirectory({})".format(x) for x,y in makefile.subdirs)

  # Write the CMakeLists
  outfile = os.path.join(folder, "CMakeLists.txt")
  with open(outfile, 'w') as ofile:
    print ("Writing {}".format(outfile), file=sys.stderr)
    ofile.write(data)

  for name, makefile in makefile.subdirs:
    write_package_cmakelist(os.path.join(folder, name), makefile, liblookup)
  #print (data)

  #"MINOS_ADD_PACKAGE( NtupleUtils 
  #  ROOTCINT LINKERROR )"

def copy_data(filename, dest):
  # FindROOT
  data = resource_string(__name__, "data/" + filename)
  with open(dest, 'w') as out:
    out.write(data)

def write_release_cmake(release_base, packages):
  # Write the basic module files
  module_dir = os.path.join(release_base, "cmake", "modules")
  if not os.path.exists(module_dir):
    os.makedirs(module_dir)
  copy_data("FindROOT.cmake",  os.path.join(module_dir, "FindROOT.cmake"))
  copy_data("FindMySQL.cmake", os.path.join(module_dir, "FindMySQL.cmake"))
  copy_data("FindMINOS.cmake", os.path.join(module_dir, "FindMINOS.cmake"))
  copy_data("FindNUEGEN3.cmake", os.path.join(module_dir, "FindNEUGEN3.cmake"))

  # Raw CMakeLists
  cmake_base = resource_string(__name__, "data/BaseCMakeLists.txt")
  cmake_base = cmake_base.replace("$subdirectories$", "\n".join("add_subdirectory({})".format(x) for x in packages))
  with open(os.path.join(release_base, "CMakeLists.txt"), 'w') as f:
    f.write(cmake_base)
