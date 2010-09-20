import datetime

from django.db import models, connection
from django.core.management.color import no_style
from django.contrib.flatpages.models import FlatPage
from django.contrib.contenttypes import generic
from django.db.models.sql.query import setup_join_cache
from django.contrib.auth.models import User

from reversion.revisions import revision
from reversion_relations.fields import ReversionForeignKey

class Supplier(models.Model):
    class Meta:
        app_label = 'reversion_relations'

    name = models.CharField(max_length=100)
    location = models.TextField(blank=True)
    salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    starred = models.BooleanField(default=False, blank=True)
    points = models.IntegerField(default=0, blank=True)
    date_foundation = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.name

class Purchase(models.Model):
    class Meta:
        app_label = 'reversion_relations'

    date = models.DateTimeField(blank=True, default=datetime.datetime.now)
    supplier = ReversionForeignKey(Supplier, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)

setup_join_cache(Supplier)
setup_join_cache(Purchase)

def create_tables():
    cursor = connection.cursor()
    style = no_style()
    tables = connection.introspection.table_names()
    seen_models = connection.introspection.installed_models(tables)

    sql, references = connection.creation.sql_create_model(Supplier, style, seen_models)
    new_sql, new_ref = connection.creation.sql_create_model(Purchase, style, seen_models)
    sql.extend(new_sql); references.update(new_ref)

    pending_references = {}
    for refto, refs in references.items():
        pending_references.setdefault(refto, []).extend(refs)
        if refto in seen_models:
            sql.extend(connection.creation.sql_for_pending_references(refto, style, pending_references))
    sql.extend(connection.creation.sql_for_pending_references(Supplier, style, pending_references))
    sql.extend(connection.creation.sql_for_pending_references(Purchase, style, pending_references))
    for statement in sql:
        cursor.execute(statement)

if not revision.is_registered(Supplier): revision.register(Supplier)
if not revision.is_registered(Purchase): revision.register(Purchase)

