# coding: utf-8

import os

STANDARD_LOCATIONS = ["~/data.index", '/minos/app/nickd/data.index']

class Library(object):
  def __init__(self, library_file = None, tag_filter = None):
    if not library_file:
      for location in [os.path.expanduser(x) for x in STANDARD_LOCATIONS]:
        if os.path.isfile(location):
          library_file = location
          break
      if not library_file:
        raise IOError("Could not determine location of data library file!")
    self.library_file = library_file
    # Read the data library
    (self.file_tags, self.file_hashes) = self._read_library(library_file)
    self.filter = set(x.lower() for x in tag_filter) if tag_filter else set()

  def _read_library(self, filename):
    file_tags = {}
    hashes = {}
    folder_tags = {}
    with open(filename) as f:
      for line in f.readlines():
        parts = line.split()
        if parts[0].startswith("/"):
          folder_tags[parts[0]] = {x.strip(":").lower() for x in parts[1:]}
        else:
          hashes[parts[1]] = parts[0]
          tags = {x.strip(":").lower() for x in parts[2:]}
          for folder in folder_tags.keys():
            if parts[1].startswith(folder):
              tags.update(folder_tags[folder])
          file_tags[parts[1]] = tags
    return (file_tags, hashes)

  def get_file(self, tags):
    files = self.find_files(tags)
    if not len(files) == 1:
      if not files:
        raise IndexError("No file found satisfying tag list: {}".format(", ".join(tags)))
      else:
        raise IndexError("More than one match found for tag list: {}".format(", ".join(tags)))
    return files[0]

  def find_files(self, tags):
    tags = set(x.lower() for x in tags).union(self.filter)
    return [x for x in self.file_tags.keys() if self.file_tags[x].issuperset(tags)]

shared_library = None
try:
  shared_library = Library()
except:
  pass