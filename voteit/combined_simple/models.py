import colander
import deform
from repoze.catalog.query import Any
from pyramid.renderers import render
from pyramid.traversal import find_root, find_resource
from voteit.core.models.poll_plugin import PollPlugin
from deform.widget import RadioChoiceWidget

from voteit.combined_simple import _


_CHOICES = (('approve', _(u"Approve")), ('deny', _(u"Deny")), ('abstain', _(u"Abstain")))
_CHOICE_ICON = {'approve': 'glyphicon glyphicon-approved',
                'deny': 'glyphicon glyphicon-denied',
                'abstain': 'glyphicon glyphicon-canceled'}
_CHOICE_TEXT_CLASS = {'approve': 'text-success',
                      'deny': 'text-danger',
                      'abstain': 'text-warning'}


class CombinedSimplePoll(PollPlugin):
    """ Poll plugin for combined simple polls. """
    name = u'combined_simple'
    title = _(u"Combined simple")
    description = _(u"combined_simple_description", 
                    default = u"Users may vote Approve / Deny / Abstain on each proposal within this poll, "
                              u"and each will be treated individually.")
    
    def get_vote_schema(self):
        """ Get an instance of the schema that this poll uses.
        """
        proposals = self.context.get_proposal_objects()
        #Choices should be something iterable with the contents [(UID for proposal, Title of proposal), <etc...>, ]
        poll_wf_state = self.context.get_workflow_state()
        if poll_wf_state == 'ongoing':
            poll_title = _(u"Vote")
        else:
            poll_title = _(u"You can't change your vote now.")
        schema = colander.Schema(title = poll_title,
                                 widget = deform.widget.FormWidget(template = 'form_modal',
                                                                   readonly_template = 'readonly/form_modal'))
        for proposal in proposals:
            schema.add(colander.SchemaNode(colander.String(),
                                           name = proposal.uid,
                                           missing = u"",
                                           title = proposal.title,
                                           validator = colander.OneOf([x[0] for x in _CHOICES]),
                                           widget = RadioChoiceWidget(values = _CHOICES,
                                                                      proposal = proposal,
                                                                      choice_text_class = _CHOICE_TEXT_CLASS,
                                                                      choice_icon = _CHOICE_ICON,
                                                                      template = 'combined_simple',
                                                                      readonly_template = 'combined_simple_readonly')))
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
        
    def render_result(self, view):
        response = {}
        response['proposals'] = self.context.get_proposal_objects()
        response['context'] = self.context

        return render('voteit.combined_simple:templates/result.pt', response, request=view.request)

    def change_states_of(self):
        results = {}
        for (uid, result) in self.context.poll_result.items():
            if result['approve'] > result['deny']:
                results[uid] = 'approved'
            if result['deny'] > result['approve']:
                results[uid] = 'denied'
        return results


def includeme(config):
    config.registry.registerAdapter(CombinedSimplePoll, name = CombinedSimplePoll.name)