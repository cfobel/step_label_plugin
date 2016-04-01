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
from flatland import Form, String
from microdrop.app_context import get_app
from microdrop.plugin_helpers import StepOptionsController, get_plugin_info
from microdrop.plugin_manager import (PluginGlobals, Plugin, IPlugin,
                                      emit_signal, implements)
from path_helpers import path
import gtk

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
        self.initialized = False
        self.label_most_recent_step_label = None
        self.label_next_step_label = None

    def on_plugin_enable(self):
        if not self.initialized:
            self.add_labels()
            self.initialized = True

    def on_plugin_disable(self):
        if self.initialized:
            self.remove_labels()

    def add_labels(self):
        app = get_app()
        self.label_most_recent_step_label = gtk.Label()
        (self.label_most_recent_step_label
         .set_name('label_most_recent_step_label'))
        self.label_next_step_label = gtk.Label()
        self.label_next_step_label.set_name('label_next_step_label')
        for label_i in (self.label_most_recent_step_label,
                        self.label_next_step_label):
            app.main_window_controller.box_step.pack_start(child=label_i,
                                                           expand=False,
                                                           fill=False,
                                                           padding=5)
            label_i.show()

    def remove_labels(self):
        app = get_app()
        for child_i in app.main_window_controller.box_step.get_children():
            if any([child_i is self.label_most_recent_step_label,
                    child_i is self.label_next_step_label]):
                app.main_window_controller.box_step.remove(child_i)
        self.label_most_recent_step_label = None
        self.label_next_step_label = None

    def update_nearest_step_labels(self):
        app = get_app()
        step_i = app.protocol.current_step_number

        i, most_recent_step_label = self.find_most_recent_step_label()

        (self.label_most_recent_step_label
         .set_markup('<b>Most recent step label:</b> {}{}'
                     .format(most_recent_step_label,
                             ' ({})'.format(i) if all([i is not None,
                                                       i != step_i])
                             else '')))

        i, next_step_label = self.find_next_step_label()
        self.label_next_step_label.set_markup('<b>Next step label:</b> {}{}'
                                                .format(next_step_label,
                                                        ' ({})'.format(i)
                                                        if i is not None
                                                        else ''))

    def on_step_options_changed(self, *args):
        self.update_nearest_step_labels()

    def on_step_swapped(self, *args):
        self.update_nearest_step_labels()

    def find_most_recent_step_label(self):
        app = get_app()
        for i in xrange(app.protocol.current_step_number, -1, -1):
            most_recent_step_label = self.get_step_value('label', step_number=i)
            if most_recent_step_label:
                return i, most_recent_step_label
        else:
            return None, ''

    def find_next_step_label(self):
        app = get_app()
        for i in xrange(app.protocol.current_step_number + 1, len(app.protocol.steps)):
            next_step_label = self.get_step_value('label', step_number=i)
            if next_step_label:
                return i, next_step_label
        else:
            return None, ''


PluginGlobals.pop_env()
