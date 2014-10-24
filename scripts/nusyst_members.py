#!/usr/bin/env python
# coding: utf-8
"""
Uses clang to static-analyse NuSystematics.cxx to determine NuEvent member usage.

Usage:
  minos-nusyst-members.py [<systematics_file>]
"""

from __future__ import absolute_import, print_function

from collections import defaultdict
import os, sys
import subprocess

from docopt import docopt

try:
  import clang.cindex
  from clang.cindex import CursorKind
except ImportError as ex:
  print ("Error: Could not import libclang; " + str(ex))
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
    for ref in iterate_kinds(start, [CursorKind.MEMBER_REF_EXPR]):
        
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
        #print ref.location.line, member_name, "->", owner.kind, owner.spelling

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

  arg_source_file = arguments["<systematics_file>"]
  source_file = arg_source_file
  if source_file and not os.path.isfile(source_file):
    print ("Error: Could not find argument source file {}".format(source_file))
    sys.exit(1)

  # Work out the flags and/or the automatic source file
  flags = subprocess.check_output(["root-config","--cflags"]).split()
  if "SRT_PUBLIC_CONTEXT" in os.environ:
    flags += ["-I{}/include".format(os.environ["SRT_PUBLIC_CONTEXT"]),
              "-I{}/include/NtupleUtils".format(os.environ["SRT_PUBLIC_CONTEXT"])]
    pub_source_file = os.path.join(os.environ["SRT_PUBLIC_CONTEXT"], "NtupleUtils", "NuSystematic.cxx")
    if os.path.isfile(pub_source_file):
      source_file = arg_source_file or pub_source_file
  if "SRT_PRIVATE_CONTEXT" in os.environ:
    # Prepend onto the list of flags
    flags = ["-I{}".format(os.environ["SRT_PRIVATE_CONTEXT"]),
              "-I{}/NtupleUtils".format(os.environ["SRT_PRIVATE_CONTEXT"])] + flags
    priv_source_file = os.path.join(os.environ["SRT_PRIVATE_CONTEXT"], "NtupleUtils", "NuSystematic.cxx")
    if os.path.isfile(priv_source_file):
      source_file = arg_source_file or priv_source_file
  # If given a source file, make sure this has flags added for it's location
  if arg_source_file:
    flags = ["-I{}".format(os.path.dirname(arg_source_file)),
             "-I{}".format(os.path.normpath(os.path.join(os.path.dirname(arg_source_file), "..")))] + flags

  if not source_file:
    print ("Error: Could not find NuSystematic.cxx. Set context or pass in as argument.")
    sys.exit(1)  

  print ("Processing source file " + source_file, file=sys.stderr)
  index = clang.cindex.Index.create()
  tu = index.parse(source_file, args=flags)
  node_names = set()

  if tu.diagnostics:
    print ("Diagnostics:", file=sys.stderr)
    print ("\n".join(str(x) for x in list(tu.diagnostics)), file=sys.stderr)

  # Find all methods of the systematics class that access NuEvent
  systematics_class = find_real_class_decl(tu.cursor, "NuSystematic")
  if not systematics_class:
    print ("Error: Could not find class declaration for NuSystematic")
    sys.exit(1)

  methods = [x for x in find_class_methods(systematics_class) if method_has_parameter_of(x, "NuEvent")]
  #dump_tree(systematics_class)
  print ("NuSystematic methods that take NuEvent:", file=sys.stderr)
  print (", ".join(x.spelling for x in methods), file=sys.stderr)

  all_fields = []
  member_count = defaultdict(int)
  member_map = {}

  # Now, break down NuEvent accesses by method
  for method in (x.get_definition() for x in methods):

    #print (method.spelling + ":")
    members = find_member_accesses(method, "NuEvent")
    #print ("  ", members)
    member_map[method.spelling] = members

    for m in members:
      if not m in all_fields:
        all_fields.append(m)
      member_count[m] = member_count[m] + 1

  # Sort the member list by occurence
  all_fields = sorted(all_fields, cmp=lambda x,y: cmp(member_count[x], member_count[y]), reverse=True)

  # Draw a table
  name_len = max(len(x.spelling) for x in methods)
  print ("Name".ljust(name_len) + ", " + ", ".join(all_fields))
  for m in methods:
    print (m.spelling.ljust(name_len), end=", ")
    contains = zip(all_fields, (x in member_map[m.spelling] for x in all_fields))
    output = [("x" if y else "").ljust(len(x)) for x, y in contains]
    print (", ".join(output))
