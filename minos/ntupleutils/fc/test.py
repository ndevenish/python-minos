# coding: utf-8

import logging
logger = logging.getLogger(__name__)

# OLD PROCeSSING
class Event(ntu.NuEvent):
  def apply_row(self, row):
    """Apply a numpy row to the event class"""
    for (name, value) in zip(row.dtype.names, row):
      setattr(self, name, value)
    self.energy = self.trkEn + self.shwEn

# Run a whole set of tests for this new method being identical to the old
def check_table(table, systematics, max_events=None):
  if max_events is not None:
    table = table[:max_events]
  shifter = Systematics(table)
  start = time.time()
  new_method_events = shifter.shift(systematics)
  logger.info("New shift took: {}s".format(time.time()-start))
  event = Event()
  nusyst_shifter = Applicator(syst_to_sigma(systematics))
  selector = ntu.cuts.Passthrough()
  nusyst_shifter.set_nubar_cutter(selector)
  start = time.time()
  for row, new_event in zip(table, new_method_events):
    # import pdb
    # pdb.set_trace()
    event.apply_row(row)
    nusyst_shifter.shift(event)
    # Now, compare these two
    assert all([numpy.isclose(getattr(event, x), new_event[x]) for x in new_event.dtype.names])
  logger.info("Syst: {}s".format(time.time()-start))

def generate_shifted_histogram(events, shifts={}):
  """Builds a shifted TH1D spectrum from a set of numpy events"""
  hname = str(uuid.uuid4())[:6]
  spectrum = TH1D(hname,hname,len(ntu.binningscheme4())-1, ntu.binningscheme4())

  event = Event()
  shifter = Applicator(shifts)
  selector = ntu.cuts.Passthrough()
  shifter.set_nubar_cutter(selector)
  for row in events:
    event.apply_row(row)
    shifter.shift(event)
    spectrum.Fill(event.energy, event.rw)
  return ntu.NuMatrixSpectrum(spectrum, events.pot)

class testNumpySystematics(object):
  @classmethod
  def setupClass(cls):
    ev_files = dataLib.get_dataset("reduced_fc_events")
    cls.events = load_and_oscillate_events(ev_files.run3, 7e20)

  def testNoShiftOnNewShifter(self):
    "Validate that the no-shifts set does not shift on the new method"
    for x in ntu.iterTuple(self.events):
      shifter = Systematics(x)
      noshift = shifter.shift(NO_SHIFTS)
      assert numpy.all(x["rw"]==noshift["rw"])
      assert numpy.all(x["trkEn"]==noshift["trkEn"])
      assert numpy.all(x["shwEn"]==noshift["shwEn"])

  def testNoShiftCase(self):
    "Test that no shifting matches between methods"
    # ntu.mapTuples(lambda x: check_table(x, NO_SHIFTS), [events])
    for x in ntu.iterTuple(self.events):
      check_table(x, NO_SHIFTS, max_events=1000)

  def testManyShiftCases(self):
    "Tests on a range of shift cases that results are identical"
    for i in range(10):
      shift = shift_generator(SHIFT_RANGES)
      logger.debug("Testing {}/{} ({})".format(i, 10, shift))
      for x, path in ntu.iterTuple(self.events, path=True):
        logger.debug("  ..{}".format(".".join(path)))
        check_table(x, shift, max_events=1000)

  def testIndividualSystematics(self):
    """Test one systematic at a time for identical results"""
    # Find the first systematic that causes a difference
    shift = shift_generator(SHIFT_RANGES)
    for name in shift.keys():
      logger.info("Testing " + name)
      # Change just ONE shift at a time
      newShift = dict(NO_SHIFTS)
      # Validate that it is actually changing
      assert newShift[name] != shift[name]
      newShift[name] = shift[name]
      # Check every sample against this
      for x in ntu.iterTuple(self.events):
        check_table(x, newShift, max_events=1000)
