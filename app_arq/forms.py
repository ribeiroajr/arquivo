from django import forms
from django.forms.widgets import ClearableFileInput
from .models import *
from django import forms


class CodigosForm(forms.ModelForm):
    class Meta:
        model = Codigos
        fields = '__all__'

class OmForm(forms.ModelForm):
    class Meta:
        model = Om
        fields = '__all__'

class TipoForm(forms.ModelForm):
    class Meta:
        model = Tipo
        fields = '__all__'

class TcuForm(forms.ModelForm):
    class Meta:
        model = Tcu
        fields = '__all__'

class AnoForm(forms.ModelForm):
    class Meta:
        model = Ano
        fields = '__all__'

class CaixaForm(forms.ModelForm):
    class Meta:
        model = Caixa
        fields = '__all__'
        
class Tipo_guardaForm(forms.ModelForm):
    class Meta:
        model = TipoGuarda
        fields = '__all__'

class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%d-%m-%Y"
        super().__init__(**kwargs)
    
# class DocsForm(forms.ModelForm):
#     class Meta:
#         model = Docs
#         fields = '__all__'    
        
##___________________________________________________
class DocsForm(forms.ModelForm):
    doc_numero = forms.CharField(widget=forms.TextInput(attrs={'style': 'text-transform:uppercase'}))
    new_file_sigad = forms.CharField(widget=forms.TextInput(attrs={'style': 'text-transform:uppercase'}))
    # fk_caixa = forms.ModelChoiceField(label='Situacao da caixa:', queryset=Status.objects.filter(status='ABERTA'), required=False)

    class Meta:
        model = Docs
        fields = '__all__'
        # fields = ['fk_codigo', 'fk_tipo', 'fk_doc_origem', 'fk_doc_destino', 'fk_caixa', 'fk_tcu', 'doc_numero', 'doc_data', 'new_file_sigad']

    def __init__(self, *args, **kwargs):
        super(DocsForm, self).__init__(*args, **kwargs)
        self.fields["doc_data"].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['fk_codigo'].widget.attrs['class'] = 'form-control'
        self.fields['fk_tipo'].widget.attrs['class'] = 'form-control'
        self.fields['fk_doc_origem'].widget.attrs['class'] = 'form-control'
        self.fields['fk_doc_destino'].widget.attrs['class'] = 'form-control'

        self.fields['fk_caixa'].widget.attrs['class'] = 'form-control'

        self.fields['fk_tcu'].widget.attrs['class'] = 'form-control'
        
        self.fields['doc_numero'].widget.attrs['class'] = 'form-control'
        self.fields['doc_numero'].required = False
        self.fields['doc_data'].widget.attrs['class'] = 'form-control'
        
        self.fields['new_file_sigad'].widget.attrs['class'] = 'form-control'
        self.fields['new_file_sigad'].widget.attrs['placeholder'] = 'NewFile/SIGAD'
        self.fields['new_file_sigad'].required = False


        self.fields['doc_corrente_ano'].widget.attrs['class'] = 'form-control'
        self.fields['doc_corrente_ano'].widget.attrs['readonly'] = True

        # self.fields['doc_intermediario_ano'].widget.attrs['class'] = 'form-control'
        self.fields['doc_intermediario_ano'].widget.attrs.update({'class': 'form-control', 'readonly': True})
        self.fields['doc_intermediario_ano'].widget.attrs['readonly'] = True

        self.fields['doc_destinacao_final_ano'].widget.attrs['class'] = 'form-control'
        self.fields['doc_destinacao_final_ano'].widget.attrs['readonly'] = True

        self.fields['doc_eliminacao_ano'].widget.attrs['class'] = 'form-control'
        self.fields['doc_eliminacao_ano'].widget.attrs['readonly'] = True
        
        self.fields['doc_obs_ano'].widget.attrs['class'] = 'form-control'
        self.fields['doc_obs_ano'].widget.attrs['readonly'] = True
        
        self.fields['doc_destinacao_final'].widget.attrs['class'] = 'form-control'
               
        self.fields['doc_numero'].widget.attrs['placeholder'] = 'Numero do documento'






