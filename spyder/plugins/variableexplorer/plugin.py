# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
# (see spyder/__init__.py for details)

"""
Variable Explorer Plugin.
"""

# Local imports
from spyder.api.plugins import Plugins, SpyderDockablePlugin
from spyder.api.plugin_registration.decorators import (
    on_plugin_available, on_plugin_teardown)
from spyder.api.shellconnect.mixins import ShellConnectMixin
from spyder.api.translations import get_translation
from spyder.plugins.variableexplorer.confpage import (
    VariableExplorerConfigPage)
from spyder.plugins.variableexplorer.widgets.main_widget import (
    VariableExplorerWidget)


# Localization
_ = get_translation('spyder')


class VariableExplorer(SpyderDockablePlugin, ShellConnectMixin):
    """
    Variable explorer plugin.
    """
    NAME = 'variable_explorer'
    REQUIRES = [Plugins.IPythonConsole, Plugins.Preferences]
    TABIFY = None
    WIDGET_CLASS = VariableExplorerWidget
    CONF_SECTION = NAME
    CONF_FILE = False
    CONF_WIDGET_CLASS = VariableExplorerConfigPage
    DISABLE_ACTIONS_WHEN_HIDDEN = False

    # ---- SpyderDockablePlugin API
    # ------------------------------------------------------------------------
    @staticmethod
    def get_name():
        return _('Variable explorer')

    def get_description(self):
        return _('Display, explore load and save variables in the current '
                 'namespace.')

    def get_icon(self):
        return self.create_icon('dictedit')

    def on_initialize(self):
        self.get_widget().sig_free_memory_requested.connect(
            self.sig_free_memory_requested)

    @on_plugin_available(plugin=Plugins.Preferences)
    def on_preferences_available(self):
        preferences = self.get_plugin(Plugins.Preferences)
        preferences.register_plugin_preferences(self)

    @on_plugin_teardown(plugin=Plugins.Preferences)
    def on_preferences_teardown(self):
        preferences = self.get_plugin(Plugins.Preferences)
        preferences.deregister_plugin_preferences(self)

    # ---- Public API
    # ------------------------------------------------------------------------
    def on_connection_to_external_spyder_kernel(self, shellwidget):
        """Send namespace view settings to the kernel."""
        widget = self.get_widget_for_shellwidget(shellwidget)
        if widget is None:
            return
        widget.set_namespace_view_settings()
        widget.refresh_namespacebrowser()
