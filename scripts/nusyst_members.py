#!/usr/bin/env python
# coding: utf-8
"""
Uses clang to static-analyse NuSystematics.cxx to determine NuEvent member usage.

Usage: nusyst-members.py [--csv | --python] <systematics_file>

Options:
  --csv     Output a CSV table of the results
  --python  Output a python data structure describing the file
"""

from __future__ import absolute_import, print_function

from collections import defaultdict
import os, sys
import subprocess
import logging
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger()

from docopt import docopt


try:
  import clang.cindex
  from clang.cindex import CursorKind
except ImportError as ex:
  logger.error ("Could not import libclang; " + str(ex))
  print (__doc__)
  sys.exit(1)

def iterate_nodes(node):
    yield node
    for c in node.get_children():
        for ret in iterate_nodes(node):
            yield ret

def iterate_kind(node, kind):
    if node.kind == kind:
        yield node
    for c in node.get_children():
        for ret in iterate_kind(c, kind):
            yield ret

def find_member_accesses(start, classname):
    members = set()
    for ref in iterate_kind(start, CursorKind.MEMBER_REF_EXPR):
        
        if ref.referenced is None:
            continue
        if ref.referenced.semantic_parent is None:
            continue
        member = ref.referenced
        member_name = member.spelling
        # What are we a member of?
        owner = member.semantic_parent
        
        if not owner.spelling == classname:
            continue
        members.add(member_name)
    return members

def find_real_class_decl(cursor, classname):
  for clsd in (x for x in iterate_kind(cursor, CursorKind.CLASS_DECL) if x.spelling == classname):
    return clsd.get_definition()

def find_class_methods(classcursor):
  for child in classcursor.get_children():
    if child.kind == CursorKind.CXX_METHOD:
      yield child

def method_has_parameter_of(method, typename):
  """determines if a typename is a parameter to a method"""
  for parm in (x for x in method.get_children() if x.kind == CursorKind.PARM_DECL):
    tref = [x for x in parm.get_children() if x.kind == CursorKind.TYPE_REF]
    if not tref:
      continue
    assert len(tref) == 1
    if tref[0].referenced.spelling == typename:
      return True
  return False

if __name__ == "__main__":
  arguments = docopt(__doc__)
  source_file = arguments["<systematics_file>"]
  
  if not os.path.isfile(source_file):
    logger.error ("Could not find argument source file {}".format(source_file))
    sys.exit(1)

  # Work out the flags and/or the automatic source file
  flags = subprocess.check_output(["root-config","--cflags"]).split()
  if "SRT_PUBLIC_CONTEXT" in os.environ:
    flags += ["-I{}/include".format(os.environ["SRT_PUBLIC_CONTEXT"]),
              "-I{}/include/NtupleUtils".format(os.environ["SRT_PUBLIC_CONTEXT"])]
  else:
    logger.warn("No SRT_PUBLIC_CONTEXT evironment variable, may not find dependencies")

  if "SRT_PRIVATE_CONTEXT" in os.environ:
    # Prepend onto the list of flags
    flags = ["-I{}".format(os.environ["SRT_PRIVATE_CONTEXT"]),
              "-I{}/NtupleUtils".format(os.environ["SRT_PRIVATE_CONTEXT"])] + flags
  else:
    logger.warn("No SRT_PRIVATE_CONTEXT evironment variable, may not find dependencies")

  # Make sure the source file has flags added for it's location
  flags = ["-I{}".format(os.path.dirname(source_file)),
           "-I{}".format(os.path.normpath(os.path.join(os.path.dirname(source_file), "..")))] + flags

  print("Processing source file " + source_file, file=sys.stderr)
  index = clang.cindex.Index.create()
  tu = index.parse(source_file, args=flags)
  node_names = set()

  if tu.diagnostics:
    logger.warn ("Diagnostics:")
    logger.warn ("\n".join(str(x) for x in list(tu.diagnostics)))

  # Find all methods of the systematics class that access NuEvent
  systematics_class = find_real_class_decl(tu.cursor, "NuSystematic")
  if not systematics_class:
    logger.error ("Error: Could not find class declaration for NuSystematic")
    sys.exit(1)

  methods = [x for x in find_class_methods(systematics_class) if method_has_parameter_of(x, "NuEvent")]
  
  logger.debug ("NuSystematic methods that take NuEvent:")
  logger.debug (", ".join(x.spelling for x in methods))

  all_fields = []
  member_count = defaultdict(int)
  member_map = {}

  # Now, break down NuEvent accesses by method
  for method in (x.get_definition() for x in methods):
    members = find_member_accesses(method, "NuEvent")
    member_map[method.spelling] = members

    for m in members:
      if not m in all_fields:
        all_fields.append(m)
      member_count[m] = member_count[m] + 1

  # Sort the member list by occurence
  all_fields = sorted(all_fields, cmp=lambda x,y: cmp(member_count[x], member_count[y]), reverse=True)

  if arguments["--csv"]:
    # Draw a table
    name_len = max(len(x.spelling) for x in methods)
    print ("Name".ljust(name_len) + ", " + ", ".join(all_fields))
    for m in methods:
      print (m.spelling.ljust(name_len), end=", ")
      contains = zip(all_fields, (x in member_map[m.spelling] for x in all_fields))
      output = [("x" if y else "").ljust(len(x)) for x, y in contains]
      print (", ".join(output))
  elif arguments["--python"]:
    print (repr(member_map))
  else:
    name_len = max(len(x.spelling) for x in methods)
    for m in [x for x in methods if member_map[x.spelling]]:
      print (m.spelling.ljust(name_len), end=" ")
      varlist = [x for x in all_fields if x in member_map[m.spelling]]
      print (", ".join(varlist))
