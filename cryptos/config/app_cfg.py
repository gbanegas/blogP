# -*- coding: utf-8 -*-
"""
Global configuration file for TG2-specific settings in CryptoS.

This file complements development/deployment.ini.

"""

from tg.configuration import AppConfig

import cryptos
from cryptos import model
from cryptos.lib import app_globals, helpers 

base_config = AppConfig()
base_config.renderers = []

# True to prevent dispatcher from striping extensions
# For example /socket.io would be served by "socket_io" method instead of "socket"
base_config.disable_request_extensions = False

# Set None to disable escaping punctuation characters to "_" when dispatching methods.
# Set to a function to provide custom escaping.
base_config.dispatch_path_translator = True 
base_config.prefer_toscawidgets2 = True

base_config.package = cryptos

#Enable json in expose
base_config.renderers.append('json')
#Enable genshi in expose to have a lingua franca for extensions and pluggable apps
#you can remove this if you don't plan to use it.
base_config.renderers.append('genshi')

#Set the default renderer
base_config.default_renderer = 'genshi'
# if you want raw speed and have installed chameleon.genshi
# you should try to use this renderer instead.
# warning: for the moment chameleon does not handle i18n translations
#base_config.renderers.append('chameleon_genshi')
base_config.use_sqlalchemy=False
base_config.use_ming=False
base_config.use_transaction_manager=False
base_config.auth_backend=None
base_config.use_toscawidgets=False
try:
    # Enable DebugBar if available, install tgext.debugbar to turn it on
    from tgext.debugbar import enable_debugbar
    enable_debugbar(base_config)
except ImportError:
    pass
