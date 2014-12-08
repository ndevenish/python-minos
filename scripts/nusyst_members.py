#!/usr/bin/env python
# coding: utf-8
"""
Uses clang to static-analyse NuSystematics.cxx to determine NuEvent member usage.

Usage: nusyst-members.py [--csv | --python] [--dump] <systematics_file>

Options:
  --csv     Output a CSV table of the results
  --python  Output a python data structure describing the file
  --dump    (DEBUG) Dump the entire parse tree
"""

from __future__ import absolute_import, print_function

from collections import defaultdict, namedtuple
import os, sys
import subprocess
import logging
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger()

from docopt import docopt

try:
  from minos.ntupleutils.structs import SystematicInformation
except ImportError:
  SystematicInformation = namedtuple("SystematicInformation", ["enum", "name", "function", "mode"])

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
      #print (c)
      for ret in iterate_nodes(c):
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

def find_call_assigns_to(cursor, member):
  for ref in [x for x in iterate_kind(cursor, CursorKind.CALL_EXPR) if "operator=" in [x.spelling, x.displayname] ]:
    children = list(ref.get_children())
    # Look for this member within the first child
    for r in [x for x in iterate_nodes(children[0]) if x.kind == CursorKind.MEMBER_REF_EXPR and x.referenced == member]:
      yield ref

def find_binary_assigns_to(cursor, member):
  for ref in [x for x in iterate_kind(cursor, CursorKind.BINARY_OPERATOR)]:
    children = list(ref.get_children())
    for r in [x for x in iterate_nodes(children[0]) if x.kind == CursorKind.MEMBER_REF_EXPR and x.referenced and x.referenced == member]:
      yield ref

def find_real_class_decl(cursor, classname):
  for clsd in (x for x in iterate_kind(cursor, CursorKind.CLASS_DECL) if x.spelling == classname):
    return clsd.get_definition()

def find_class_methods(classcursor):
  for child in classcursor.get_children():
    if child.kind == CursorKind.CXX_METHOD:
      yield child
def find_class_field(classcursor, name):
  for child in classcursor.get_children():
    if child.kind == CursorKind.FIELD_DECL and child.spelling == name:
      return child

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

def dump_tree(cursor, depths=[]):
  SPACER_CHILD = u"\u2502 "
  SPACER_REF   = u"\u2551 "

  #print "| "*(depth-1)
  disp = cursor.spelling or cursor.displayname or ""
  print ("{} <line:{} col:{}> {}".format(cursor.kind.name, cursor.location.line, cursor.location.column, disp))
  all_children = list(cursor.get_children())
  has_reference = cursor.referenced and not cursor.referenced == cursor
  #spacing = "".join([u"\u2502 " if x else "  " for x in depths])
  spacing = "".join(depths)
  for i, child in enumerate(cursor.get_children()):
    is_last_child = (i+1 == len(all_children))
    is_last = is_last_child and not has_reference
    corner = u"\u2514\u2500" if is_last else u"\u251C\u2500"
    print (spacing + corner, end='')
    # What do we pass down as a divider?
    if is_last:
      depth_spacer = "  "
    elif is_last_child:
      depth_spacer = SPACER_REF
    else:
      depth_spacer = SPACER_CHILD
    dump_tree(child, depths+[depth_spacer])
  if cursor.referenced and not cursor.referenced == cursor:
    print (spacing + u"\u255A\u2550", end='')
    #dump_tree(cursor.referenced, depth, skip+1)
    ref = cursor.referenced
    print ("{} <line:{} col:{}> {}".format(ref.kind.name, ref.location.line, ref.location.column, ref.spelling))

def get_member_array_values(cursor, systematics_class, field_name):
  table = {}
  # Look up initialisation methods
  systNames = find_class_field(systematics_class, field_name)
  for assignment in find_call_assigns_to(tu.cursor, systNames):
    children = list(assignment.get_children())
    enum_name = extract_enum_name(children[0])
    # The value is embedded in the third entry
    assert len(children) >= 3
    table[enum_name] = children[2]
    # Find the string literal
    #string = list(iterate_kind(children[2], CursorKind.STRING_LITERAL))[0]
    #text = list(string.get_tokens())[0].spelling[1:-1]
    #table[text] = enum_name
