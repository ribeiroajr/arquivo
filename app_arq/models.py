from django.db import models
from django.contrib.auth.models import User

class Status(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=10, verbose_name="Status", null=True)

    create_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.status)
    
    class Meta:
        verbose_name = 'Statu'
        verbose_name_plural = 'Status'
        ordering = ['id']

class Tcu(models.Model):
    id = models.AutoField(primary_key=True)
    tcu = models.CharField(max_length=50, verbose_name="Numero", null=True)
    tcu_desc = models.CharField(max_length=200, verbose_name="Descrição", null=True)

    create_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.tcu)
    
    class Meta:
        verbose_name = 'TCU'
        verbose_name_plural = 'TCUs'
        ordering = ['id']
    
class Om(models.Model):
    id = models.AutoField(primary_key=True)
    om = models.CharField(max_length=20, verbose_name="OM", null=True)
    om_descricao = models.CharField(max_length=200, verbose_name="OM Descrição", null=True)

    create_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.om)
    
    class Meta:
        verbose_name = 'OM'
        verbose_name_plural = 'OMs'
        ordering = ['id']
    
class Tipo(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=50, verbose_name="Tipo", null=True)
    tipo_desc = models.CharField(max_length=200, verbose_name="Tipo Descrição", null=True)

    create_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.tipo)
    
    class Meta:
        verbose_name = 'TIPO'
        verbose_name_plural = 'TIPOS'
        ordering = ['id']
    
class Ano(models.Model):
    id = models.AutoField(primary_key=True)
    ano = models.CharField(max_length=10, verbose_name="Ano", null=True)

    create_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.ano)
    
    class Meta:
        verbose_name = 'ANO'
        verbose_name_plural = 'ANOS'
        ordering = ['id']
    
class Caixa(models.Model):
    id = models.AutoField(primary_key=True)
    fk_ano = models.ForeignKey(Ano, on_delete=models.CASCADE, verbose_name="ANO", null=True, blank=True)
    fk_status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name="Status da caixa", null=True, blank=True)
    caixa = models.CharField(max_length=10, verbose_name="Caixa", null=True)
    caixa_desc = models.CharField(max_length=200, verbose_name="Caixa Descrição", null=True)

    create_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.caixa)
    
    class Meta:
        verbose_name = 'CAIXA'
        verbose_name_plural = 'CAIXAS'
        ordering = ['id']
        
class TipoGuarda(models.Model):
    id = models.AutoField(primary_key=True)
    # tipo_guarda = models.IntegerField(verbose_name="Tipo de Guarda", null=True, blank=True)
    tipo_guarda_descricao = models.CharField(max_length=50, verbose_name="Tipo de guarda descrição", null=True)
    create_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.tipo_guarda_descricao)
    
    class Meta:
        verbose_name = 'CAIXA'
        verbose_name_plural = 'CAIXAS'
        ordering = ['id']

class Codigos(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=10, verbose_name="Código", null=True)
    descritor_do_codigo = models.TextField(verbose_name="Descritor do código", null=True, blank=True)
    
    # fase_corrente_ano = models.IntegerField(verbose_name="Fase corrente ano", null=True, blank=True)
    # fase_corrente_ano = models.IntegerField(verbose_name="Fase corrente ano", default=0, blank=True)
    fase_corrente_ano = models.IntegerField(verbose_name="Fase corrente ano", null=True, blank=True, default=0)

    fase_corrente_desc = models.TextField(verbose_name="Fase corrente descrição", null=True, blank=True)
    
    fase_intermediaria_ano = models.IntegerField(verbose_name="Fase intermediária Ano", null=True, blank=True, default=0)
    fase_intermediaria_desc = models.TextField(verbose_name="Fase intermediária descrição", null=True, blank=True)
    
    destinacao_final_ano = models.IntegerField(verbose_name="Destinação final ano", null=True, blank=True, default=0)
    destinacao_final_desc = models.TextField(verbose_name="Destinação final descrição", null=True, blank=True)
    fk_tipo_guarda = models.ForeignKey(TipoGuarda, on_delete=models.CASCADE, verbose_name="Tipo de Guarda", default=1, blank=True)

    observacoes_ano = models.IntegerField(verbose_name="Observações ano", null=True, blank=True, default=0)
    observacoes_desc = models.TextField(verbose_name="Observações descrição", null=True, blank=True)

    create_at = models.DateTimeField(auto_now_add=True, null=True)

    #
    def __str__(self):
        return str(self.codigo)
    
    class Meta:
        verbose_name = 'Codigo'
        verbose_name_plural = 'Codigos'
        ordering = ['id']

class Docs(models.Model):
    id = models.AutoField(primary_key=True)
    doc_data = models.DateField(verbose_name="Data do documento", null=True, blank=True)
    fk_codigo = models.ForeignKey(Codigos, on_delete=models.CASCADE, verbose_name="CÓDIGO", null=True, blank=True)
    
    doc_destinacao_final =models.CharField(max_length=50, verbose_name="Destinação final", null=True, blank=True)
    doc_eliminacao_ano = models.IntegerField(verbose_name="Ano de eliminacao", null=True, blank=True)
    doc_corrente_ano = models.IntegerField(verbose_name="Fase corrente anos", null=True, blank=True)
    doc_intermediario_ano = models.IntegerField(verbose_name="Fase intermediaria anos", null=True, blank=True)
    doc_destinacao_final_ano = models.IntegerField(verbose_name="Destinação final anos", null=True, blank=True)
    doc_obs_ano = models.IntegerField(verbose_name="Observação ano", null=True, blank=True)
    
    
    fk_tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE, verbose_name="TIPO", null=True, blank=True)
    fk_doc_origem = models.ForeignKey(Om, on_delete=models.CASCADE, verbose_name="ORIGEM", related_name='fk_doc_origem', null=True, blank=True)
    fk_doc_destino = models.ForeignKey(Om, on_delete=models.CASCADE, verbose_name="DESTINO", related_name='fk_doc_destino', null=True, blank=True)
    fk_caixa = models.ForeignKey(Caixa, on_delete=models.CASCADE, verbose_name="CAIXA", null=True, blank=True)
    fk_tcu = models.ForeignKey(Tcu, on_delete=models.CASCADE, verbose_name="TCU", null=True, blank=True)
    
    doc_numero = models.CharField(max_length=50, verbose_name="Numero do documento", null=True, blank=True)
    
    new_file_sigad = models.CharField(max_length=50, verbose_name="NewFile/SIGAD", null=True, blank=True)
    
    
    
    
    
    
    # Campo ForeignKey para armazenar o usuário logado
    # fk_usuario_logado = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_usuario_logado', blank=True, null=True)

    

    create_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.doc_numero)
    
    class Meta:
        verbose_name = 'DOCUMENTO'
        verbose_name_plural = 'DOCUMENTOS'
        ordering = ['id']




