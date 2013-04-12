#import colander
#from pyramid.renderers import render
#from pyramid.response import Response
from voteit.core.models.poll_plugin import PollPlugin


class CombinedSimplePoll(PollPlugin):
    """ Poll plugin for combined simple polls. """
    name = u'combined_simple'
    title = _(u"Combined simple")
    description = _(u"combined_simple_description", 
                    default = u"Users may vote Yes / No / Abstain on each proposal within this poll, "
                              u"and each will be treated individually.")