#    print (enum_name, "=", text)
    #table[enum] = text
  return table

def extract_literal_string(cursor):
  string = list(iterate_kind(cursor, CursorKind.STRING_LITERAL))[0]
  return list(string.get_tokens())[0].spelling[1:-1]

def extract_enum_name(cursor):
    enums = list([x.referenced for x in iterate_kind(cursor, CursorKind.DECL_REF_EXPR) if x.referenced.kind == CursorKind.ENUM_CONSTANT_DECL])
    return enums[0].spelling
    
def get_systname_table(cursor, systematics_class):
  """Returns a map of enum:name"""
  # Look up initialisation methods
  cursors = get_member_array_values(cursor, systematics_class, "systNames")
  # Convert the cursor references to string literals
  return {x: extract_literal_string(y) for x, y in cursors.items()}    

def get_syst_mode_table(cursor, systematics_class):
  #cursors = get_member_array_values(cursor, systematics_class, "systMode")
#  return {x: extract_enum_name(y) for x, y in cursors.items()}
  table = {}
  modes = find_class_field(systematics_class, "systMode")
  for assignment in find_binary_assigns_to(cursor, modes):
    children = list(assignment.get_children())
    enum_name = extract_enum_name(children[0])
    # The value is embedded in the third entry
    assert len(children) >= 2
    table[enum_name] = children[1].spelling or children[1].displayname
  return table

def get_syst_function_map(cursor, systematics_class):
  table = {}
  # Find the shift method
  shift = [x.get_definition() for x in find_class_methods(systematics_class) if x.get_definition() and x.get_definition().spelling == "Shift"][0]
  assert shift
  for ifst in iterate_kind(shift, CursorKind.IF_STMT):
    (expr, action) = list(ifst.get_children())
    # Look for every enum here
    for enum in [x for x in iterate_kind(expr, CursorKind.DECL_REF_EXPR) if x.referenced.kind == CursorKind.ENUM_CONSTANT_DECL]:
      table[enum.displayname] = action.displayname
  return table

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
    logger.warn("No SRT_PUBLIC_CONTEXT environment variable, may not find dependencies")

  if "SRT_PRIVATE_CONTEXT" in os.environ:
    # Prepend onto the list of flags
    flags = ["-I{}".format(os.environ["SRT_PRIVATE_CONTEXT"]),
              "-I{}/NtupleUtils".format(os.environ["SRT_PRIVATE_CONTEXT"])] + flags
  elif not "SRT_PUBLIC_CONTEXT" in os.environ:
    # Only warn about private if there was no public
    logger.warn("No SRT_PRIVATE_CONTEXT environment variable, may not find dependencies")

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

  if arguments["--dump"]:
    dump_tree(tu.cursor)
    sys.exit(0)

  # Find all methods of the systematics class that access NuEvent
  systematics_class = find_real_class_decl(tu.cursor, "NuSystematic")
  if not systematics_class:
    logger.error ("Error: Could not find class declaration for NuSystematic")
    sys.exit(1)

  # Gather information for the systematics table
  systNames = get_systname_table(tu.cursor, systematics_class)
  modes = get_syst_mode_table(tu.cursor, systematics_class)
  fmap = get_syst_function_map(tu.cursor, systematics_class)
  syst_data = {}
  for enum in set(systNames.keys()) | set(modes.keys()) | set(fmap.keys()):
    try:
      name = systNames[enum]
      function = fmap[enum]
      mode = modes[enum]
      syst_data[enum] = SystematicInformation(enum=enum, name=name, function=function, mode=mode)
    except KeyError:
      logger.warning("Incomplete information for enum " + enum)
      continue
  
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
    print ("_systematic_data = " + repr(syst_data))
    print ("_systematic_variables = " + repr(member_map))
  else:
    name_len = max(len(x.spelling) for x in methods)
    for m in [x for x in methods if member_map[x.spelling]]:
      print (m.spelling.ljust(name_len), end=" ")
      varlist = [x for x in all_fields if x in member_map[m.spelling]]
      print (", ".join(varlist))
