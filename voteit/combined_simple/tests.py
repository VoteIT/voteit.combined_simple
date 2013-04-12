#import unittest
#
#import colander
#from pyramid import testing
#from zope.interface.verify import verifyObject
#from zope.interface.verify import verifyClass
#
#from voteit.core.models.agenda_item import AgendaItem
#from voteit.core.models.meeting import Meeting
#from voteit.core.models.poll import Poll
#from voteit.core.models.poll_plugin import PollPlugin
#from voteit.core.models.proposal import Proposal
#from voteit.core.models.interfaces import IPollPlugin
#from voteit.core.models.interfaces import IVote
#from voteit.core.security import unrestricted_wf_transition_to
#from voteit.core.testing_helpers import bootstrap_and_fixture
#
#
#class CombinedSimplePollTests(unittest.TestCase):
#
#    def setUp(self):
#        request = testing.DummyRequest()
#        self.config = testing.setUp(request = request)
#
#    def tearDown(self):
#        testing.tearDown()
#    
#    @property
#    def _cut(self):
#        from .models import CombinedSimplePoll
#        return CombinedSimplePoll
#
#    def test_verify_class(self):
#        self.failUnless(verifyClass(IPollPlugin, self._cut))
#
#    def test_verify_object(self):
#        self.failUnless(verifyObject(IPollPlugin, self._cut(None)))
