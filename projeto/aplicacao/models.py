import datetime
from django.db import models

class Instituicao(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.TextField(blank=True, default='')
    
    def __unicode__(self):
        return self.nome

class Documento(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, default='')
    valor = models.DecimalField(max_digits=12, decimal_places=2)
    logico = models.BooleanField(default=False, blank=True)
    inteiro = models.IntegerField()
    data = models.DateField(default=datetime.date.today, blank=True)
    datahora = models.DateTimeField(default=datetime.datetime.now, blank=True)

    def __unicode__(self):
        return self.titulo

