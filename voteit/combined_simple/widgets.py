from deform.widget import RadioChoiceWidget


class CombinedSimpleWidget(RadioChoiceWidget):
    """ VoteIT poll style widget
    """
    template = 'combined_simple'
    readonly_template = 'combined_simple_readonly'