# self.fields['doc_intermediario_ano'].widget.attrs.update({'class': 'form-control', 'readonly': True})
# self.fields['doc_destinacao_final_ano'].widget.attrs.update({'class': 'form-control', 'readonly': True})
# self.fields['doc_eliminacao_ano'].widget.attrs.update({'class': 'form-control', 'readonly': True})
# self.fields['doc_obs_ano'].widget.attrs.update({'class': 'form-control', 'readonly': True})
# self.fields['doc_destinacao_final'].widget.attrs['class'] = 'form-control'
# self.fields['doc_numero'].widget.attrs['placeholder'] = 'Numero do documento'
###_______________________________________



# class NumeracaoForm(forms.ModelForm):
#     fk_tipo = forms.ModelChoiceField(queryset=Tipo.objects.all(), initial=None)
#     fk_user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput)
#     destino_doc = forms.CharField(widget=forms.TextInput(attrs={'style': 'text-transform:uppercase'}))
#     doc_sigad_origem = forms.CharField(widget=forms.TextInput(attrs={'style': 'text-transform:uppercase'}))

#     class Meta:
#         # specify model to be used
#         model = Numeracao
 
#         # specify fields to be used
#         fields = [
#             "fk_tipo",
#             "doc_numero",
#             "fk_setor",
#             "destino_doc",
#             "doc_sigad_origem",
#             "doc_description",
#             "fk_user",
#         ]
    
#     def __init__(self, *args, **kwargs):
#         super(NumeracaoForm, self).__init__(*args, **kwargs)
#         self.fields['fk_tipo'].label = "Tipo do Documento"
#         self.fields['fk_tipo'].widget.attrs['class'] = 'form-control'
#         self.fields['fk_tipo'].widget.attrs['readonly'] = True

#         self.fields['doc_sigad_origem'].widget.attrs['placeholder'] = 'SIGADAER de origem do documento'
        
#         self.fields['doc_numero'].widget.attrs['class'] = 'form-control'
#         self.fields['doc_numero'].widget.attrs['readonly'] = True
        
#         self.fields['fk_setor'].widget.attrs['class'] = 'form-control'

#         self.fields['doc_sigad_origem'].widget.attrs['class'] = 'form-control'

#         self.fields['doc_description'].widget.attrs['class'] = 'form-control'
        
#         self.fields['destino_doc'].widget.attrs['class'] = 'form-control'
#         self.fields['destino_doc'].widget.attrs['placeholder'] = 'Se houver mais de um destino, separe-os por vírgula e espaço ex: COMAR I, COMAR II.'



























# class DocsForm(forms.ModelForm):
#     class Meta:
#         model = Docs
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super(DocsForm, self).__init__(*args, **kwargs)
#         self.fields["doc_data"].widget = forms.DateInput(attrs={'type': 'date'})

        
    # class Meta:
    #     model = Codigos
    #     fields = '__all__'  # Ou liste os campos que deseja incluir no formulário manualmente
    #     widgets = {
    #         'fk_ano_curso': forms.Select(),
    #         'fk_turma': forms.Select(),
    #         'fk_tipo': forms.Select(),
    #         'fk_assinaturas': forms.Select(),
    #     }

# class CSVUploadForm(forms.Form):
#     file = forms.FileField()

# class AlunoForm(forms.ModelForm):
#     class Meta:
#         model = Aluno
#         fields = '__all__'  # Ou liste os campos que deseja incluir no formulário manualmente
#         widgets = {
#             'fk_status': forms.Select(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
#             'fk_turma': forms.Select(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
#             'fk_curso': forms.Select(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
#             'fk_forca_orgao': forms.Select(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
#             'fk_om': forms.Select(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
#             'fk_posto': forms.Select(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
#             'fk_quadro': forms.Select(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
#             'fk_especialidade': forms.Select(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
#             'fk_aluno_tipo': forms.Select(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
#             'fk_in_ex': forms.Select(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
#             'fk_tratamento': forms.Select(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
#             'aluno_nome': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
#             'aluno_cpf': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
#             'aluno_email': forms.EmailInput(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
#             'aluno_nota': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
#             'codigo_hash': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
#             'qrcode': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
#         }



