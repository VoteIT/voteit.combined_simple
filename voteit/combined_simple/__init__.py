from pyramid.i18n import TranslationStringFactory


PROJECTNAME = 'voteit.combined_simple'
_ = TranslationStringFactory(PROJECTNAME)


def includeme(config):
    config.add_translation_dirs('%s:locale/' % PROJECTNAME)
    from pyramid_deform import configure_zpt_renderer
    configure_zpt_renderer(['voteit.combined_simple:templates/widgets'])
    config.include('.models')
