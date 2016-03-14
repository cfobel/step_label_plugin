# `step_label_plugin` #

Assign a label to each step in [MicroDrop][1] protocol.

## Usage ##

 - Set label value in protocol grid in MicroDrop.
 - Label for current step can be looked up programmatically by another plugin:

        >>> from microdrop.plugin_manager import get_service_names, get_service_instance_by_name
        >>> get_service_names()
        [..., 'wheelerlab.step_label_plugin', ...]
        >>> step_plugin = get_service_instance_by_name('wheelerlab.step_label_plugin')
        >>># Get options for current step.
        >>> step_plugin.get_step_options()
        {'label': u'dispense'}
        >>># Get options for step with specified index (e.g., step 2).
        >>> step_plugin.get_step_options(2)
        {'label': u'merge'}

# Credits #

Christian Fobel <christian@fobel.net>

# Help #

For help, please post to the [DropBot][2] developers [Google Group][3].


[1]: http://microfluidics.utoronto.ca/microdrop
[2]: http://microfluidics.utoronto.ca/dropbot/
[3]: https://groups.google.com/forum/#!forum/dropbot-dev