# forms.py
# class AlunoCreationForm(forms.ModelForm):
#     class Meta:
#         model = Aluno
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['fk_posto'].queryset = Posto.objects.none()
#         self.fields['fk_quadro'].queryset = Quadro.objects.none()
#         self.fields['fk_especialidade'].queryset = Especialidade.objects.none()
#         self.fields['fk_turma'].queryset = Turma.objects.none()  # Certifique-se de adicionar o campo fk_turma

#         if 'fk_forca_orgao' in self.data:
#             try:
#                 forca_orgao_id = int(self.data.get('fk_forca_orgao'))
#                 self.fields['fk_posto'].queryset = Posto.objects.filter(fk_forca_orgao_id=forca_orgao_id).order_by('posto')
#                 self.fields['fk_quadro'].queryset = Quadro.objects.filter(fk_forca_orgao_id=forca_orgao_id).order_by('quadro')
#                 self.fields['fk_especialidade'].queryset = Especialidade.objects.filter(fk_forca_orgao_id=forca_orgao_id).order_by('especialidade')
                
#                 # Aqui vem a lógica para atualizar o queryset de fk_turma de acordo com fk_curso
#                 self.fields['fk_turma'].queryset = Turma.objects.filter(fk_curso__fk_forca_orgao_id=forca_orgao_id).order_by('turma')
#             except (ValueError, TypeError):
#                 pass
#         elif self.instance.pk:
#             self.fields['fk_posto'].queryset = self.instance.fk_forca_orgao.posto_set.order_by('posto')
#             self.fields['fk_quadro'].queryset = self.instance.fk_forca_orgao.quadro_set.order_by('quadro')
#             self.fields['fk_especialidade'].queryset = self.instance.fk_forca_orgao.especialidade_set.order_by('especialidade')
            
#             # Atualize o queryset de fk_turma com base no curso associado ao aluno
#             self.fields['fk_turma'].queryset = self.instance.fk_curso.turma_set.all()






# class ModeloForm(forms.ModelForm):
#     class Meta:
#         model = Modelo
#         fields = '__all__'  # Ou liste os campos que deseja incluir no formulário manualmente
#         widgets = {
#             'fk_id_aluno': forms.Select(),
#         }

# class TipoForm(forms.ModelForm):
#     class Meta:
#         model = Tipo
#         fields = '__all__'  # Ou liste os campos que deseja incluir no formulário manualmente

# class AnoForm(forms.ModelForm):
#     class Meta:
#         model = Ano
#         fields = '__all__'  # Ou liste os campos que deseja incluir no formulário manualmente

# class StatusForm(forms.ModelForm):
#     class Meta:
#         model = Status
#         fields = '__all__'  # Ou liste os campos que deseja incluir no formulário manualmente

# # class Imagem(forms.ModelForm):
# #     assinatura_dpl_img = forms.ImageField(widget=ClearableFileInput)
# #     class Meta:
# #         model = Assinaturas_DPL
# #         fields = '__all__'  # Ou liste os campos que deseja incluir no formulário manualmente
# #         widgets = {
# #             'assinatura_dpl' : forms.TextInput(attrs={
# #                 'class': 'form-control',
# #                 'max_length': 50,
# #                 'placeholder': 'Nome da assinatura DPL'
# #             }),'assinatura_dpl_cargo' : forms.TextInput(attrs={
# #                 'class': 'form-control',
# #                 'max_length': 50,
# #                 'placeholder': 'Descrição assinatura DPL'
# #             })
# #         }
# #         error_messages = {
# #             'assinatura_dpl': {
# #                 'required': 'O campo assinatura e obrigatório'
# #             },
# #             'assinatura_dpl_cargo': {
# #                 'required': 'O campo assinatura_cargo e obrigatório'
# #             }

# #         }

# # class AssinaturaCHForm(forms.ModelForm):
# #     assinatura_ch_img = forms.ImageField(widget=ClearableFileInput)
# #     class Meta:
# #         model = Assinaturas_CH
# #         fields = '__all__'  # Ou liste os campos que deseja incluir no formulário manualmente
# #         widgets = {
# #             'assinatura_ch' : forms.TextInput(attrs={
# #                 'class': 'form-control',
# #                 'max_length': 50,
# #                 'placeholder': 'Nome da assinatura CH'
# #             }),'assinatura_ch_cargo' : forms.TextInput(attrs={
# #                 'class': 'form-control',
# #                 'max_length': 50,
# #                 'placeholder': 'Descrição assinatura CH'
# #             })
# #         }
# #         error_messages = {
    
