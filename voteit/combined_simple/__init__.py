from pkg_resources import resource_filename
from pyramid.i18n import TranslationStringFactory


PROJECTNAME = 'voteit.combined_simple'
CombinedTSF = TranslationStringFactory(PROJECTNAME)


def includeme(config):
    config.add_translation_dirs('%s:locale/' % PROJECTNAME)
    from .models import CombinedSimplePoll
    config.registry.registerAdapter(CombinedSimplePoll, name = CombinedSimplePoll.name)

    from voteit.core.deform_bindings import append_search_path
    widgets_path = resource_filename('voteit.combined_simple', 'templates/widgets')
    append_search_path(widgets_path)
