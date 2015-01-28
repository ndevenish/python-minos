# coding: utf-8

"""Handles parsing and structure of the minossoft Makefiles"""

from __future__ import print_function
import re
import sys, os
from collections import defaultdict
import glob
import itertools
#from .options import OPTIONS

reMakeLines = re.compile(r'^((?:[^\n]+\\\n)*[^\r\n]+$)', re.MULTILINE)
reStripComments = re.compile(r'((?:#[^\\\n]*$)|(?:#[^\\\n]+(?=\\\n)))', re.MULTILINE)

reNormalComments = re.compile(r'(#.*$)', re.MULTILINE)
reContinueComments = re.compile(r'(#.*(?=\\\n))',re.MULTILINE)
reContinuation = re.compile(r'[ \t]*\\\n[ \t]*', re.MULTILINE)

reVarExpansion = re.compile(r'\$[\({]([^\)}]+)[\)}]')
reFilterOut = re.compile(r'\$\(\s*filter-out (.*),(.*)\)')

reIdentifier = re.compile("[_A-Za-z][_a-zA-Z0-9]*$")

class MakefileInfo(object):
  def __init__(self, filename):
    self.file = filename
    self.folder = os.path.dirname(filename)
    self.data = open(filename).read()
    self.vars = defaultdict(list)
    self.subdirs = []
    self.target = None
    self.uses_gsl = False
    self.uses_mysql = False
    self.skip_target = False
    self.override = set() # Override variables
    self.uses_sigc = False
    self.uses_fortran = False
    self.uses_neugen = False
    self.uses_pythia = False
  

  @property
  def all_sources(self):
    return list(itertools.chain(self.vars["LIBCXXFILES"],self.vars["LIBCCFILES"],self.vars["LIBCPPFILES"],self.vars["LIBCFILES"]))

  @property
  def build_library(self):
    return self.all_sources and self.vars["LIB"] #and not self.skip_target

  
class MakefileError(Exception):
  pass
class UnrecognisedMakefileLine(MakefileError):
  pass
class UnsupportedMakefileOp(MakefileError):
  pass
class BadAssumptionExpansion(MakefileError):
  pass

def _clean_makefile(data):
  """Strings all comments and line continuations from a makefile"""
  data = reContinueComments.sub("", data)
  data = reNormalComments.sub("", data)
  data = reContinuation.sub(" ", data)
  return data

def _expand_phrase(var, makefile, feeder=None):
  value = "<expanded>"
  if var in makefile.vars:
    value = " ".join(makefile.vars[var])

  if var.startswith("wildcard"):
    wildcard = var[len("wildcard"):].strip()
    results = glob.glob(os.path.join(os.path.dirname(makefile.file), wildcard))
    value = " ".join([os.path.basename(x) for x in results])

  # Custom hack for the one instance of this in the makefiles
  if var.startswith("macros/wildcard"):
    wildcard = var[len("macros/wildcard"):].strip()
    results = glob.glob(os.path.join(os.path.dirname(makefile.file), "macros", wildcard))
    value = " ".join([os.path.join("macros", os.path.basename(x)) for x in results])    

  if "shell gsl-config" in var:
    makefile.uses_gsl = True
    value = ""

  if var in ["SRT_SUBDIR", "SRT_PRIVATE_CONTEXT", "SRT_PUBLIC_CONTEXT"]:
    return "$"+var
    #raise BadAssumptionExpansion("SRT_SUBDIR has no meaning in this context")

  if var == "skipfiles:.cxx=.h":
    # Special case
    return " ".join([x.replace("cxx", "h") for x in makefile.vars["skipfiles"]])

  # In NeugenInterface, assigns from unset variable
  if var == "BINS":
    return ""

  # If it is identifier-like, just leave it as is and print a warning
  if value == "<expanded>" and reIdentifier.match(var):
    print ("Warning: Do not know how to expand '{}'; Leaving as ${}".format(var,var))
    return "$"+var

  if value == "<expanded>":
    raise UnrecognisedMakefileLine("Could not expand {} - unrecognised expansion form".format(var))
  #print ("  Expanding {} to {}".format(var, value))
  return value