# #             'assinatura_ch': {
# #                 'required': 'O campo assinatura e obrigatório'
# #             },
# #             'assinatura_ch_cargo': {
# #                 'required': 'O campo assinatura_cargo e obrigatório'
# #             }

# #         }

# class GradeTurmaForm(forms.ModelForm):
#     class Meta:
#         model = GradeTurma
#         fields = '__all__'  # Ou liste os campos que deseja incluir no formulário manualmente
        
# class ImagemForm(forms.ModelForm):
#     class Meta:
#         model = Imagem
#         fields = '__all__'  # Ou liste os campos que deseja incluir no formulário manualmente

# class TratamentoForm(forms.ModelForm):
#     class Meta:
#         model = Tratamento
#         fields = '__all__'  # Ou liste os campos que deseja incluir no formulário manualmente

# class InstrucaoForm(forms.ModelForm):
#     class Meta:
#         model = Instrucao
#         fields = '__all__'  # Ou liste os campos que deseja incluir no formulário manualmente

# class TextoForm(forms.ModelForm):
#     class Meta:
#         model = Textos
#         fields = '__all__'  # Ou liste os campos que deseja incluir no formulário manualmente


# class DateInput(forms.DateInput):
#     input_type = "date"

#     def __init__(self, **kwargs):
#         kwargs["format"] = "%d-%m-%Y"
#         super().__init__(**kwargs)

# class TurmaForm(forms.ModelForm):


#     class Meta:
#         model = Turma
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
    
#     # def __init__(self, *args, **kwargs):
#     #     super(TurmaForm, self).__init__(*args, **kwargs)


#         # self.fields["data_inicio_turma_interno"].widget = DateInput()
#         # self.fields["data_fim_turma_interno"].widget = DateInput()
#         # self.fields["data_inicio_turma_externo"].widget = DateInput()
#         # self.fields["data_fim_turma_externo"].widget = DateInput()

#         self.fields['fk_assinaturas_ch'].queryset = Imagem.objects.filter(imagem_tipo__imagemTipo='CH')
#         self.fields['fk_assinaturas_dpl'].queryset = Imagem.objects.filter(imagem_tipo__imagemTipo='DIV')

#         self.fields['fk_img_frente'].queryset = Imagem.objects.filter(imagem_tipo__imagemTipo='FRENTE')
#         self.fields['fk_img_fundo'].queryset = Imagem.objects.filter(imagem_tipo__imagemTipo='VERSO')






# class CertExtForm(forms.ModelForm):
#     # primeira_parte = forms.CharField(label='Primeira Parte:', max_length=100, required=True)
#     a_quem = forms.CharField(label='Para:', max_length=100, required=True)
#     motivo = forms.CharField(label='Motivo:', max_length=100, required=True)

#     # Renomeando o campo campo_texto para tipo
#     tipo = forms.ModelChoiceField(label='Tipo:', queryset=Textos.objects.all(), required=False)
    
#     primeira_parte = forms.ModelChoiceField(label='Primeira_parte:', queryset=Textos.objects.all(), required=False)

#     # Renomeando os rótulos dos campos do modelo Turma
#     fk_assinaturas_ch = forms.ModelChoiceField(label='Chefe do CIAER:', queryset=Imagem.objects.filter(imagem_tipo__imagemTipo='CH'), required=False)
#     fk_assinaturas_dpl = forms.ModelChoiceField(label='Chefe da DIV:', queryset=Imagem.objects.filter(imagem_tipo__imagemTipo='DIV'), required=False)
#     fk_img_frente = forms.ModelChoiceField(label='Imagem de fundo:', queryset=Imagem.objects.filter(imagem_tipo__imagemTipo='FRENTE'), required=False)

#     class Meta:
#         model = Turma
#         fields = ['fk_assinaturas_ch', 'fk_assinaturas_dpl', 'fk_img_frente', 'primeira_parte', 'a_quem', 'motivo', 'tipo']
#         widgets = {
#             'primeira_parte': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
#             'a_quem': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
#             'motivo': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px;'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)






