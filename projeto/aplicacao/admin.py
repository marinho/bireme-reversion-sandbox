from django.contrib import admin

from reversion.admin import VersionAdmin

from models import Instituicao, Documento

class AdminInstituicao(VersionAdmin):
    pass

class AdminDocumento(VersionAdmin):
    pass

admin.site.register(Instituicao, AdminInstituicao)
admin.site.register(Documento, AdminDocumento)