def _match_and_expand(value, makefile):
  match = reVarExpansion.search(value)
  while match:
    value = value[:match.start()] + _expand_phrase(match.group(1), makefile) + value[match.end():]
    match = reVarExpansion.search(value)
  return value

def _filter_out(line, makefile):
  match = reFilterOut.search(line)
  skip, full = match.groups()
  skip = _match_and_expand(skip, makefile).split()
  full = _match_and_expand(full, makefile).split()
  out = line[:match.start()] + " ".join([x for x in full if not x in skip]) + line[match.end():]
  #print ("Filter-line {} -> {}".format(line, out))
  return out

def _var_assign(line, rule, makefile, feeder):
  override, name, op, value = rule.findall(line)[0]
  override = override.strip() == "override"
  # Logic for override - if this var was specified override before and not now, ignore
  if override:
    makefile.override.add(name)
  elif name in makefile.override:
    return

  #print ("  Processing variable assignment {} {}=: ".format(name,op) + line, file=sys.stderr)
  # Look for any functional brackets first
  if reFilterOut.search(value):
    value = _filter_out(value, makefile)

  # Hack for complicated CPPFLag assignment that we can skip in cmake
  if name == "CXXFLAGS" and "mysql" in value:
    makefile.uses_mysql = True
    return

  try:
    value = _match_and_expand(value, makefile)
  except BadAssumptionExpansion:
    print ("  WARN: Bad expansion asssumption, skipping variable {}".format(name))
    makefile.vars[name] = []
    return

  if op == "":
    makefile.vars[name] = value.split()
  elif op == "+":
    makefile.vars[name].extend(value.split())
  elif op == ":":
    makefile.vars[name] = value.split()
  else:
    raise UnsupportedMakefileOp("Do not support assignment operator " + op)

def _include_makefile(line, rule, makefile, feeder):
  inc = rule.findall(line)[0]
  
#CINT_CXXFILES = $(wildcard *.cxx)
#CINTLIST += $(addsuffix .h, $(basename $(CINT_CXXFILES)))
  if inc.endswith("arch_spec_root.mk"):
    # Do the ROOT arch spec rules
    cxx = _expand_phrase("wildcard *.cxx", makefile).split()
    if not "CINT_CXXFILES" in makefile.override:
      makefile.vars["CINT_CXXFILES"] = cxx
    if not "CINTLIST" in makefile.override:
      makefile.vars["CINTLIST"].extend([os.path.splitext(x)[0] + ".h" for x in cxx])

  if inc.endswith("arch_spec_sigc++.mk"):
    makefile.uses_sigc = True

  if inc.endswith("arch_spec_gfortran.mk") or inc.endswith("arch_spec_f77.mk"):
    makefile.uses_fortran = True

  #print ("  Including sub-makefile: " + inc, file=sys.stderr)

def _vpath_dbi(line, rule, makefile, feeder):
  makefile.dbi_extra = True

