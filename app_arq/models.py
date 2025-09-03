from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    """
    Modelo base com campos comuns a serem herdados por outros modelos.
    """
    id = models.AutoField(primary_key=True)
    fk_user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Usuário", default=1)
    create_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        abstract = True

class LogAcaoUsuario(BaseModel):
    acao = models.CharField(max_length=100, verbose_name="Ação realizada")
    # data_acao = models.DateTimeField(auto_now_add=True, verbose_name="Data e hora da ação")
    objeto = models.CharField(max_length=100)
    objeto_id = models.PositiveIntegerField()  # Campo para armazenar o ID do objeto

    class Meta:
        verbose_name = 'Log de Ação do Usuário'
        verbose_name_plural = 'Logs de Ações dos Usuários'

    def __str__(self):
        return f'{self.fk_user.username} - {self.acao} - {self.create_at}'




class Status(BaseModel):
    """
    Representa o status de um objeto.
    """
    status = models.CharField(max_length=10, verbose_name="Status")

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Status'


class Tcu(BaseModel):
    """
    Representa o Tribunal de Contas da União.
    """
    tcu = models.CharField(max_length=250, verbose_name="Número")
    # tcu_desc = models.CharField(max_length=200, verbose_name="Descrição")

    def __str__(self):
        return self.tcu

    class Meta:
        verbose_name = 'TCU'
        verbose_name_plural = 'TCUs'


class Om(BaseModel):
    """
    Representa uma Organização Militar.
    """
    om = models.CharField(max_length=200, verbose_name="OM")
    # om_descricao = models.CharField(max_length=200, verbose_name="Descrição")

    def __str__(self):
        return self.om

    class Meta:
        verbose_name = 'OM'
        verbose_name_plural = 'OMs'


class Tipo(BaseModel):
    """
    Representa um tipo genérico.
    """
    tipo = models.CharField(max_length=200, verbose_name="Tipo")
    # tipo_desc = models.CharField(max_length=200, verbose_name="Descrição")

    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name = 'Tipo'
        verbose_name_plural = 'Tipos'


class Ano(BaseModel):
    """
    Representa um ano.
    """
    ano = models.CharField(max_length=10, verbose_name="Ano")

    def __str__(self):
        return self.ano

    class Meta:
        verbose_name = 'Ano'
        verbose_name_plural = 'Anos'


class Caixa(BaseModel):
    """
    Representa uma caixa.
    """
    fk_ano = models.ForeignKey(Ano, on_delete=models.CASCADE, verbose_name="Ano")
    fk_status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name="Status da caixa")
    caixa = models.CharField(max_length=200, verbose_name="Caixa")
    # caixa_desc = models.CharField(max_length=200, verbose_name="Descrição da caixa")

    def __str__(self):
        return self.caixa

    class Meta:
        verbose_name = 'Caixa'
        verbose_name_plural = 'Caixas'


class TipoGuarda(BaseModel):
    """
    Representa um tipo de guarda.
    """
    tipo_guarda_descricao = models.CharField(max_length=50, verbose_name="Descrição do tipo de guarda")

    def __str__(self):
        return self.tipo_guarda_descricao

    class Meta:
        verbose_name = 'Tipo de Guarda'
        verbose_name_plural = 'Tipos de Guarda'


class Codigos(BaseModel):
    """
    Representa um código.
    """
    codigo = models.CharField(max_length=10, verbose_name="Código")
    descritor_do_codigo = models.TextField(verbose_name="Descritor do código")
    fase_corrente_ano = models.IntegerField(verbose_name="Fase corrente ano", blank=True, default=0)
    fase_corrente_desc = models.TextField(verbose_name="Fase corrente descrição", blank=True, null=True)
    fase_intermediaria_ano = models.IntegerField(verbose_name="Fase intermediária ano", blank=True, default=0)
    fase_intermediaria_desc = models.TextField(verbose_name="Fase intermediária descrição", blank=True, null=True)
    destinacao_final_ano = models.IntegerField(verbose_name="Destinação final ano", blank=True, default=0)
    destinacao_final_desc = models.TextField(verbose_name="Destinação final descrição", blank=True, null=True)
    fk_tipo_guarda = models.ForeignKey(TipoGuarda, on_delete=models.CASCADE, verbose_name="Tipo de Guarda", blank=True, default=1)
    observacoes_ano = models.IntegerField(verbose_name="Observações ano", blank=True, default=0)
    observacoes_desc = models.TextField(verbose_name="Observações descrição", blank=True, null=True)

    def __str__(self):
        return self.codigo

    class Meta:
        verbose_name = 'Código'
        verbose_name_plural = 'Códigos'


class Docs(BaseModel):
    """
    Representa um documento.
    """
    doc_data = models.DateField(verbose_name="Data do documento", blank=True, null=True)
    fk_codigo = models.ForeignKey(Codigos, on_delete=models.CASCADE, verbose_name="Código", null=True, blank=True)
    doc_destinacao_final = models.CharField(max_length=50, verbose_name="Destinação final", blank=True)
    doc_corrente_ano = models.IntegerField(verbose_name="Fase corrente anos", blank=True, null=True)

    doc_eliminacao_ano = models.IntegerField(verbose_name="Ano de eliminação", blank=True, null=True)
    doc_numero = models.CharField(max_length=50, verbose_name="Número do documento", blank=True)
    new_file_sigad = models.CharField(max_length=50, verbose_name="NewFile/SIGAD", blank=True)

    fk_tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE, verbose_name="Tipo", null=True, blank=True)

    fk_doc_origem = models.ForeignKey(Om, on_delete=models.CASCADE, verbose_name="Origem", related_name='fk_doc_origem', null=True, blank=True)
    fk_doc_destino = models.ForeignKey(Om, on_delete=models.CASCADE, verbose_name="Destino", related_name='fk_doc_destino', null=True, blank=True)

    fk_caixa = models.ForeignKey(Caixa, on_delete=models.CASCADE, verbose_name="Caixa", null=True, blank=True)
    fk_tcu = models.ForeignKey(Tcu, on_delete=models.CASCADE, verbose_name="TCU", null=True, blank=True)

    doc_intermediario_ano = models.IntegerField(verbose_name="Fase intermediária anos", blank=True, null=True)
    doc_destinacao_final_ano = models.IntegerField(verbose_name="Destinação final anos", blank=True, null=True)
    doc_obs_ano = models.IntegerField(verbose_name="Observação ano", blank=True, null=True) 
    
    status_doc = models.BooleanField(default=False, verbose_name="Conferido")

    def __str__(self):
        return self.doc_numero

    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'


