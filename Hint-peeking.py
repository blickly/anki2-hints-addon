# -*- coding: utf-8 -*-
# Author:  Ben Lickly <blickly at berkeley dot edu>
#
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
#   Hint-peeking add-on
#
# This add-on allows peeking at some of the fields in a flashcard
# before seeing the answer. This can be used to peek at word context,
# example sentences, word pronunciation (especially useful for
# Chinese/Japanese/Korean), and much more.

from PyQt4.QtCore import Qt

########################### Settings #######################################
# The following settings can be changed to suit your needs. Lines
# starting with a pound sign (#) are comments and are ignored.

# SHOW_HINT_KEY defines the key that will reveal the hint fields.
# A list of possible key values can be found at:
#       http://opendocs.net/pyqt/pyqt4/html/qt.html#Key-enum
SHOW_HINT_KEY=Qt.Key_H

# CARD_TEMPLATES defines a list of card templates for which hints may
# be used. Other templates will not show anything when the show hint key
# is pressed.
CARD_TEMPLATES=["Recognition"]
######################### End of Settings ##################################

import simplejson
from anki.hooks import wrap
from aqt.reviewer import Reviewer

def newKeyHandler(self, evt, _old):
    """Show hint when the SHOW_HINT_KEY is pressed."""
    if (self.state == "question"
            #and self.card.model() in CARD_TEMPLATES
            and evt.key() == SHOW_HINT_KEY):
        print "Models: {{{{" + str(self.card.model()) + "}}}}"
        self._showHint()
    else:
        return _old(self, evt)

def _showHint(self):
    """To show hint, display answer and filter out the non-hint parts."""
    self.state = "hint"
    c = self.card
    h = c.a()
    h.replace("<style>", "<style>.nonhint{color:white;}")
    print "h: {{{{" + h + "}}}}"
    h = self._mungeQA(h)
    self.web.eval("_updateQA(%s, true);" % simplejson.dumps(h))
    #runHook('showHint')

Reviewer._keyHandler = wrap(Reviewer._keyHandler, newKeyHandler, "around")
Reviewer._showHint = _showHint