known_conditionals = {
  'ifneq ($(findstring CYGWIN,$(SRT_ARCH)),)': False,
  'ifneq (${IFBEAM_DIR},)': False,
  'ifneq (,$(findstring Darwin, $(SRT_ARCH)))': False,
  'ifneq (,$(findstring Darwin,$(SRT_ARCH)))': False,
  'ifndef GENIE': True,
  'ifdef GENIE': False,
  'ifeq ($(findstring Darwin, $(SRT_ARCH)), Darwin)': False,
  'ifneq ($(findstring Darwin, $(SRT_ARCH)), Darwin)': True,
  'ifdef LABYRINTH_DIR': False,
  'ifdef MYSQL_DIR': False,
  'ifneq ($(findstring Darwin,$(SRT_ARCH)),)': False,
  'ifeq ($(TRIDPRINT),raw)': True,
  'ifeq ($(TRIDPRINT),asimage)': False,
  'ifneq ($(findstring IRIX,$(SRT_ARCH)),)': False,
  'ifndef NEUGEN3PATH': False,
  'ifeq (no,$(shell test -f `root-config --incdir`/NetErrors.h || echo no))': False,
  'ifeq ($(TRIDPRINT),writegif)': False,
  'ifneq ($(wildcard /usr/lib/ati),)': False,
  'ifneq ($(findstring profile,$(SRT_QUAL)),profile)': True, 
  'ifeq ($(findstring IRIX,$(SRT_ARCH)), IRIX)': False,
  'ifneq ($(shell /bin/ls $(CERNLIBS)/libkernlib_noshift.a 2> /dev/null ),)': False,
  'ifneq ($(shell /bin/ls $(CERNLIBS)/libpacklib_noshift.a 2> /dev/null ),)': False,
  'ifneq ($(shell /bin/ls $(CERNLIBS)/libpdflib804.a 2> /dev/null ),)': False,
  'ifneq ($(STDHEP_DIR),)': False,
  'ifeq ($(F77),gfortran)': True,
  'ifeq ($(F77),g77)': True,
  'ifeq ($(F77),f77)': False,
}
def _conditional(line, rule, makefile, feeder):
  #print ("Encountered Conditional: {}".format(line))
  if line.strip() in known_conditionals:
    result = known_conditionals[line.strip()]
    #print ("  Conditional known to be {}".format(result))
    if not result:
      # Easy part: skip until else
      while not feeder.line.strip() in ["else", "endif"]:
        feeder.nextline()
      #  print ("Skipping conditional line {}".format(feeder.line))
      if feeder.line.strip() == "else":
        feeder.nextline()

      while feeder.line.strip() != "endif":
      #  print ("Processing line {}".format(feeder.line))
        feeder.dispatch(makefile)
        feeder.nextline()
    else:
      feeder.nextline()
      while not feeder.line.strip() in ["else", "endif"]:
        feeder.dispatch(makefile)
        feeder.nextline()
      while feeder.line.strip() != "endif":
        feeder.nextline()
  else:
    raise MakefileError("Unknown conditional {}".format(line))

def _message(line, rule, makefile, feeder):
  print ("MESSAGE: {}".format(line))

def _endif(line, rule, makefile, feeder):
  print ("  WARNING: unattended endif, possible multiple-depth if?")

def _make_rule(line, rule, makefile, feeder):
#  print ("  SKipping make rule " + line )
  while feeder.peekline() is not None and (feeder.peekline().startswith("\t") or feeder.peekline() == ""):
    feeder.nextline()
#    print ("Skipped " + feeder.line)

def _other_vpath(line, rule, makefile, feeder):
  pass

make_rules = (
  (r'^\s*$', None), # Blank lines
  (r'^[ \t]*(override[ \t]+)?([^\s\t+?:!=]+)[ \t]*([+?:!])?=[ \t]*(.*)$', _var_assign), # Variable assignment
  (r'^include[ \t]+(.+)$', _include_makefile), # Makefile inclusion
  (r'^vpath (?:DatabaseInterface/)?DbiResultPtr.h', _vpath_dbi), # DBI Inclusion
  (r'^vpath (?:DatabaseInterface/)?DbiWriter.h', _vpath_dbi), # DBI Inclusion
  (r'^if', _conditional),
  (r'^[\s]*\$\(warning', _message),
  (r'^endif', _endif),
  (r'^[^:]+:', _make_rule),
  (r'^vpath', _other_vpath),
)

def _unrecognised(line, rule, makefile, feeder):
  print ("  Error: Unrecognised line: " + line)
  raise UnrecognisedMakefileLine(line)

def _determine_package(filename):
  """Walks up the filesystem until it finds a makefile with the right signature"""
  path = os.path.dirname(filename)
  while not os.path.dirname(path) == "/":
    #prev_dirname = os.path.basename(path)
    path, prev_dirname = os.path.split(path)
    makefile = os.path.join(path, "GNUmakefile")
    if "srt_internal_top_of_testrel" in open(makefile).read():
      #print ("Package for {} = {}".format(filename, prev_dirname))
      return prev_dirname
  raise RuntimeError("Could not determine package for makefile {}".format(filename))

