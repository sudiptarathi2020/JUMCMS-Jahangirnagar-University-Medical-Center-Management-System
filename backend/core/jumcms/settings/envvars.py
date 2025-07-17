from core.general.utils.collections import deep_update
from core.general.utils.settings import get_settings_from_environment
from core.jumcms.settings import ENVVAR_SETTINGS_PREFIX

deep_update(globals(), get_settings_from_environment(ENVVAR_SETTINGS_PREFIX))