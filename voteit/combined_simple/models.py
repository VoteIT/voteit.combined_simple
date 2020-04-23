import colander
import deform
from deform.widget import RadioChoiceWidget
from pyramid.renderers import render
from voteit.core.models.poll_plugin import PollPlugin

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
    name = 'combined_simple'
    title = _("Combined simple")
    description = _("combined_simple_description",
                    default="Users may vote Approve / Deny / Abstain on each proposal within this poll, "
                            "and each will be treated individually. "
                            "Remember that you can't use this method to determine "
                            "order or to for instance elect a board.")
    multiple_winners = True
    recommended_for = _("recommended_for",
                        default="Situations where each individual proposal could "
                                "be approved or rejected independent of each other.")
    priority = 100

    def get_vote_schema(self):
        """ Get an instance of the schema that this poll uses.
        """
        proposals = self.context.get_proposal_objects()
        # Choices should be something iterable with the contents [(UID for proposal, Title of proposal), <etc...>, ]
        poll_wf_state = self.context.get_workflow_state()
        if poll_wf_state == 'ongoing':
            poll_title = _(u"Vote")
        else:
            poll_title = _(u"You can't change your vote now.")
        schema = colander.Schema(
            title=poll_title,
            widget=deform.widget.FormWidget(
                template='form_modal',
                readonly_template='readonly/form_modal'
            )
        )
        for proposal in proposals:
            schema.add(colander.SchemaNode(
                colander.String(),
                name=proposal.uid,
                missing=u"",
                title="#%s" % proposal.aid,
                validator=colander.OneOf([x[0] for x in _CHOICES]),
                proposal=proposal,
                widget=RadioChoiceWidget(
                    values=_CHOICES,
                    choice_text_class=_CHOICE_TEXT_CLASS,
                    choice_icon=_CHOICE_ICON,
                    template='combined_simple',
                    readonly_template='combined_simple_readonly')
            ))
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
    config.registry.registerAdapter(CombinedSimplePoll, name=CombinedSimplePoll.name)
