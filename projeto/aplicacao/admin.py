from django.contrib import admin

from reversion.admin import VersionAdmin

from models import Supplier, Purchase

class AdminSupplier(VersionAdmin):
    pass

class AdminPurchase(VersionAdmin):
    list_display = ('date','supplier','user')

admin.site.register(Supplier, AdminSupplier)
admin.site.register(Purchase, AdminPurchase)

