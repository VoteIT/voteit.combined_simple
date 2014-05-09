import colander
import deform
from repoze.catalog.query import Any
from pyramid.renderers import render
#from pyramid.response import Response
from pyramid.traversal import find_root

from voteit.core.models.poll_plugin import PollPlugin

from . import CombinedTSF as _
from .widgets import CombinedSimpleWidget


class CombinedSimplePoll(PollPlugin):
    """ Poll plugin for combined simple polls. """
    name = u'combined_simple'
    title = _(u"Combined simple")
    description = _(u"combined_simple_description", 
                    default = u"Users may vote Approve / Deny / Abstain on each proposal within this poll, "
                              u"and each will be treated individually.")
    
    def get_vote_schema(self, request = None, api = None):
        """ Get an instance of the schema that this poll uses.
        """
        root = find_root(self.context)
        get_metadata = root.catalog.document_map.get_metadata
        num, results = root.catalog.query(Any('uid', self.context.proposal_uids), sort_index = 'created')
        proposals = [get_metadata(x) for x in results]
        #Choices should be something iterable with the contents [(UID for proposal, Title of proposal), <etc...>, ]
        poll_wf_state = self.context.get_workflow_state()
        if poll_wf_state == 'ongoing':
            poll_title = _(u"Vote")
        else:
            poll_title = _(u"You can't change your vote now.")
        schema = colander.Schema(title = poll_title)
        choices = (('approve', _(u"Approve")), ('deny', _(u"Deny")), ('abstain', _(u"Abstain")))
        for proposal in proposals:
            schema.add(colander.SchemaNode(colander.String(),
                                           name = proposal['uid'],
                                           missing = u"",
                                           title = proposal['title'],
                                           validator = colander.OneOf([x[0] for x in choices]),
                                           widget = CombinedSimpleWidget(values = choices,
                                                                       proposal = proposal,
                                                                       api = api,)))
        return schema

    def handle_close(self):
        """ Calculate the result of the ballots
        """
        ballots = self.context.ballots
        results = {}
        valid_choices = ('approve', 'deny', 'abstain')
        if ballots:
            for (ballot, count) in ballots:
                for (p_uid, choice) in ballot.items():
                        prop = results.setdefault(p_uid, {u'approve': 0, u'deny': 0, u'abstain': 0})
                        if choice in valid_choices:
                            prop[choice] += count
        self.context.poll_result = results
        
    def render_result(self, request, api, complete=True):
        get_metadata = api.root.catalog.document_map.get_metadata
        results = api.root.catalog.query(Any('uid', self.context.proposal_uids), sort_index = 'created')[1]
        response = {}
        response['proposals'] = [get_metadata(x) for x in results]
        response['api'] = api
        response['context'] = self.context
        response['complete'] = complete
        return render('templates/result.pt', response, request=request)

    def change_states_of(self):
        results = {}
        for (uid, result) in self.context.poll_result.items():
            if result['approve'] > result['deny']:
                results[uid] = 'approved'
            if result['deny'] > result['approve']:
                results[uid] = 'denied'
        return results
