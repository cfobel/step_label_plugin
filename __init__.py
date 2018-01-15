from flatland import Form, String
from microdrop.app_context import get_app
from microdrop.plugin_helpers import StepOptionsController, get_plugin_info
from microdrop.plugin_manager import (PluginGlobals, Plugin, IPlugin,
                                      implements)
from path_helpers import path
from pygtkhelpers.gthreads import gtk_threadsafe
import gtk

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

PluginGlobals.push_env('microdrop.managed')


class StepLabelPlugin(Plugin, StepOptionsController):
    """
    This class is automatically registered with the PluginManager.
    """
    implements(IPlugin)
    version = __version__
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

    @gtk_threadsafe
    def add_labels(self):
        '''
        .. versionchanged:: 2.1.3
            Wrap with :func:`gtk_threadsafe` decorator to ensure the code runs
            in the main GTK thread.
        '''
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

    @gtk_threadsafe
    def remove_labels(self):
        '''
        .. versionchanged:: 2.1.3
            Wrap with :func:`gtk_threadsafe` decorator to ensure the code runs
            in the main GTK thread.
        '''
        app = get_app()
        for child_i in app.main_window_controller.box_step.get_children():
            if any([child_i is self.label_most_recent_step_label,
                    child_i is self.label_next_step_label]):
                app.main_window_controller.box_step.remove(child_i)
        self.label_most_recent_step_label = None
        self.label_next_step_label = None

    @gtk_threadsafe
    def update_nearest_step_labels(self, step_i):
        '''
        .. versionchanged:: 2.1.3
            Add :data:`step_i` parameter.

            Wrap with :func:`gtk_threadsafe` decorator to ensure the code runs
            in the main GTK thread.

        .. versionchanged:: 2.2.1
            Add missing :data:`step_i` argument to fix call to
            :meth:`find_next_step_label`.

        Parameters
        ----------
        step_i : int
            Step number to find labels relative to.
        '''
        i, most_recent_step_label = self.find_most_recent_step_label(step_i)
        offset_str = (' ({}{})'.format('+' if i > step_i else '', i - step_i)
                      if all([i is not None, i != step_i]) else '')
        (self.label_most_recent_step_label
         .set_markup('<b>Most recent step label:</b>\n{}{}'
                     .format(most_recent_step_label, offset_str)))

        i, next_step_label = self.find_next_step_label(step_i)
        offset_str = (' ({}{})'.format('+' if i > step_i else '', i - step_i)
                      if i is not None else '')
        self.label_next_step_label.set_markup('<b>Next step label:</b>\n{}{}'
                                              .format(next_step_label,
                                                      offset_str))

    def on_step_options_changed(self, *args):
        '''
        .. versionchanged:: 2.1.3
            Pass current step number to as argument to
            :meth:`update_nearest_step_labels`.
        '''
        app = get_app()
        step_i = app.protocol.current_step_number
        self.update_nearest_step_labels(step_i)

    def on_step_swapped(self, *args):
        '''
        .. versionchanged:: 2.1.3
            Pass current step number to as argument to
            :meth:`update_nearest_step_labels`.
        '''
        app = get_app()
        step_i = app.protocol.current_step_number
        self.update_nearest_step_labels(step_i)

    def find_most_recent_step_label(self, step_i):
        '''
        .. versionchanged:: 2.1.3
            Add :data:`step_i` parameter.

        Parameters
        ----------
        step_i : int
            Step number to find labels relative to.
        '''
        for i in xrange(step_i, -1, -1):
            most_recent_step_label = self.get_step_value('label',
                                                         step_number=i)
            if most_recent_step_label:
                return i, most_recent_step_label
        else:
            return None, ''

    def find_next_step_label(self, step_i):
        '''
        .. versionchanged:: 2.1.3
            Add :data:`step_i` parameter.

        Parameters
        ----------
        step_i : int
            Step number to find labels relative to.
        '''
        app = get_app()
        for i in xrange(step_i + 1, len(app.protocol.steps)):
            next_step_label = self.get_step_value('label', step_number=i)
            if next_step_label:
                return i, next_step_label
        else:
            return None, ''


PluginGlobals.pop_env()
