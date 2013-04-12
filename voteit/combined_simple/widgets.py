from deform.widget import RadioChoiceWidget


class YesNoAbstainWidget(RadioChoiceWidget):
    """ VoteIT poll style widget
    """
    template = 'yes_no_abstain'
    readonly_template = 'yes_no_abstain_readonly'

#    def __init__(self, **kw):
#        super(YesNoAbstainWidget, self).__init__(**kw)
