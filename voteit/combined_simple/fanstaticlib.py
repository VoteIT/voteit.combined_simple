from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource

from voteit.core.fanstaticlib import voteit_common_js

cs_lib = Library('combined_simple', 'static')
cs_styles = Resource(cs_lib, 'styles.css')
cs_script = Resource(cs_lib, 'script.js', depends = (voteit_common_js,))
cs_group = Group((cs_styles, cs_script))


def includeme(config):
    """ Include fanstatic resources. """
    from voteit.core.models.interfaces import IFanstaticResources
    from voteit.core.fanstaticlib import is_agenda_item
    util = config.registry.getUtility(IFanstaticResources)
    util.add('combined_simple_group', cs_group, is_agenda_item)