class LineFeeder(object):
  def __init__(self, data, rules):
    self.data = data
    self.lines = data.splitlines()
    self.rules = [(re.compile(rule, re.M), func) for rule, func in rules] + [(None, _unrecognised)]
    self.cur_line = -1

  @property
  def line(self):
    if self.cur_line < 0 or self.cur_line >= len(self.lines):
      return None
    return self.lines[self.cur_line]

  def nextline(self):
    #while self.cur_line < len(self.lines):
    self.cur_line += 1
    return self.cur_line < len(self.lines)

  def peekline(self):
    if self.cur_line + 1 >= len(self.lines):
      return None
    return self.lines[self.cur_line+1]

  def dispatch(self, makefile):
    for rule, handler in self.rules:
      if rule and rule.match(self.line):
        break
    # Call the handler
    if handler is not None:
      handler(self.line, rule, makefile, self)

def parse_makefile(filename, package, targetname=None):
  targetname = targetname or package

  makefile = MakefileInfo(filename)
  makefile.data = _clean_makefile(makefile.data)
  makefile.vars["PACKAGE"] = [package]
  makefile.target = targetname
  
  # Set empty ROOT and MINOS libs for now
  makefile.vars["ROOTLIBS"] = []
  makefile.vars["ROOTGLIBS"] = []
  makefile.vars["MINOSLIBS"] = []

  makefile.vars["SRT_ARCH"] = ["Linux3.1"]

  makefile.vars["IFBEAM_DIR"] = []
  makefile.vars["SRT_PRIVATE_CONTEXT"] = os.environ["SRT_PUBLIC_CONTEXT"]
  makefile.vars["SRT_PROJECT"] = ["MINOS"]
  makefile.vars["ENV_CPPFLAGS"] = []
  makefile.vars["CERNPAK"] = []
  makefile.vars["ROOTSYS"] = ["$ROOTSYS"]

  # Force this until we have proper dependency checking
  if targetname == "PulserCalibration":
    makefile.uses_mysql = True

  if targetname == "NeugenInterface" and not "dummy" in makefile.folder:
    makefile.uses_neugen = True
    makefile.uses_pythia = True

  # PhysicsNtuple/Store have clang errors
  # MidadGUI has lots of 64-bit issues, skip it (and all dependencies e.g. midad) for now
  skips = ["Registrytest", "MidadGui", "TriD", "PhysicsNtuple", "PhysicsNtupleStore"]
  if targetname in skips or targetname.startswith("Midad"):
    makefile.skip_target = True

  #if targetname in ["OnlineUtil"]:
  #  raise MakefileError("Hard skipping {}".format(targetname))

  feeder = LineFeeder(makefile.data, make_rules)

  # Split the makefile into lines
  while feeder.nextline():
    feeder.dispatch(makefile)
  #for line in feeder.nextline():
    
  if targetname == "NeugenInterface" and os.path.isdir(os.path.join(makefile.folder, "dummy")):
    if not "dummy" in makefile.vars["SUBDIRS"]:
      makefile.vars["SUBDIRS"].append("dummy")

  # Process any SUBDIRs
  for subdir in makefile.vars["SUBDIRS"]:
    try:
      sub_makefile = os.path.join(makefile.folder, subdir, "GNUmakefile")
      print ("  Processing Subdir {}".format(subdir))
      if not os.path.isfile(sub_makefile):
        print ("  ERROR: Could not process subdir " + subdir, file=sys.stderr)
      makefile.subdirs.append((subdir, parse_makefile(sub_makefile, package, makefile.target+subdir)))
    except MakefileError as ex:
      print ("  ERROR: Could not process sub-package {}: {}".format(subdir, ex))
  #print (makefile.vars)

  # Special-case post-processing
  if targetname == "OnlineUtil":
    replacements = {
      "msgLog.c": "msgLogLib/msgLog.c",
      "msgRead.c": "msgLogLib/msgRead.c",
      "keyValuePair.c": "kvplib/keyValuePair.c",
      "KeyRing.c": "kvplib/KeyRing.cc"
    }
    sources = set(makefile.vars["LIBCFILES"])
    for x, y in replacements.items():
      sources.discard(x)
      sources.add(y)
    makefile.vars["LIBCFILES"] = list(sources)

  return makefile