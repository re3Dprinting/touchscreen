from builtins import object
import logging

class Material(object):
    def __init__(self, name, e1, e2, bed, parent=None):

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("Material __init__ <%s>/%d/%d/%d" % (name, e1, e2, bed))

        self.parent = parent
        self.name = name
        self.e1 = e1
        self.e2 = e2
        self.bed = bed

    def _log(self, message):
        self._logger.debug(message)

    def e1set(self):
        self._log("UI: User touched <%s> extruder 0 preset (%d)." % (self.name, self.e1))
        self.parent.extruder1.setandsend(self.e1)

    def e2set(self):
        self._log("UI: User touched <%s> extruder 1 preset (%d)." % (self.name, self.e2))
        self.parent.extruder2.setandsend(self.e2)

    def bedset(self):
        self._log("UI: User touched <%s> bed preset (%d)." % (self.name, self.bed))
        self.parent.heatedbed.setandsend(self.bed)

    def allset(self):
        self._log("UI: User touched <%s> ALL preset (%d/%d/%d)." % (self.name, self.e1, self.e2, self.bed))
        self.parent.extruder1.setandsend(self.e1)
        self.parent.extruder2.setandsend(self.e2)
        self.parent.heatedbed.setandsend(self.bed)
