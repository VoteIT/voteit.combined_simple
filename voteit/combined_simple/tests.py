import unittest

import colander
from pyramid import testing
from zope.interface.verify import verifyObject
from zope.interface.verify import verifyClass

from voteit.core.models.agenda_item import AgendaItem
from voteit.core.models.meeting import Meeting
from voteit.core.models.poll import Poll
from voteit.core.models.poll_plugin import PollPlugin
from voteit.core.models.proposal import Proposal
from voteit.core.models.interfaces import IPollPlugin
from voteit.core.models.interfaces import IVote
from voteit.core.security import unrestricted_wf_transition_to
from voteit.core.views.api import APIView
from voteit.core.testing_helpers import active_poll_fixture


class CombinedSimplePollTests(unittest.TestCase):

    def setUp(self):
        request = testing.DummyRequest()
        self.config = testing.setUp(request = request)

    def tearDown(self):
        testing.tearDown()
    
    @property
    def _cut(self):
        from .models import CombinedSimplePoll
        return CombinedSimplePoll

    def _fixture(self):
        self.config.include('voteit.core.models.fanstatic_resources')
        self.config.include('voteit.core.testing_helpers.register_catalog')
        self.config.include('voteit.combined_simple')
        self.config.testing_securitypolicy(userid='mr_tester')
        root = active_poll_fixture(self.config)
        self.config.include('voteit.core.testing_helpers.register_security_policies')
        poll = root['meeting']['ai']['poll']
        poll.set_field_value('poll_plugin', 'combined_simple')
        return poll

    def _add_votes(self, poll):
        from voteit.core.models.vote import Vote
        ai = poll.__parent__
        p1_uid = ai['prop1'].uid
        p2_uid = ai['prop2'].uid
        v1 = Vote(creators = ['one'])
        v1.set_vote_data({p1_uid: u'abstain', p2_uid: u'approve'}, notify = False)
        poll['v1'] = v1
        v2 = Vote(creators = ['two'])
        v2.set_vote_data({p1_uid: u'approve', p2_uid: u'deny'}, notify = False)
        poll['v2'] = v2
        v3 = Vote(creators = ['three'])
        v3.set_vote_data({p1_uid: u'approve'}, notify = False)
        poll['v3'] = v3
        v4 = Vote(creators = ['four'])
        v4.set_vote_data({p1_uid: u'approve'}, notify = False)
        poll['v4'] = v4

    def test_verify_class(self):
        self.failUnless(verifyClass(IPollPlugin, self._cut))

    def test_verify_object(self):
        self.failUnless(verifyObject(IPollPlugin, self._cut(None)))

    def test_integration(self):
        self.config.include('voteit.core')
        self.config.include('voteit.combined_simple')
        poll = Poll()
        self.failUnless(self.config.registry.queryAdapter(poll, IPollPlugin, name = u'combined_simple'))

    def test_get_vote_schema(self):
        poll = self._fixture()
        obj = self._cut(poll)
        schema = obj.get_vote_schema()
        self.assertEqual(len(schema.children), 2) #2 proposals in fixture

    def test_handle_close(self):
        poll = self._fixture()
        obj = self._cut(poll)
        self._add_votes(poll)
        request = testing.DummyRequest()
        unrestricted_wf_transition_to(poll, 'ongoing')
        unrestricted_wf_transition_to(poll, 'closed')
        ai = poll.__parent__
        p1_uid = ai['prop1'].uid
        p2_uid = ai['prop2'].uid
        expected = {p1_uid: {u'approve': 3, u'abstain': 1, u'deny': 0}, p2_uid: {u'approve': 1, u'abstain': 0, u'deny': 1}}
        self.assertEqual(poll.poll_result, expected)

    def test_render_result(self):
        self.config.scan('voteit.core.views.components')
        poll = self._fixture()
        obj = self._cut(poll)
        self._add_votes(poll)
        request = testing.DummyRequest()
        unrestricted_wf_transition_to(poll, 'ongoing')
        unrestricted_wf_transition_to(poll, 'closed')
        ai = poll.__parent__
        p1_uid = ai['prop1'].uid
        p2_uid = ai['prop2'].uid
        request = testing.DummyRequest()
        api = APIView(poll, request)
        result = obj.render_result(request, api)
        self.assertIn('Proposal 1', result)

    def test_change_states_of(self):
        self.config.scan('voteit.core.views.components')
        poll = self._fixture()
        ai = poll.__parent__
        p1_uid = ai['prop1'].uid
        obj = self._cut(poll)
        self._add_votes(poll)
        unrestricted_wf_transition_to(poll, 'ongoing')
        unrestricted_wf_transition_to(poll, 'closed')
        result = obj.change_states_of()
        self.assertEqual(result, {p1_uid: 'approved'})

    def test_change_states_no_vote(self):
        self.config.scan('voteit.core.views.components')
        poll = self._fixture()
        ai = poll.__parent__
        p1_uid = ai['prop1'].uid
        p2_uid = ai['prop2'].uid
        obj = self._cut(poll)
        self._add_votes(poll)
        poll['v3'].set_vote_data({p2_uid: u'deny'}, notify = False)
        poll['v4'].set_vote_data({p2_uid: u'deny'}, notify = False)
        unrestricted_wf_transition_to(poll, 'ongoing')
        unrestricted_wf_transition_to(poll, 'closed')

        result = obj.change_states_of()
        self.assertEqual(result, {p1_uid: 'approved', p2_uid: 'denied'})

