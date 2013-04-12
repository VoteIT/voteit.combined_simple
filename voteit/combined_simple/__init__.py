from pyramid.i18n import TranslationStringFactory


PROJECTNAME = 'voteit.combined_simple'
CombinedTSF = TranslationStringFactory(PROJECTNAME)


def includeme(config):
    config.add_translation_dirs('%s:locale/' % PROJECTNAME)

    from .models import CombinedSimplePoll
    config.registry.registerAdapter(CombinedSimplePoll, name = CombinedSimplePoll.name)
