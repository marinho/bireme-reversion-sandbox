from django.db.models.base import ModelBase
from django.db.models import ForeignKey, Field
from django.db.models.fields.related import ReverseSingleRelatedObjectDescriptor, RelatedField
from django.forms import Field as FormField, Widget
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers

from reversion.models import Version, Revision
from reversion.revisions import revision

class ReversionForeignKey(ForeignKey):
    def __init__(self, to, **kwargs):
        """Here we must to store indirect object type to use it later"""

        self.indirect_to = to
        self.indirect_kwargs = {
            'db_index': kwargs.pop('db_index', None),
            }

        super(ReversionForeignKey, self).__init__(Version, **kwargs)

    def contribute_to_class(self, cls, name):
        super(ReversionForeignKey, self).contribute_to_class(cls, name)

        # Replaces field descriptor
        setattr(cls, self.name, ReversionRelatedObjectDescriptor(self))

    def pre_save(self, model_instance, add):
        try:
            obj = model_instance._indirect_references.get(self, None)
        except AttributeError:
            obj = None

        if not obj: return None

        # Gets the latest version of this object
        c_type = ContentType.objects.get_for_model(self.indirect_to)

        try:
            version = Version.objects.filter(content_type=c_type, object_id=obj.pk).latest('pk')
        except ObjectDoesNotExist:
            # If there is no version available, creates one
            revision.start()
            obj.save()
            revision.end()

            version = Version.objects.filter(content_type=c_type, object_id=obj.pk).latest('pk')

            """new_revision = Revision.objects.create(user=revision._state.user, comment=revision._state.comment)

            registration_info = revision.get_registration_info(obj.__class__)
            serialized_data = serializers.serialize(registration_info.format, [obj], fields=registration_info.fields)

            version = Version.objects.create(
                    revision=new_revision,
                    content_type=c_type,
                    object_id=obj.pk,
                    format=registration_info.format,
                    serialized_data=serialized_data,
                    object_repr=unicode(obj),
                    )"""

        # Returns version's id
        return version.pk

class ReversionRelatedObjectDescriptor(ReverseSingleRelatedObjectDescriptor):
    """Take more details from the superclass."""

    def __init__(self, field_with_rel):
        self.field = field_with_rel    

    def __get__(self, instance, instance_type=None):
        if instance is None:
            return self

        cache_name = self.field.get_cache_name()
        
        try:
            value = getattr(instance, cache_name)
        except AttributeError:
            value = None

        if isinstance(value, Version):
            value = ReversionProxy(value)
        
        return value
    
    def __set__(self, instance, value):
        """Here we have to store the referenced object in a temporary attribute of
        instance and set a temporary Version instance to the field."""

        instance._indirect_references = getattr(instance, '_indirect_references', {})
        instance._indirect_references[self.field] = value

        if value:
            setattr(instance, self.field.attname, value.pk)
            setattr(instance, self.field.get_cache_name(), value)
        else:
            setattr(instance, self.field.attname, None)
            setattr(instance, self.field.get_cache_name(), None)

class ReversionProxy(object):
    version = None

    def __init__(self, version=None):
        self.version = version

class ReversionChoiceField(FormField):
    pass

class ReversionChoiceWidget(Widget):
    pass


