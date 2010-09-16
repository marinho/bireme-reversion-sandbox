from django.db.models import ForeignKey
from django.forms import Field as FormField, Widget

from reversion.models import Version

class ReversionForeignKey(ForeignKey):
    def __init__(self, to, **kwargs):
        """Here we must to store indirect object type to use it later"""

        self.indirect_to = to
        self.indirect_kwargs = {
            'db_index': kwargs.pop('db_index', None),
            }

        super(ReversionForeignKey, self).__init__(Version, **kwargs)

    def contribute_to_class(self, cls, name): # FIXME
        raise Exception(cls, name)

    def __set__(self, instance, value): # FIXME
        """Here we have to store the referenced object in a temporary attribute of
        instance and set a temporary Version instance to the field."""

        raise Exception('x')
        
        instance._indirect_references = getattr(instance, '_indirect_references', {})
        instance._indirect_references[self] = value

        setattr(instance, self.field.get_cache_name(), Version())

class ReversionChoiceField(FormField):
    pass

class ReversionChoiceWidget(Widget):
    pass


