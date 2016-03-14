"""
Copyright 2016 Christian Fobel

This file is part of step_label_plugin.

step_label_plugin is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

step_label_plugin is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with step_label_plugin.  If not, see <http://www.gnu.org/licenses/>.
"""
from path_helpers import path
from flatland import Form, String
from microdrop.plugin_helpers import StepOptionsController, get_plugin_info
from microdrop.plugin_manager import (PluginGlobals, Plugin, IPlugin,
                                      implements)

PluginGlobals.push_env('microdrop.managed')

class Step_Label_Plugin(Plugin, StepOptionsController):
    """
    This class is automatically registered with the PluginManager.
    """
    implements(IPlugin)
    version = get_plugin_info(path(__file__).parent).version
    plugin_name = get_plugin_info(path(__file__).parent).plugin_name

    '''
    StepFields
    ---------

    A flatland Form specifying the per step options for the current plugin.
    Note that nested Form objects are not supported.

    Since we subclassed StepOptionsController, an API is available to access and
    modify these attributes.  This API also provides some nice features
    automatically:
        -all fields listed here will be included in the protocol grid view
            (unless properties=dict(show_in_gui=False) is used)
        -the values of these fields will be stored persistently for each step
    '''
    StepFields = Form.of(String.named('label').using(optional=True,
                                                     default=''))

    def __init__(self):
        self.name = self.plugin_name


PluginGlobals.pop_env()
