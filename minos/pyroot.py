# coding: utf-8

"""Utilities to make accessing pyroot structures easier"""

import numpy as np

ACCEPTED_TYPES = {'UInt_t', 'Float_t', 'Int_t', 'Char_t'}
ROOT_TYPE_MAP = {"UInt_t": "uint32", "Float_t": "float32", "Int_t": "int32", "Char_t": "int8"}
TREE_ACCESS_METHOD = {
  "UInt_t": lambda x: x.GetValueLong64,
  "Float_t": lambda x: x.GetValue,
  "Int_t": lambda x: x.GetValueLong64,
  "Char_t": lambda x: x.GetValueLong64,
}





#leaves = [x for x in tree.GetListOfLeaves() if x.GetTypeName() in ACCEPTED_TYPES and not x.GetName() in {"fBits", "fUniqueID"}]


def get_tree_dtype(leaves):
  """Returns a numpy dtype structure from a list of leaves"""
  # Build the numpy field list
  return [(x.GetName(), ROOT_TYPE_MAP[x.GetTypeName()]) for x in leaves]

def get_row_accessor(leaves):
  dtype = get_tree_dtype(leaves)
  def _get_row():
    return np.array(tuple([TREE_ACCESS_METHOD[x.GetTypeName()](x)() for x in leaves]), dtype=dtype)
  return _get_row

def read_tree_columns(tree, names):
  """Reads a set of columns from a tree and returns a numpy array"""
  tree.SetBranchStatus("*",0)
  for name in names:
    tree.SetBranchStatus(name,1)
  leaves = [tree.GetLeaf(x) for x in names]
  # Check all of these leaves exist
  if not all(leaves):
    noleaf = [name for i, name in enumerate(names) if not leaves[i]]
    raise RuntimeError("Could not read leaves named: {}".format(", ".join(noleaf)))
  # Build the output array and row reader
  output = np.zeros(tree.GetEntries(), dtype=get_tree_dtype(leaves))
  read_rows = get_row_accessor(leaves)
  # Read everything from the tree
  for i, entry in enumerate(tree):
    output[i] = read_rows()
  # Leave the tree in the same all-access state
  tree.SetBranchStatus("*",1)
  return output
